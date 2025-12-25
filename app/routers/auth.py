from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from app.models.schemas import UserCreate, Token
from app.services.auth_service import authenticate_user, create_user, create_user_token
from app.utils.dependencies import get_current_user

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    user_dict = user.model_dump()
    user_dict["created_at"] = datetime.utcnow()
    user_dict["followers"] = []
    user_dict["following"] = []
    
    created_user = await create_user(user_dict)
    access_token = create_user_token(str(created_user["_id"]))
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(created_user["_id"]),
            "name": created_user["name"],
            "email": created_user["email"]
        }
    }

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_user_token(str(user["_id"]))
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
    }

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "age": current_user["age"],
        "gender": current_user["gender"],
        "height": current_user["height"],
        "weight": current_user["weight"],
        "activity_level": current_user["activity_level"],
        "goal": current_user["goal"]
    }