from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["electronics_store"]

users_col = db["users"]
products_col = db["products"]
orders_col = db["orders"]
reviews_col = db["reviews"]
categories_col = db["categories"]