"""
Plant Disease Detection Training
MobileNetV2 transfer learning + fine-tuning.

Expected layout (one of the existing layouts is detected automatically):
PROJECT_ROOT/
    backend/
        train_model.py
        plant_disease_model.keras
        class_names.json
    dataset_split/
        train/<class_name>/*.jpg
        val/<class_name>/*.jpg
        test/<class_name>/*.jpg   # optional independent test set

Or:
PROJECT_ROOT/New Plant Diseases Dataset(Augmented)/...
    train/<class_name>/*.jpg
    valid/<class_name>/*.jpg

Install:
    python -m pip install tensorflow pillow

Optional test-set evaluation:
    python train_model.py --epochs 20 --test-dir "..\\dataset_split\\test"
"""

import argparse
import json
from pathlib import Path
from typing import Optional

import numpy as np
import tensorflow as tf
from PIL import Image, UnidentifiedImageError


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

MODEL_SAVE_PATH = BASE_DIR / "plant_disease_model.keras"
LABELS_SAVE_PATH = BASE_DIR / "class_names.json"
BEST_MODEL_PATH = BASE_DIR / "plant_disease_model.keras"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
DEFAULT_EPOCHS = 20
FINE_TUNE_LAYERS = 30
AUTOTUNE = tf.data.AUTOTUNE
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}


def find_dataset_dirs():
    """Locate training and validation directories using the existing path rules."""
    split_train = PROJECT_ROOT / "dataset_split" / "train"
    split_val = PROJECT_ROOT / "dataset_split" / "val"
    if split_train.is_dir() and split_val.is_dir():
        return split_train, split_val

    nested_root = (
        PROJECT_ROOT
        / "New Plant Diseases Dataset(Augmented)"
        / "New Plant Diseases Dataset(Augmented)"
    )
    train_candidate = nested_root / "train"
    val_candidate = nested_root / "valid"
    if train_candidate.is_dir() and val_candidate.is_dir():
        return train_candidate, val_candidate

    direct_train = PROJECT_ROOT / "New Plant Diseases Dataset(Augmented)" / "train"
    direct_val = PROJECT_ROOT / "New Plant Diseases Dataset(Augmented)" / "valid"
    if direct_train.is_dir() and direct_val.is_dir():
        return direct_train, direct_val

    raise FileNotFoundError(
        "Could not automatically locate train and validation directories.\n"
        f"Checked: {split_train}, {train_candidate}, and {direct_train}.\n"
        "Pass --train-dir and --val-dir to specify the directories explicitly."
    )


def validate_dataset_directories(train_dir: Path, val_dir: Path):
    """Check class folders and matching class names before loading data."""
    if not train_dir.is_dir():
        raise FileNotFoundError(f"Training directory not found: {train_dir}")
    if not val_dir.is_dir():
        raise FileNotFoundError(f"Validation directory not found: {val_dir}")

    train_classes = sorted(p.name for p in train_dir.iterdir() if p.is_dir())
    val_classes = sorted(p.name for p in val_dir.iterdir() if p.is_dir())

    if not train_classes:
        raise ValueError(f"No class subfolders found in training directory: {train_dir}")
    if train_classes != val_classes:
        missing_in_val = sorted(set(train_classes) - set(val_classes))
        extra_in_val = sorted(set(val_classes) - set(train_classes))
        raise ValueError(
            "Training and validation class folders do not match.\n"
            f"Missing from validation: {missing_in_val}\n"
            f"Only in validation: {extra_in_val}"
        )
    return train_classes


def build_model(num_classes: int) -> tuple[tf.keras.Model, tf.keras.Model]:
    """Build MobileNetV2 with a frozen feature extractor and a new classifier."""
    inputs = tf.keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3), name="input_image")

    # MobileNetV2 expects pixels scaled from [0, 255] to [-1, 1].
    scaled = tf.keras.layers.Rescaling(
        scale=1.0 / 127.5, offset=-1.0, name="rescaling"
    )(inputs)

    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False

    x = base_model(scaled, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = tf.keras.layers.Dropout(0.2, name="dropout")(x)
    outputs = tf.keras.layers.Dense(
        num_classes, activation="softmax", name="predictions"
    )(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="plant_disease_model")
    return model, base_model


def make_callbacks(stage_name: str, initial_best_val_loss=None):
    """Stop when validation loss stalls and retain the best model checkpoint."""
    checkpoint_args = {
        "filepath": str(BEST_MODEL_PATH),
        "monitor": "val_loss",
        "mode": "min",
        "save_best_only": True,
        "verbose": 1,
    }
    # Preserve the best checkpoint from stage 1 when stage 2 starts.
    if initial_best_val_loss is not None:
        checkpoint_args["initial_value_threshold"] = float(initial_best_val_loss)

    return [
        tf.keras.callbacks.ModelCheckpoint(**checkpoint_args),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            mode="min",
            patience=4 if stage_name == "head" else 5,
            min_delta=0.001,
            restore_best_weights=True,
            verbose=1,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            mode="min",
            factor=0.2,
            patience=2,
            min_lr=1e-7,
            verbose=1,
        ),
    ]


