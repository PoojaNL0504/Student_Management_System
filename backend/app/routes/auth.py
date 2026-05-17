from app.crud import authenticate_user, create_user
from app.auth_utils import create_access_token
from fastapi import APIRouter

router = APIRouter()


@router.post("/signup")
def signup(username: str, password: str):
    user = create_user(username, password)
    print("Creating user:", username)
    if not user:
        return {"message": "Signup failed"}

    return {"message": "User created"}



@router.post("/login")
def login(username: str, password: str):
    user = authenticate_user(username, password)
    print("LOGIN USER:", user)
    if not user:
        return {"message": "Invalid credentials"}

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }