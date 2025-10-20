import json
from database import products_col, users_col, orders_col, reviews_col, categories_col
from bson import ObjectId
from datetime import datetime


def _convert_extended(obj):
    """Recursively convert extended JSON markers to Python/Mongo types.

    - {"$oid": "..."} -> ObjectId(...)
    - {"$date": "..."} -> datetime
    """
    if isinstance(obj, dict):
        # exact $oid object
        if "$oid" in obj and len(obj) == 1:
            return ObjectId(obj["$oid"])
        if "$date" in obj and len(obj) == 1:
            s = obj["$date"]
            try:
                return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                try:
                    # fallback for ISO strings
                    return datetime.fromisoformat(s.replace('Z', '+00:00'))
                except Exception:
                    return s
        return {k: _convert_extended(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_convert_extended(v) for v in obj]
    return obj


def seed_database():
    products_col.delete_many({})
    users_col.delete_many({})
    orders_col.delete_many({})
    reviews_col.delete_many({})
    categories_col.delete_many({})
    
    products_col.create_index([("name", "text"), ("description", "text")])
    
    with open('categories.json') as f:
        data = json.load(f)
        categories_col.insert_many(_convert_extended(data))
    
    with open('product.json') as f:
        data = json.load(f)
        products_col.insert_many(_convert_extended(data))
    
    with open('users.json') as f:
        data = json.load(f)
        users_col.insert_many(_convert_extended(data))
    
    with open('orders.json') as f:
        data = json.load(f)
        orders_col.insert_many(_convert_extended(data))
    
    with open('reviews.json') as f:
        data = json.load(f)
        reviews_col.insert_many(_convert_extended(data))
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()