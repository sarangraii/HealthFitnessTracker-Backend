from fastapi import APIRouter, Depends
from app.models.schemas import AIUserData, DietRecommendation, WorkoutPlan, CalorieResponse
from app.services.diet_recommender import DietRecommender
from app.services.workout_planner import WorkoutPlanner
from app.services.calorie_predictor import CaloriePredictor
from app.utils.dependencies import get_current_user

router = APIRouter()

diet_recommender = DietRecommender()
workout_planner = WorkoutPlanner()
calorie_predictor = CaloriePredictor()

@router.post("/diet-recommendations", response_model=DietRecommendation)
async def get_diet_recommendations(
    user_data: AIUserData,
    current_user: dict = Depends(get_current_user)
):
    # Calculate BMR and TDEE
    bmr = diet_recommender.calculate_bmr(
        user_data.age,
        user_data.gender,
        user_data.height,
        user_data.weight
    )
    
    tdee = diet_recommender.calculate_tdee(bmr, user_data.activity_level)
    
    # Get calorie target based on goal
    daily_calories = diet_recommender.get_calorie_target(tdee, user_data.goal)
    
    # Calculate macros
    macros = diet_recommender.calculate_macros(daily_calories, user_data.goal)
    
    # Create meal breakdown
    meals_breakdown = diet_recommender.create_meal_breakdown(daily_calories)
    
    # Get recommendations
    recommendations = diet_recommender.get_recommendations(user_data.goal)
    
    return DietRecommendation(
        daily_calories=daily_calories,
        protein_grams=macros["protein"],
        carbs_grams=macros["carbs"],
        fats_grams=macros["fats"],
        meals_breakdown=meals_breakdown,
        recommendations=recommendations
    )

@router.post("/workout-plan", response_model=WorkoutPlan)
async def get_workout_plan(
    user_data: AIUserData,
    current_user: dict = Depends(get_current_user)
):
    # Determine days per week based on activity level
    days_map = {
        "sedentary": 3,
        "light": 3,
        "moderate": 4,
        "active": 5,
        "very_active": 6
    }
    
    days_per_week = days_map.get(user_data.activity_level, 4)
    
    # Generate plan
    plan = workout_planner.generate_plan(
        user_data.goal,
        user_data.activity_level,
        days_per_week
    )
    
    # Add exercise details to each day
    for day in plan["weekly_schedule"]:
        if day["type"] == "strength":
            day["exercises"] = workout_planner.get_exercise_details("strength", "chest")
        elif day["type"] == "cardio":
            day["exercises"] = workout_planner.get_exercise_details("cardio")
        else:
            day["exercises"] = []
    
    return WorkoutPlan(**plan)

@router.post("/predict-calories", response_model=CalorieResponse)
async def predict_calories(
    user_data: AIUserData,
    current_user: dict = Depends(get_current_user)
):
    result = calorie_predictor.predict(
        user_data.age,
        user_data.gender,
        user_data.height,
        user_data.weight,
        user_data.activity_level
    )
    return CalorieResponse(**result)

@router.get("/food-database")
async def get_food_database(current_user: dict = Depends(get_current_user)):
    foods = [
        {"name": "Chicken Breast", "calories": 165, "protein": 31, "carbs": 0, "fats": 3.6, "serving": "100g"},
        {"name": "Brown Rice", "calories": 112, "protein": 2.6, "carbs": 24, "fats": 0.9, "serving": "100g"},
        {"name": "Broccoli", "calories": 55, "protein": 3.7, "carbs": 11, "fats": 0.6, "serving": "100g"},
        {"name": "Salmon", "calories": 208, "protein": 20, "carbs": 0, "fats": 13, "serving": "100g"},
        {"name": "Eggs", "calories": 155, "protein": 13, "carbs": 1.1, "fats": 11, "serving": "2 large"},
        {"name": "Oatmeal", "calories": 71, "protein": 2.5, "carbs": 12, "fats": 1.5, "serving": "100g"},
        {"name": "Banana", "calories": 105, "protein": 1.3, "carbs": 27, "fats": 0.4, "serving": "1 medium"},
        {"name": "Greek Yogurt", "calories": 100, "protein": 17, "carbs": 6, "fats": 0.7, "serving": "170g"},
        {"name": "Almonds", "calories": 164, "protein": 6, "carbs": 6, "fats": 14, "serving": "28g"},
        {"name": "Sweet Potato", "calories": 86, "protein": 1.6, "carbs": 20, "fats": 0.1, "serving": "100g"},
        {"name": "Spinach", "calories": 23, "protein": 2.9, "carbs": 3.6, "fats": 0.4, "serving": "100g"},
        {"name": "Tuna", "calories": 132, "protein": 28, "carbs": 0, "fats": 1.3, "serving": "100g"},
        {"name": "Quinoa", "calories": 120, "protein": 4.4, "carbs": 21, "fats": 1.9, "serving": "100g"},
        {"name": "Avocado", "calories": 160, "protein": 2, "carbs": 9, "fats": 15, "serving": "100g"},
        {"name": "Cottage Cheese", "calories": 98, "protein": 11, "carbs": 3.4, "fats": 4.3, "serving": "100g"},
        {"name": "Apple", "calories": 52, "protein": 0.3, "carbs": 14, "fats": 0.2, "serving": "100g"},
        {"name": "Turkey Breast", "calories": 135, "protein": 30, "carbs": 0, "fats": 0.7, "serving": "100g"},
        {"name": "Black Beans", "calories": 132, "protein": 8.9, "carbs": 24, "fats": 0.5, "serving": "100g"},
        {"name": "Peanut Butter", "calories": 188, "protein": 8, "carbs": 7, "fats": 16, "serving": "2 tbsp"},
        {"name": "Orange", "calories": 47, "protein": 0.9, "carbs": 12, "fats": 0.1, "serving": "100g"}
    ]
    return {"foods": foods}