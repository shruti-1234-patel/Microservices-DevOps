from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="User Service")

users = {
    1: {
        "id": 1,
        "name": "Shruti",
        "email": "shruti@gmail.com"
    },
    2: {
        "id": 2,
        "name": "Priya",
        "email": "priya@gmail.com"
    }
}


class User(BaseModel):
    name: str
    email: str


@app.get("/")
def home():
    return {
        "service": "User Service",
        "message": "User Service is running"
    }


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return users[user_id]


@app.post("/users")
def create_user(user: User):
    new_id = max(users.keys()) + 1

    users[new_id] = {
        "id": new_id,
        "name": user.name,
        "email": user.email
    }

    return users[new_id]