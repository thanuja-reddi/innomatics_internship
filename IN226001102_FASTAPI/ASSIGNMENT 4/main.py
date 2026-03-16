from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="FastAPI Shopping Cart Assignment")

# ---------------------------
# In-memory data
# ---------------------------
products = {
    1: {"name": "Wireless Mouse", "price": 499, "stock": 10},
    2: {"name": "Notebook", "price": 99, "stock": 20},
    3: {"name": "USB Hub", "price": 299, "stock": 0},
    4: {"name": "Pen Set", "price": 49, "stock": 30},
}

cart = {}
orders = []
order_counter = 1


# ---------------------------
# Request models
# ---------------------------
class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int


class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str


# ---------------------------
# Helper functions
# ---------------------------
def build_cart_item(product_id: int, quantity: int):
    product = products[product_id]
    return {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": product["price"] * quantity,
    }


# ---------------------------
# Routes
# ---------------------------
@app.get("/")
def home():
    return {"message": "FastAPI Shopping Cart API is running"}


@app.post("/cart/add")
def add_to_cart(data: AddToCartRequest):
    global cart

    if data.product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    if data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    product = products[data.product_id]

    if product["stock"] == 0:
        raise HTTPException(status_code=400, detail=f'{product["name"]} is out of stock')

    current_qty = cart.get(data.product_id, 0)
    new_qty = current_qty + data.quantity

    if new_qty > product["stock"]:
        raise HTTPException(
            status_code=400,
            detail=f"Only {product['stock']} units of {product['name']} available",
        )

    cart[data.product_id] = new_qty
    cart_item = build_cart_item(data.product_id, new_qty)

    if current_qty == 0:
        return {
            "message": "Added to cart",
            "cart_item": cart_item,
        }
    else:
        return {
            "message": "Cart updated",
            "cart_item": cart_item,
        }


@app.get("/cart")
def view_cart():
    if not cart:
        return {"message": "Cart is empty"}

    items = []
    grand_total = 0

    for product_id, quantity in cart.items():
        item = build_cart_item(product_id, quantity)
        items.append(item)
        grand_total += item["subtotal"]

    return {
        "items": items,
        "item_count": len(items),
        "grand_total": grand_total,
    }


@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: int):
    if product_id not in cart:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    removed_item = build_cart_item(product_id, cart[product_id])
    del cart[product_id]

    return {
        "message": "Item removed from cart",
        "removed_item": removed_item,
    }


@app.post("/cart/checkout")
def checkout(data: CheckoutRequest):
    global cart, orders, order_counter

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty — add items first")

    placed_orders = []
    grand_total = 0

    for product_id, quantity in cart.items():
        product = products[product_id]
        total_price = product["price"] * quantity

        order = {
            "order_id": order_counter,
            "customer_name": data.customer_name,
            "delivery_address": data.delivery_address,
            "product_id": product_id,
            "product": product["name"],
            "quantity": quantity,
            "unit_price": product["price"],
            "total_price": total_price,
        }

        orders.append(order)
        placed_orders.append(order)
        grand_total += total_price
        order_counter += 1

    cart = {}

    return {
        "message": "Checkout successful",
        "orders_placed": placed_orders,
        "grand_total": grand_total,
    }


@app.get("/orders")
def get_orders():
    return {
        "orders": orders,
        "total_orders": len(orders),
    }
