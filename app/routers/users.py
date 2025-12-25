from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import UserUpdate
from app.utils.dependencies import get_current_user
from app.database import get_database
from bson import ObjectId
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "age": current_user["age"],
        "gender": current_user["gender"],
        "height": current_user["height"],
        "weight": current_user["weight"],
        "activity_level": current_user["activity_level"],
        "goal": current_user["goal"],
        "bio": current_user.get("bio", ""),
        "created_at": current_user["created_at"]
    }

@router.put("/profile")
async def update_profile(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    
    update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
    
    if update_data:
        await db.users.update_one(
            {"_id": ObjectId(current_user["id"])},
            {"$set": update_data}
        )
    
    updated_user = await db.users.find_one({"_id": ObjectId(current_user["id"])})
    updated_user["id"] = str(updated_user["_id"])
    
    return updated_user

@router.get("/stats")
async def get_user_stats(current_user: dict = Depends(get_current_user)):
    db = get_database()
    user_id = current_user["id"]
    
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    
    workouts_today = await db.workouts.count_documents({
        "user_id": user_id,
        "date": {"$gte": today, "$lt": tomorrow}
    })
    
    meals_today = await db.meals.count_documents({
        "user_id": user_id,
        "date": {"$gte": today, "$lt": tomorrow}
    })
    
    meals_cursor = db.meals.find({
        "user_id": user_id,
        "date": {"$gte": today, "$lt": tomorrow}
    })
    meals = await meals_cursor.to_list(length=100)
    calories_consumed = sum(meal.get("total_calories", 0) for meal in meals)
    
    workouts_cursor = db.workouts.find({
        "user_id": user_id,
        "date": {"$gte": today, "$lt": tomorrow}
    })
    workouts = await workouts_cursor.to_list(length=100)
    calories_burned = sum(workout.get("calories_burned", 0) for workout in workouts)
    
    return {
        "workouts_today": workouts_today,
        "meals_today": meals_today,
        "calories_consumed": calories_consumed,
        "calories_burned": calories_burned
    }