def evaluate_classwise(model, dataset, class_names, dataset_label="Validation"):
    """Print accuracy, precision, recall, and F1 for each class without sklearn."""
    y_true_batches = []
    y_pred_batches = []

    for images, labels in dataset:
        probabilities = model.predict(images, verbose=0)
        y_pred_batches.extend(np.argmax(probabilities, axis=1).tolist())
        y_true_batches.extend(np.argmax(labels.numpy(), axis=1).tolist())

    y_true = np.asarray(y_true_batches, dtype=np.int64)
    y_pred = np.asarray(y_pred_batches, dtype=np.int64)

    if len(y_true) == 0:
        print(f"{dataset_label} dataset is empty; skipping class-wise metrics.")
        return

    correct = int(np.sum(y_true == y_pred))
    print(f"\n=== {dataset_label} evaluation ===")
    print(f"Overall accuracy: {correct / len(y_true) * 100:.2f}%")
    print(f"Images evaluated: {len(y_true)}")
    print("\nPer-class metrics:")
    print(f"{'Class':45s} {'Precision':>10s} {'Recall':>10s} {'F1-score':>10s} {'Support':>9s}")
    print("-" * 90)

    for class_index, class_name in enumerate(class_names):
        tp = int(np.sum((y_true == class_index) & (y_pred == class_index)))
        fp = int(np.sum((y_true != class_index) & (y_pred == class_index)))
        fn = int(np.sum((y_true == class_index) & (y_pred != class_index)))
        support = int(np.sum(y_true == class_index))

        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall
            else 0.0
        )
        print(
            f"{class_name[:45]:45s} {precision:10.3f} {recall:10.3f} "
            f"{f1:10.3f} {support:9d}"
        )


def load_dataset(directory: Path, class_names, batch_size: int, shuffle: bool):
    """Load images with a fixed class order and prefetch batches."""
    dataset = tf.keras.utils.image_dataset_from_directory(
        directory,
        class_names=class_names,
        image_size=IMG_SIZE,
        batch_size=batch_size,
        label_mode="categorical",
        shuffle=shuffle,
        seed=42,
    )
    return dataset.prefetch(buffer_size=AUTOTUNE)


def validate_uploaded_image(image_path: str | Path):
    """
    Validate and preprocess an image for inference.
    This checks file readability and image dimensions, but cannot determine
    whether the image actually contains a plant leaf.
    Returns a float32 array with shape (1, 224, 224, 3).
    """
    path = Path(image_path)
    if path.suffix.lower() not in IMAGE_EXTENSIONS:
        raise ValueError(f"Unsupported image extension: {path.suffix}")

    try:
        with Image.open(path) as image:
            image = image.convert("RGB")
            if image.width < 32 or image.height < 32:
                raise ValueError("Image is too small. Please upload a clearer image.")
            image = image.resize(IMG_SIZE)
            array = np.asarray(image, dtype=np.float32)
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("The uploaded file is not a readable image.") from exc

    return np.expand_dims(array, axis=0)


