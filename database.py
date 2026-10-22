"""
MongoDB connection and history management for AgriCure.
Compatible with MongoDB Compass (mongodb://127.0.0.1:27017).
Database: agricure_db
Collection: diagnoses
"""

import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError

MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
DB_NAME = "agricure_db"
COLLECTION_NAME = "diagnoses"

_client: Optional[MongoClient] = None
_collection = None

def get_collection():
    global _client, _collection
    if _collection is not None:
        return _collection
    try:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        # Test connection
        _client.admin.command("ping")
        db = _client[DB_NAME]
        _collection = db[COLLECTION_NAME]
        # Create an index on timestamp descending for fast history lookups
        _collection.create_index([("timestamp", -1)])
        print(f"[AgriCure DB] Connected to MongoDB ({MONGO_URI} -> {DB_NAME}.{COLLECTION_NAME})")
        return _collection
    except Exception as err:
        print(f"[AgriCure DB Warning] MongoDB not available: {err}")
        return None

def is_db_connected() -> bool:
    try:
        col = get_collection()
        return col is not None
    except Exception:
        return False

def save_diagnosis(data: Dict[str, Any]) -> Dict[str, Any]:
    """Save a plant diagnosis record to MongoDB."""
    col = get_collection()
    record = dict(data)
    record["timestamp"] = datetime.now(timezone.utc).isoformat()

    if col is not None:
        try:
            res = col.insert_one(record)
            record["id"] = str(res.inserted_id)
            if "_id" in record:
                del record["_id"]
            return record
        except PyMongoError as e:
            print(f"[AgriCure DB Error] Failed to insert record: {e}")

    # Fallback ID if DB is temporarily disconnected
    record["id"] = f"local_{int(datetime.now().timestamp() * 1000)}"
    return record

def get_history(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieve recent diagnoses from MongoDB."""
    col = get_collection()
    if col is None:
        return []

    try:
        cursor = col.find({}, {"_id": 1, "timestamp": 1, "predicted_disease": 1, "display_name": 1, "crop": 1, "condition": 1, "confidence": 1, "is_healthy": 1, "description": 1, "solutions": 1, "symptoms": 1, "cause": 1, "image_thumbnail": 1}).sort("timestamp", -1).limit(limit)
        results = []
        for doc in cursor:
            doc["id"] = str(doc.pop("_id"))
            results.append(doc)
        return results
    except Exception as err:
        print(f"[AgriCure DB Error] Error fetching history: {err}")
        return []

def delete_diagnosis(diagnosis_id: str) -> bool:
    """Delete a specific diagnosis from MongoDB by ObjectId."""
    col = get_collection()
    if col is None:
        return False

    try:
        res = col.delete_one({"_id": ObjectId(diagnosis_id)})
        return res.deleted_count > 0
    except Exception as err:
        print(f"[AgriCure DB Error] Error deleting {diagnosis_id}: {err}")
        return False

def clear_all_history() -> bool:
    """Clear all records from the diagnoses collection."""
    col = get_collection()
    if col is None:
        return False

    try:
        col.delete_many({})
        return True
    except Exception as err:
        print(f"[AgriCure DB Error] Error clearing history: {err}")
        return False

def get_stats() -> Dict[str, Any]:
    """Get high level statistics for the history view."""
    col = get_collection()
    if col is None:
        return {"total": 0, "connected": False}

    try:
        total = col.count_documents({})
        healthy = col.count_documents({"is_healthy": True})
        diseased = total - healthy
        return {
            "total": total,
            "healthy": healthy,
            "diseased": diseased,
            "connected": True,
            "database": DB_NAME,
            "collection": COLLECTION_NAME,
            "uri": MONGO_URI
        }
    except Exception as err:
        return {"total": 0, "connected": False, "error": str(err)}
