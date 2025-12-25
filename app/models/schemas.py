from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Literal
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int
    gender: Literal["male", "female", "other"]
    height: float
    weight: float
    activity_level: Literal["sedentary", "light", "moderate", "active", "very_active"] = "moderate"
    goal: Literal["lose_weight", "maintain", "gain_muscle"] = "maintain"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    activity_level: Optional[str] = None
    goal: Optional[str] = None
    bio: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class Exercise(BaseModel):
    name: str
    sets: int
    reps: int
    weight: Optional[float] = None
    duration: Optional[int] = None

class WorkoutCreate(BaseModel):
    title: str
    type: Literal["strength", "cardio", "flexibility", "sports", "other"]
    exercises: List[Exercise] = []
    duration: int
    calories_burned: Optional[int] = 0
    notes: Optional[str] = None
    date: Optional[datetime] = None

class WorkoutUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    exercises: Optional[List[Exercise]] = None
    duration: Optional[int] = None
    calories_burned: Optional[int] = None
    notes: Optional[str] = None

class FoodItem(BaseModel):
    name: str
    quantity: float
    unit: str
    calories: int
    protein: Optional[float] = 0
    carbs: Optional[float] = 0
    fats: Optional[float] = 0

class MealCreate(BaseModel):
    type: Literal["breakfast", "lunch", "dinner", "snack"]
    foods: List[FoodItem]
    notes: Optional[str] = None
    date: Optional[datetime] = None

class MealUpdate(BaseModel):
    type: Optional[str] = None
    foods: Optional[List[FoodItem]] = None
    notes: Optional[str] = None

class PostCreate(BaseModel):
    content: str
    type: Literal["workout", "meal", "achievement", "general"] = "general"

class AIUserData(BaseModel):
    age: int
    gender: str
    height: float
    weight: float
    activity_level: str
    goal: str

class DietRecommendation(BaseModel):
    daily_calories: int
    protein_grams: int
    carbs_grams: int
    fats_grams: int
    meals_breakdown: dict
    recommendations: List[str]

class WorkoutPlan(BaseModel):
    plan_name: str
    duration_weeks: int
    weekly_schedule: List[dict]
    tips: List[str]

class CalorieResponse(BaseModel):
    bmr: float
    tdee: float
    recommended_calories: dict