def train(
    train_dir: Path,
    val_dir: Path,
    epochs: int = DEFAULT_EPOCHS,
    batch_size: int = BATCH_SIZE,
    subset_batches: Optional[int] = None,
    test_dir: Optional[Path] = None,
    fine_tune: bool = True,
):
    print("=== Plant Disease Detection: MobileNetV2 ===")
    print(f"Training directory : {train_dir}")
    print(f"Validation directory: {val_dir}")
    print(f"Image size         : {IMG_SIZE}")
    print(f"Batch size         : {batch_size}")
    print(f"Maximum epochs     : {epochs}")
    print(f"Fine-tuning        : {'enabled' if fine_tune else 'disabled'}")
    print("Early stopping and best-checkpoint saving: enabled")
    print("============================================\n")

    class_names = validate_dataset_directories(train_dir, val_dir)
    num_classes = len(class_names)
    print(f"Found {num_classes} classes.")
    print("Class names:", class_names)

    # Keep the class mapping stable and available to the website.
    with open(LABELS_SAVE_PATH, "w", encoding="utf-8") as file:
        json.dump(class_names, file, indent=2, ensure_ascii=False)
    print(f"Saved class labels to: {LABELS_SAVE_PATH}")

    train_ds = load_dataset(train_dir, class_names, batch_size, shuffle=True)
    val_ds = load_dataset(val_dir, class_names, batch_size, shuffle=False)

    if subset_batches is not None and subset_batches > 0:
        print(f"QUICK MODE: at most {subset_batches} training batches.")
        train_ds = train_ds.take(subset_batches)
        val_ds = val_ds.take(max(1, subset_batches // 2))

    model, base_model = build_model(num_classes)

    # Stage 1: train only the newly added classification head.
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    print("\n=== Stage 1: Train classification head ===")
    model.summary()
    head_epochs = max(1, epochs // 2) if fine_tune else epochs
    head_history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=head_epochs,
        callbacks=make_callbacks("head"),
    )

    # Reload the best checkpoint before fine-tuning.
    if BEST_MODEL_PATH.exists():
        model = tf.keras.models.load_model(BEST_MODEL_PATH)

    # Stage 2: unfreeze only the final part of MobileNetV2 and use a low LR.
    if fine_tune:
        print("\n=== Stage 2: Fine-tune selected MobileNetV2 layers ===")
        # The model's first layers are input, rescaling, then the base model.
        base_model = model.layers[2]
        base_model.trainable = True

        # Freeze earlier feature layers; fine-tune only the last N layers.
        fine_tune_from = max(0, len(base_model.layers) - FINE_TUNE_LAYERS)
        for layer in base_model.layers[:fine_tune_from]:
            layer.trainable = False

        # BatchNormalization layers are kept frozen for stable fine-tuning.
        for layer in base_model.layers:
            if isinstance(layer, tf.keras.layers.BatchNormalization):
                layer.trainable = False

        # Establish the stage-1 checkpoint's validation loss as the threshold,
        # so fine-tuning cannot overwrite it with a worse model.
        stage1_metrics = model.evaluate(val_ds, verbose=0, return_dict=True)
        stage1_best_val_loss = stage1_metrics.get("loss")

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
            loss="categorical_crossentropy",
            metrics=["accuracy"],
        )
        model.summary()
        fine_tune_epochs = max(1, epochs - head_epochs)
        model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=fine_tune_epochs,
            callbacks=make_callbacks(
                "fine_tune",
                initial_best_val_loss=stage1_best_val_loss,
            ),
        )

    # Restore the best saved checkpoint across both stages.
    if BEST_MODEL_PATH.exists():
        model = tf.keras.models.load_model(BEST_MODEL_PATH)

    # Save at the established output path; keep class_names.json compatible.
    model.save(MODEL_SAVE_PATH)
    print(f"\nBest model saved to: {MODEL_SAVE_PATH}")
    print(f"Class names saved to: {LABELS_SAVE_PATH}")

    val_metrics = model.evaluate(val_ds, verbose=1, return_dict=True)
    print("\nFinal validation metrics:")
    for metric_name, value in val_metrics.items():
        print(f"{metric_name}: {value:.4f}")

    evaluate_classwise(model, val_ds, class_names, "Validation")

    # An independent test set is optional and should not be used for tuning.
    if test_dir is not None:
        test_dir = test_dir.resolve()
        if not test_dir.is_dir():
            raise FileNotFoundError(f"Test directory not found: {test_dir}")
        test_classes = sorted(p.name for p in test_dir.iterdir() if p.is_dir())
        if test_classes != sorted(class_names):
            raise ValueError(
                "Test class folders do not match training classes.\n"
                f"Expected: {sorted(class_names)}\nFound: {test_classes}"
            )
        test_ds = load_dataset(test_dir, class_names, batch_size, shuffle=False)
        test_metrics = model.evaluate(test_ds, verbose=1, return_dict=True)
        print("\nIndependent test metrics:")
        for metric_name, value in test_metrics.items():
            print(f"{metric_name}: {value:.4f}")
        evaluate_classwise(model, test_ds, class_names, "Independent test")

    print("\nTraining and evaluation completed.")
    print("Note: image file validation does not prove an image contains a plant leaf.")
    return model, head_history


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a MobileNetV2 plant disease classifier."
    )
    parser.add_argument("--epochs", type=int, default=DEFAULT_EPOCHS,
                        help="Maximum total epochs across both stages (default: 20)")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE,
                        help="Images per batch (default: 32)")
    parser.add_argument("--quick", action="store_true",
                        help="Run on a small subset to verify the pipeline")
    parser.add_argument("--batches", type=int, default=None,
                        help="Number of training batches in quick mode")
    parser.add_argument("--train-dir", type=str, default=None,
                        help="Explicit training directory")
    parser.add_argument("--val-dir", type=str, default=None,
                        help="Explicit validation directory")
    parser.add_argument("--test-dir", type=str, default=None,
                        help="Optional independent test directory")
    parser.add_argument("--no-fine-tune", action="store_true",
                        help="Disable MobileNetV2 fine-tuning")
    args = parser.parse_args()

    if args.epochs < 1:
        parser.error("--epochs must be at least 1")
    if args.batch_size < 1:
        parser.error("--batch-size must be at least 1")

    if args.train_dir and args.val_dir:
        train_path = Path(args.train_dir).resolve()
        val_path = Path(args.val_dir).resolve()
    elif args.train_dir or args.val_dir:
        parser.error("Provide both --train-dir and --val-dir, or neither.")
    else:
        train_path, val_path = find_dataset_dirs()

    batch_limit = args.batches
    if args.quick and not batch_limit:
        batch_limit = 10

    train(
        train_dir=train_path,
        val_dir=val_path,
        epochs=args.epochs,
        batch_size=args.batch_size,
        subset_batches=batch_limit,
        test_dir=Path(args.test_dir) if args.test_dir else None,
        fine_tune=not args.no_fine_tune,
    )
