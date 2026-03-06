from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 800, "in_stock": True},
    {"id": 2, "name": "Phone", "category": "Electronics", "price": 500, "in_stock": False},
    {"id": 3, "name": "Chair", "category": "Furniture", "price": 120, "in_stock": True},
    {"id": 4, "name": "Desk", "category": "Furniture", "price": 300, "in_stock": True},
    {"id": 5, "name": "Headphones", "category": "Electronics", "price": 150, "in_stock": True},
]

@app.get("/")
def home():
    return {"message": "Welcome to the Product Store API"}

@app.get("/products")
def get_products():
    return products

@app.get("/products/category/{category}")
def get_products_by_category(category: str):
    result = [p for p in products if p["category"].lower() == category.lower()]
    return result

@app.get("/products/instock")
def get_instock_products():
    result = [p for p in products if p["in_stock"]]
    return result

@app.get("/store/summary")
def store_summary():
    total_products = len(products)
    total_value = sum(p["price"] for p in products)
    return {
        "total_products": total_products,
        "total_value": total_value
    }

@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    result = [p for p in products if keyword.lower() in p["name"].lower()]
    return result