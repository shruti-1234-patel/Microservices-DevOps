from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
app = FastAPI(title="Order Service")

USER_SERVICE_URL = os.getenv(
    "USER_SERVICE_URL",
    "http://localhost:8001"
)

orders = []


class Order(BaseModel):
    user_id: int
    product: str
    quantity: int


@app.get("/")
def home():
    return {
        "service": "Order Service",
        "message": "Order Service is running"
    }


@app.post("/orders")
def create_order(order: Order):

    response = requests.get(
        f"{USER_SERVICE_URL}/users/{order.user_id}"
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="User does not exist"
        )

    user = response.json()

    new_order = {
        "order_id": len(orders) + 1,
        "user_id": order.user_id,
        "user_name": user["name"],
        "product": order.product,
        "quantity": order.quantity
    }

    orders.append(new_order)

    return new_order


@app.get("/orders")
def get_orders():
    return orders