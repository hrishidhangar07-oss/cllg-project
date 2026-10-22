import os
import sys
import random
import shutil
import argparse
from pathlib import Path

# Base directories resolved relative to this script
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# Candidate locations for the dataset
CANDIDATE_SOURCES = [
    PROJECT_ROOT / "New Plant Diseases Dataset(Augmented)" / "New Plant Diseases Dataset(Augmented)" / "train",
    PROJECT_ROOT / "New Plant Diseases Dataset(Augmented)" / "train",
    PROJECT_ROOT / "New Plant Diseases Dataset(Augmented)" / "New Plant Diseases Dataset(Augmented)",
    PROJECT_ROOT / "New Plant Diseases Dataset(Augmented)",
    Path("New Plant Diseases Dataset(Augmented)") / "New Plant Diseases Dataset(Augmented)" / "train",
    Path("New Plant Diseases Dataset(Augmented)") / "train",
    Path("New Plant Diseases Dataset(Augmented)"),
]

def find_source_dir() -> Path:
    for candidate in CANDIDATE_SOURCES:
        candidate_resolved = candidate.resolve()
        if candidate_resolved.exists() and candidate_resolved.is_dir():
            # Check if this folder directly contains class subfolders (not just 'train' or 'valid')
            subdirs = [p for p in candidate_resolved.iterdir() if p.is_dir()]
            subdir_names = {p.name.lower() for p in subdirs}
            if "train" in subdir_names:
                train_dir = candidate_resolved / "train"
                if train_dir.is_dir():
                    return train_dir
            if len(subdirs) > 2 and "train" not in subdir_names:
                return candidate_resolved
    # Fallback to the nested train folder if it exists or root
    default_path = PROJECT_ROOT / "New Plant Diseases Dataset(Augmented)" / "New Plant Diseases Dataset(Augmented)" / "train"
    return default_path

DEFAULT_SOURCE = find_source_dir()
DEFAULT_DEST = PROJECT_ROOT / "dataset_split"

TRAIN_RATIO = 0.70
SEED = 42
EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

def split_dataset(
    source_dir: Path,
    dest_dir: Path,
    train_ratio: float = 0.70,
    seed: int = 42,
    max_per_class: int | None = None
):
    random.seed(seed)
    source_dir = Path(source_dir).resolve()
    dest_dir = Path(dest_dir).resolve()

    print(f"=== Dataset Split Configuration ===")
    print(f"Source directory : {source_dir}")
    print(f"Destination      : {dest_dir}")
    print(f"Train / Val Ratio: {int(train_ratio * 100)}% / {int((1 - train_ratio) * 100)}%")
    print(f"Random seed      : {seed}")
    if max_per_class:
        print(f"Max per class    : {max_per_class} images (subset mode)")
    print("===================================\n")

    if not source_dir.exists():
        raise FileNotFoundError(
            f"Source dataset directory not found at: {source_dir}\n"
            f"Please verify the dataset folder location."
        )

    class_dirs = [d for d in source_dir.iterdir() if d.is_dir()]
    if not class_dirs:
        raise RuntimeError(f"No class subfolders found inside {source_dir}")

    train_dest = dest_dir / "train"
    val_dest = dest_dir / "val"
    train_dest.mkdir(parents=True, exist_ok=True)
    val_dest.mkdir(parents=True, exist_ok=True)

    total_train = 0
    total_val = 0

    print(f"Found {len(class_dirs)} class categories. Processing...")

    for class_dir in sorted(class_dirs, key=lambda d: d.name):
        class_name = class_dir.name
        images = [
            f for f in class_dir.iterdir()
            if f.is_file() and f.suffix.lower() in EXTENSIONS
        ]

        if not images:
            print(f"  [WARN] No matching images found in '{class_name}'")
            continue

        random.shuffle(images)

        if max_per_class and max_per_class > 0:
            images = images[:max_per_class]

        split_idx = int(len(images) * train_ratio)
        train_images = images[:split_idx]
        val_images = images[split_idx:]

        class_train_dir = train_dest / class_name
        class_val_dir = val_dest / class_name
        class_train_dir.mkdir(parents=True, exist_ok=True)
        class_val_dir.mkdir(parents=True, exist_ok=True)

        for img in train_images:
            shutil.copy2(img, class_train_dir / img.name)
        for img in val_images:
            shutil.copy2(img, class_val_dir / img.name)

        total_train += len(train_images)
        total_val += len(val_images)

        print(f"  [OK] {class_name:40s} -> {len(train_images):4d} train, {len(val_images):4d} val")

    print("\n=== Split Complete ===")
    print(f"Total training images  : {total_train}")
    print(f"Total validation images: {total_val}")
    print(f"Output saved to        : {dest_dir}")
    print("======================\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split plant disease dataset into train and val folders.")
    parser.add_argument("--source", type=str, default=str(DEFAULT_SOURCE), help="Path to source dataset folder")
    parser.add_argument("--dest", type=str, default=str(DEFAULT_DEST), help="Destination folder for split dataset")
    parser.add_argument("--train-ratio", type=float, default=TRAIN_RATIO, help="Fraction for train set (default 0.70)")
    parser.add_argument("--seed", type=int, default=SEED, help="Random seed for reproducibility")
    parser.add_argument("--max-per-class", type=int, default=None, help="Optional max images per class (useful for quick testing)")

    args = parser.parse_args()
    split_dataset(
        source_dir=Path(args.source),
        dest_dir=Path(args.dest),
        train_ratio=args.train_ratio,
        seed=args.seed,
        max_per_class=args.max_per_class,
    )
