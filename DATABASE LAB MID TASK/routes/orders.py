from fastapi import APIRouter, HTTPException
from database import orders_col
from bson import ObjectId
from bson.json_util import dumps
import json

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/{order_id}")
def get_order(order_id: str):
    try:
        obj_id = ObjectId(order_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid order ID format")

    order = orders_col.find_one({"_id": obj_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return json.loads(dumps(order))