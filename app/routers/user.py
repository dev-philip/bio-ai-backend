from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# In-memory user store (for demo purposes)
fake_users_db = [
    {"id": 1, "name": "Philip Awobusuyi", "email": "philip@example.com"},
    {"id": 2, "name": "Jane Doe", "email": "jane@example.com"},
]

class UserCreate(BaseModel):
    name: str
    email: str

# GET /users/
@router.get("/")
def get_users():
    return {"users": fake_users_db}

# POST /users/
@router.post("/")
def create_user(user: UserCreate):
    new_user = {
        "id": len(fake_users_db) + 1,
        "name": user.name,
        "email": user.email
    }
    fake_users_db.append(new_user)
    return {"message": "User created successfully", "user": new_user}

# GET /users/{user_id}
@router.get("/{user_id}")
def get_user_by_id(user_id: int):
    user = next((u for u in fake_users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}
