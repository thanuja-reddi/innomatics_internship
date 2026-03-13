from fastapi import FastAPI, Response, status, Query

app = FastAPI()

# Initial product data
products = [
    {"id": 1, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 2, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

# Helper function
def find_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    return None


@app.get("/")
def home():
    return {"message": "FastAPI Product Inventory API"}


# Get all products
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }

# Assignment Question 5 – Product Audit
@app.get("/products/audit")
def product_audit():

    in_stock_products = [p for p in products if p["in_stock"]]
    out_of_stock_products = [p for p in products if not p["in_stock"]]

    total_stock_value = sum(p["price"] * 10 for p in in_stock_products)

    most_expensive = max(products, key=lambda p: p["price"])

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock_products),
        "out_of_stock_names": [p["name"] for p in out_of_stock_products],
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }
# Get single product
@app.get("/products/{product_id}")
def get_product(product_id: int, response: Response):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    return product


# Add new product
@app.post("/products")
def add_product(product: dict, response: Response):

    # duplicate check
    for p in products:
        if p["name"] == product["name"]:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": "Product already exists"}

    new_id = max(p["id"] for p in products) + 1
    product["id"] = new_id

    products.append(product)

    response.status_code = status.HTTP_201_CREATED

    return {
        "message": "Product added successfully",
        "product": product
    }


# Update product
@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    price: int = None,
    in_stock: bool = None,
    response: Response = None
):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    if price is not None:
        product["price"] = price

    if in_stock is not None:
        product["in_stock"] = in_stock

    return {
        "message": "Product updated successfully",
        "product": product
    }


# Delete product
@app.delete("/products/{product_id}")
def delete_product(product_id: int, response: Response):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    products.remove(product)

    return {
        "message": f"Product '{product['name']}' deleted"
    }


