from fastapi import APIRouter, HTTPException
from database import users_col, orders_col
from bson import ObjectId
from bson.json_util import dumps
import json

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}/orders")
def get_user_orders(user_id: str):
    try:
        obj_id = ObjectId(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    orders = list(orders_col.find({"user_id": obj_id}))
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")

    return json.loads(dumps({"user_orders": orders}))