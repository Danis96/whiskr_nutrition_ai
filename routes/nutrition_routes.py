from fastapi import APIRouter, HTTPException
from typing import Dict
from llm import PetNutritionLLM

router = APIRouter(
    prefix="/nutrition",
    tags=["nutrition"]
)

nutrition_llm = PetNutritionLLM()

# Todo -  add JWT auth

@router.post("/get_meal_guidelines")
async def get_nutrition_plan(request_data: Dict):
    try:
        pet_data: Dict = {
            "name": request_data.get("name", "Unknown"),
            "breed": request_data.get("breed", "Unknown"),
            "gender": request_data.get("gender", "Unknown"),
            "species": request_data.get("species", "Unknown"),
            "age": request_data.get("age", 0),
            "weight": request_data.get("weight", 0.0),
            "activity_level": request_data.get("activity_level", "Unknown"),
            "health_concerns": request_data.get("health_concerns", "None"),
        }

        response: Dict = nutrition_llm.generate_meal_plan(
            pet_data=pet_data,
            food_journal=request_data.get("food_journal")
        )

        return response  

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
