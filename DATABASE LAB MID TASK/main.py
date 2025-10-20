from fastapi import FastAPI
from routes import products, users, orders, reviews

app = FastAPI(title="E-Commerce Marketplace API")

app.include_router(products.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(reviews.router)

@app.get("/")
def home():
    return {"message": "E-commerce API is running successfully."}