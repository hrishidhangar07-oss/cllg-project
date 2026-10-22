import os
import json
import base64
from io import BytesIO
from pathlib import Path
from typing import List, Dict, Any, Optional

import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps, UnidentifiedImageError
from fastapi import FastAPI, File, HTTPException, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from disease_info import get_disease_details, get_disease_details_gujarati
from database import (
    save_diagnosis,
    get_history,
    delete_diagnosis,
    clear_all_history,
    get_stats,
    is_db_connected,
    DB_NAME,
    COLLECTION_NAME,
    MONGO_URI
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "plant_disease_model.keras"
LABELS_PATH = BASE_DIR / "class_names.json"

IMG_SIZE = (224, 224)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP", "BMP"}

app = FastAPI(
    title="AgriCure API",
    description="AI-powered plant disease diagnosis and cure recommendation system with automated case record preservation."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

_model = None
_class_names: List[str] = []

def load_model_and_labels():
    global _model, _class_names
    if not MODEL_PATH.exists() or not LABELS_PATH.exists():
        raise RuntimeError(
            f"Model files missing. Need {MODEL_PATH.name} and {LABELS_PATH.name}. Run train_model.py first."
        )

    print(f"[AgriCure] Loading model from {MODEL_PATH}...")
    _model = tf.keras.models.load_model(MODEL_PATH)

    with open(LABELS_PATH, encoding="utf-8") as f:
        _class_names = json.load(f)

    if _model.output_shape[-1] != len(_class_names):
        raise RuntimeError(
            f"Model output shape ({_model.output_shape[-1]}) does not match labels count ({len(_class_names)})."
        )
    print(f"[AgriCure] Model loaded successfully with {len(_class_names)} classes.")
    return _model, _class_names

def get_model():
    if _model is None:
        return load_model_and_labels()
    return _model, _class_names

@app.on_event("startup")
def startup():
    if MODEL_PATH.exists() and LABELS_PATH.exists():
        try:
            get_model()
        except Exception as err:
            print(f"[AgriCure Warning] Could not load model at startup: {err}")
    # Verify records storage connection at startup
    db_ok = is_db_connected()
    if db_ok:
        print(f"[AgriCure] Connected to records storage ({DB_NAME}.{COLLECTION_NAME})")
    else:
        print("[AgriCure] Notice: Records storage offline. Predictions will still work and fallback gracefully.")

@app.get("/")
def home():
    has_model = MODEL_PATH.exists() and LABELS_PATH.exists()
    return {
        "app": "AgriCure - Plant Disease Doctor",
        "status": "online",
        "model_loaded": _model is not None or has_model,
        "classes": len(_class_names) if _class_names else 38,
        "mongodb_connected": is_db_connected(),
        "database": DB_NAME,
        "collection": COLLECTION_NAME
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": _model is not None or (MODEL_PATH.exists() and LABELS_PATH.exists()),
        "mongodb": is_db_connected()
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...), lang: str = Query("en", regex="^(en|gu)$")):
    """
    Diagnoses uploaded leaf image, returns ONLY the single highest predicted outcome
    with comprehensive disease description, symptoms, and detailed treatments,
    and automatically stores the diagnosis into MongoDB Compass (agricure_db.diagnoses).
    """
    try:
        model, class_names = get_model()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Model is not ready: {str(e)}")

    if file.content_type not in {"image/jpeg", "image/png", "image/webp", "image/bmp"}:
        raise HTTPException(status_code=415, detail="Please upload a JPEG, PNG, WEBP, or BMP leaf image.")

    raw = await file.read(MAX_FILE_SIZE + 1)

    if not raw:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(raw) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Image must be 10 MB or smaller.")

    try:
        with Image.open(BytesIO(raw)) as original:
            if original.format not in ALLOWED_FORMATS:
                raise HTTPException(status_code=415, detail="Unsupported image format.")
            original.verify()

        with Image.open(BytesIO(raw)) as original:
            image_rgb = ImageOps.exif_transpose(original).convert("RGB")
            resized = image_rgb.resize(IMG_SIZE)
            array = np.asarray(resized, dtype=np.float32)

            # Generate a lightweight base64 thumbnail (160x160) for MongoDB history view
            thumb = image_rgb.copy()
            thumb.thumbnail((160, 160))
            thumb_buffer = BytesIO()
            thumb.save(thumb_buffer, format="JPEG", quality=75)
            thumbnail_b64 = "data:image/jpeg;base64," + base64.b64encode(thumb_buffer.getvalue()).decode("utf-8")

    except HTTPException:
        raise
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid or corrupted leaf image file.")

    batch = np.expand_dims(array, axis=0)

    # Model inference
    predictions = model.predict(batch, verbose=0)[0]

    # Select ONLY the single highest predicted outcome
    best_index = int(np.argmax(predictions))
    best_disease = class_names[best_index]
    confidence = round(float(predictions[best_index]) * 100, 2)

    # Retrieve in-depth disease description, symptoms, and treatment solutions
    if lang == "gu":
        details = get_disease_details_gujarati(best_disease)
    else:
        details = get_disease_details(best_disease)

    # Prepare document for MongoDB
    diagnosis_record = {
        "filename": file.filename or "leaf_image.jpg",
        "predicted_disease": best_disease,
        "display_name": details["display_name"],
        "crop": details["crop"],
        "condition": details["condition"],
        "confidence": confidence,
        "is_healthy": details["is_healthy"],
        "cause": details["cause"],
        "description": details["description"],
        "symptoms": details["symptoms"],
        "solutions": details["solutions"],
        "image_thumbnail": thumbnail_b64
    }

    # Save to MongoDB Compass database (agricure_db -> diagnoses)
    saved = save_diagnosis(diagnosis_record)

    return {
        "predicted_disease": best_disease,
        "confidence": confidence,
        "display_name": details["display_name"],
        "crop": details["crop"],
        "condition": details["condition"],
        "is_healthy": details["is_healthy"],
        "cause": details["cause"],
        "description": details["description"],
        "symptoms": details["symptoms"],
        "solutions": details["solutions"],
        "history_id": saved.get("id"),
        "timestamp": saved.get("timestamp"),
        "disclaimer": (
            "Predictions are AI estimates based on leaf patterns. "
            "For large-scale agricultural decisions, verify with your local agronomy extension."
        )
    }

@app.get("/history")
def fetch_history(limit: int = Query(50, ge=1, le=200), lang: str = Query("en", regex="^(en|gu)$")):
    """Fetch diagnosis history from MongoDB, optionally translated to Gujarati."""
    records = get_history(limit=limit)

    if lang == "gu" and records:
        translated = []
        for rec in records:
            disease_key = rec.get("predicted_disease", "")
            gu_details = get_disease_details_gujarati(disease_key)
            translated.append({
                **rec,
                "display_name": gu_details.get("display_name", rec.get("display_name", "")),
                "crop":         gu_details.get("crop",         rec.get("crop", "")),
                "condition":    gu_details.get("condition",    rec.get("condition", "")),
                "cause":        gu_details.get("cause",        rec.get("cause", "")),
                "description":  gu_details.get("description",  rec.get("description", "")),
                "symptoms":     gu_details.get("symptoms",     rec.get("symptoms", [])),
                "solutions":    gu_details.get("solutions",    rec.get("solutions", {})),
            })
        records = translated

    return {
        "count": len(records),
        "history": records,
        "mongodb_connected": is_db_connected()
    }

@app.delete("/history/{item_id}")
def delete_history_entry(item_id: str):
    """Delete a single history entry from MongoDB."""
    success = delete_diagnosis(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="History entry not found or could not be deleted.")
    return {"status": "deleted", "id": item_id}

@app.delete("/history")
def clear_history():
    """Clear all diagnosis history from MongoDB."""
    success = clear_all_history()
    return {"status": "cleared", "success": success}

@app.get("/history/stats")
def history_stats():
    """Get database and diagnosis statistics for MongoDB Compass."""
    return get_stats()


# ──────────────────────────────────────────────
# CROP RECOMMENDATION ENGINE
# ──────────────────────────────────────────────

class CropRequest(BaseModel):
    soil_type: str = Field(..., description="Sandy / Loamy / Clay / Silty / Peaty / Saline")
    land_state: str = Field(..., description="Flat / Sloped / Waterlogged / Terraced / Hilly")
    water_availability: str = Field(..., description="Low / Medium / High / Irrigated")
    rainfall_mm: float = Field(..., ge=0, le=5000, description="Annual rainfall in mm")
    temperature_c: float = Field(..., ge=-10, le=55, description="Average temperature in °C")
    ph_level: float = Field(..., ge=0, le=14, description="Soil pH (0–14)")
    nitrogen: str = Field(..., description="Low / Medium / High")
    phosphorus: str = Field(..., description="Low / Medium / High")
    potassium: str = Field(..., description="Low / Medium / High")
    season: str = Field(..., description="Kharif / Rabi / Zaid / Year-round")
    humidity_pct: float = Field(..., ge=0, le=100, description="Relative humidity %")
    lang: Optional[str] = Field("en", description="en or gu")

# Rule-based crop scoring — each crop has ideal ranges & weighted scoring
CROP_RULES = [
    {
        "name": "Rice",  "gu": "ચોખા",  "emoji": "🌾",
        "min_rain": 1000, "max_rain": 2500, "min_temp": 20, "max_temp": 38,
        "min_ph": 5.5, "max_ph": 7.0,
        "soils": ["Loamy", "Clay", "Silty"], "water": ["High", "Irrigated"],
        "land": ["Flat", "Waterlogged"], "seasons": ["Kharif", "Year-round"],
        "N": "High", "desc_en": "Thrives in waterlogged, warm climates with heavy rainfall.",
        "desc_gu": "ભારે વરસાદ અને ગરમ વાતાવરણમાં ઉગે છે."
    },
    {
        "name": "Wheat",  "gu": "ઘઉં",  "emoji": "🌾",
        "min_rain": 250, "max_rain": 750, "min_temp": 10, "max_temp": 25,
        "min_ph": 6.0, "max_ph": 7.5,
        "soils": ["Loamy", "Clay", "Silty"], "water": ["Medium", "Irrigated"],
        "land": ["Flat", "Terraced"], "seasons": ["Rabi"],
        "N": "High", "desc_en": "Best in cool winters with moderate rainfall or irrigation.",
        "desc_gu": "ઠંડા શિયાળા અને મધ્યમ સિંચાઈ માટે ઉત્તમ."
    },
    {
        "name": "Maize",  "gu": "મકાઈ",  "emoji": "🌽",
        "min_rain": 500, "max_rain": 1000, "min_temp": 18, "max_temp": 35,
        "min_ph": 5.8, "max_ph": 7.0,
        "soils": ["Loamy", "Sandy", "Silty"], "water": ["Medium", "High", "Irrigated"],
        "land": ["Flat", "Sloped", "Terraced"], "seasons": ["Kharif", "Zaid"],
        "N": "High", "desc_en": "Versatile warm-season crop; needs good drainage.",
        "desc_gu": "ગરમ ઋતુ માટે બહુ ઉપયોગી; સારા નિકાલ-વ્યવસ્થાની જરૂર."
    },
    {
        "name": "Cotton",  "gu": "કપાસ",  "emoji": "🪴",
        "min_rain": 500, "max_rain": 1200, "min_temp": 21, "max_temp": 40,
        "min_ph": 6.0, "max_ph": 8.0,
        "soils": ["Loamy", "Clay", "Silty"], "water": ["Medium", "Irrigated"],
        "land": ["Flat", "Sloped"], "seasons": ["Kharif"],
        "N": "Medium", "desc_en": "Prefers long frost-free growing periods and deep soils.",
        "desc_gu": "ઊંડી માટી અને લાંબો ઠંડ-રહિત સમય જોઈએ."
    },
    {
        "name": "Sugarcane",  "gu": "શેરડી",  "emoji": "🎋",
        "min_rain": 1200, "max_rain": 2500, "min_temp": 20, "max_temp": 38,
        "min_ph": 6.0, "max_ph": 7.5,
        "soils": ["Loamy", "Clay"], "water": ["High", "Irrigated"],
        "land": ["Flat", "Waterlogged"], "seasons": ["Kharif", "Year-round"],
        "N": "High", "desc_en": "Thrives in tropical/subtropical climates with high water.",
        "desc_gu": "ઉષ્ણ/અર્ધ-ઉષ્ણ વાતાવરણ અને ઊંચા પાણીની જરૂર."
    },
    {
        "name": "Groundnut",  "gu": "મગફળી",  "emoji": "🥜",
        "min_rain": 400, "max_rain": 900, "min_temp": 20, "max_temp": 35,
        "min_ph": 5.5, "max_ph": 7.0,
        "soils": ["Sandy", "Loamy"], "water": ["Low", "Medium"],
        "land": ["Flat", "Sloped"], "seasons": ["Kharif"],
        "N": "Low", "desc_en": "Fixes nitrogen; suited for light sandy soils with low water.",
        "desc_gu": "નાઇટ્રોજન ઉત્પન્ન; હળવી, રેતાળ, ઓછા-પાણી ભૂમિ."
    },
    {
        "name": "Soybean",  "gu": "સોયાબીન",  "emoji": "🌱",
        "min_rain": 600, "max_rain": 1200, "min_temp": 15, "max_temp": 32,
        "min_ph": 6.0, "max_ph": 7.5,
        "soils": ["Loamy", "Clay", "Silty"], "water": ["Medium", "High"],
        "land": ["Flat", "Sloped"], "seasons": ["Kharif"],
        "N": "Low", "desc_en": "Nitrogen-fixing legume; needs warm summers and adequate moisture.",
        "desc_gu": "ઉનાળામાં ઉગે; જમીનમાં નાઇટ્રોજન ઉમેરે."
    },
    {
        "name": "Tomato",  "gu": "ટામેટા",  "emoji": "🍅",
        "min_rain": 400, "max_rain": 800, "min_temp": 15, "max_temp": 30,
        "min_ph": 5.5, "max_ph": 7.5,
        "soils": ["Loamy", "Sandy", "Silty"], "water": ["Medium", "Irrigated"],
        "land": ["Flat", "Terraced", "Sloped"], "seasons": ["Rabi", "Zaid", "Year-round"],
        "N": "Medium", "desc_en": "High-value vegetable; needs well-drained, fertile soil.",
        "desc_gu": "ઊંચી કિંમત; સારી નિકાલ-ભૂમિ અને ફળદ્રુપ જમીનની જરૂર."
    },
    {
        "name": "Potato",  "gu": "બટાટા",  "emoji": "🥔",
        "min_rain": 400, "max_rain": 700, "min_temp": 8, "max_temp": 22,
        "min_ph": 5.0, "max_ph": 6.5,
        "soils": ["Sandy", "Loamy"], "water": ["Medium", "Irrigated"],
        "land": ["Flat", "Sloped", "Terraced"], "seasons": ["Rabi"],
        "N": "High", "desc_en": "Prefers cool climate and loose, well-drained acidic soil.",
        "desc_gu": "ઠંડા વાતાવરણ; છૂટી, સારી-નિકાળ, અમ્લ-ભૂમિ."
    },
    {
        "name": "Onion",  "gu": "ડુંગળી",  "emoji": "🧅",
        "min_rain": 300, "max_rain": 700, "min_temp": 10, "max_temp": 30,
        "min_ph": 6.0, "max_ph": 7.5,
        "soils": ["Loamy", "Sandy", "Silty"], "water": ["Low", "Medium", "Irrigated"],
        "land": ["Flat", "Sloped"], "seasons": ["Rabi", "Kharif"],
        "N": "Medium", "desc_en": "Hardy bulb crop; tolerates dry spells, needs good drainage.",
        "desc_gu": "સૂકા સ્વભાવ; ઊંચી નિકાળ-ક્ષમતા."
    },
    {
        "name": "Chickpea",  "gu": "ચણા",  "emoji": "🫘",
        "min_rain": 250, "max_rain": 600, "min_temp": 10, "max_temp": 28,
        "min_ph": 5.5, "max_ph": 7.5,
        "soils": ["Sandy", "Loamy"], "water": ["Low", "Medium"],
        "land": ["Flat", "Sloped"], "seasons": ["Rabi"],
        "N": "Low", "desc_en": "Drought-tolerant legume ideal for dry Rabi season.",
        "desc_gu": "દુષ્કાળ-સહિષ્ણુ; સૂકી રવિ ઋતુ."
    },
    {
        "name": "Millet (Bajra)",  "gu": "બાજરો",  "emoji": "🌾",
        "min_rain": 150, "max_rain": 600, "min_temp": 25, "max_temp": 42,
        "min_ph": 5.5, "max_ph": 7.5,
        "soils": ["Sandy", "Loamy"], "water": ["Low", "Medium"],
        "land": ["Flat", "Sloped", "Hilly"], "seasons": ["Kharif"],
        "N": "Low", "desc_en": "Highly drought-resistant; excellent for arid and semi-arid zones.",
        "desc_gu": "અત્યંત દુષ્કાળ-સહિષ્ણુ; શુષ્ક ક્ષેત્ર."
    },
    {
        "name": "Banana",  "gu": "કેળ",  "emoji": "🍌",
        "min_rain": 1200, "max_rain": 2500, "min_temp": 20, "max_temp": 38,
        "min_ph": 5.5, "max_ph": 7.0,
        "soils": ["Loamy", "Clay", "Silty"], "water": ["High", "Irrigated"],
        "land": ["Flat", "Terraced"], "seasons": ["Year-round"],
        "N": "High", "desc_en": "Tropical fruit; needs abundant water and warm temperature.",
        "desc_gu": "ઉષ્ણ; ભારે પાણી અને ગર્મ તાપમાન."
    },
    {
        "name": "Mustard",  "gu": "રાઈ",  "emoji": "🌼",
        "min_rain": 250, "max_rain": 600, "min_temp": 5, "max_temp": 22,
        "min_ph": 6.0, "max_ph": 7.5,
        "soils": ["Loamy", "Sandy", "Clay"], "water": ["Low", "Medium"],
        "land": ["Flat", "Sloped"], "seasons": ["Rabi"],
        "N": "Medium", "desc_en": "Cool-season oilseed; tolerates frost and dry conditions.",
        "desc_gu": "ઠંડ-ઋતુ તેલ-ઉત્પાદક; ઠંડ-સહિષ્ણુ."
    },
    {
        "name": "Sunflower",  "gu": "સૂર્યમુખી",  "emoji": "🌻",
        "min_rain": 400, "max_rain": 800, "min_temp": 18, "max_temp": 35,
        "min_ph": 6.0, "max_ph": 7.5,
        "soils": ["Loamy", "Sandy", "Silty"], "water": ["Medium"],
        "land": ["Flat", "Sloped"], "seasons": ["Kharif", "Rabi"],
        "N": "Medium", "desc_en": "Versatile oilseed crop; adaptable to many soils.",
        "desc_gu": "વૈવિધ્યપૂર્ણ; ઘણી ભૂમિ-પ્રકારો."
    },
]

def _score_crop(crop: dict, req: CropRequest) -> float:
    score = 0.0
    if req.rainfall_mm >= crop["min_rain"] and req.rainfall_mm <= crop["max_rain"]:
        score += 2.0
    elif abs(req.rainfall_mm - (crop["min_rain"] + crop["max_rain"]) / 2) < 500:
        score += 0.5
    if req.temperature_c >= crop["min_temp"] and req.temperature_c <= crop["max_temp"]:
        score += 2.0
    elif abs(req.temperature_c - (crop["min_temp"] + crop["max_temp"]) / 2) < 8:
        score += 0.5
    if crop["min_ph"] <= req.ph_level <= crop["max_ph"]:
        score += 1.5
    if req.soil_type in crop["soils"]:
        score += 1.5
    if req.water_availability in crop["water"]:
        score += 1.5
    if req.land_state in crop["land"]:
        score += 1.0
    if req.season in crop["seasons"]:
        score += 2.0
    if req.nitrogen == crop["N"]:
        score += 0.5
    return score

@app.post("/crop-recommend")
def crop_recommend(req: CropRequest):
    """
    Returns top crop recommendations based on soil, climate, and farm conditions.
    Accepts multiple agronomic factors and scores each crop using a weighted rule engine.
    """
    scored = []
    for crop in CROP_RULES:
        s = _score_crop(crop, req)
        if s > 0:
            scored.append({
                "name": crop["gu"] if req.lang == "gu" else crop["name"],
                "name_en": crop["name"],
                "emoji": crop["emoji"],
                "score": round(s, 2),
                "max_score": 12.5,
                "suitability_pct": round(min(100, (s / 12.5) * 100), 1),
                "description": crop["desc_gu"] if req.lang == "gu" else crop["desc_en"],
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[:5]

    return {
        "recommendations": top,
        "factors_used": {
            "soil_type": req.soil_type,
            "land_state": req.land_state,
            "water_availability": req.water_availability,
            "rainfall_mm": req.rainfall_mm,
            "temperature_c": req.temperature_c,
            "ph_level": req.ph_level,
            "season": req.season,
        },
        "disclaimer": (
            "Recommendations are rule-based estimates. "
            "Verify with your local agriculture extension officer before planting."
        )
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
