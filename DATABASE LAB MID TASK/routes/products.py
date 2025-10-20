from fastapi import APIRouter, Query
from database import products_col, reviews_col
from bson import ObjectId
from difflib import SequenceMatcher
from bson.json_util import dumps
import json

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/search")
def search_products(query: str = Query(...)):
    products = list(products_col.find({"$text": {"$search": query}}))
    for p in products:
        p["_id"] = str(p["_id"])
    return {"results": products}

@router.get("/similarity")
def similarity_search(query: str = Query(...)):
    all_products = list(products_col.find())
    results = []

    for prod in all_products:
        score = SequenceMatcher(None, query.lower(), prod["name"].lower()).ratio()
        if score > 0.4:
            prod["_id"] = str(prod["_id"])
            prod["similarity_score"] = round(score, 2)
            results.append(prod)

    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    return {"results": results[:10]}

@router.get("/hybrid")
def hybrid_search(query: str = Query(...), budget: float = Query(1000.0)):
    all_products = list(products_col.find())
    results = []

    for prod in all_products:
        sim = SequenceMatcher(None, query.lower(), prod["name"].lower()).ratio()
        price_score = 1 - abs(prod["price"] - budget) / budget
        pop_score = min(prod.get("popularity", 0) / 500, 1)

        hybrid_score = (0.4 * sim) + (0.4 * price_score) + (0.2 * pop_score)
        prod["_id"] = str(prod["_id"])
        prod["hybrid_score"] = round(hybrid_score, 2)
        results.append(prod)

    results.sort(key=lambda x: x["hybrid_score"], reverse=True)
    return {"results": results[:10]}

@router.get("/{product_id}/reviews")
def get_product_reviews(product_id: str):
    try:
        obj_id = ObjectId(product_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid product ID format")
    reviews = list(reviews_col.find({"product_id": obj_id}))
    return json.loads(dumps(reviews))