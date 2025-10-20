from fastapi import APIRouter
from database import reviews_col
from bson.json_util import dumps
import json

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("/")
def get_all_reviews():
    reviews = list(reviews_col.find())
    return json.loads(dumps(reviews))