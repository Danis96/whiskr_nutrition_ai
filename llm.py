from fastapi import HTTPException
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from typing import Dict, List, Optional, Set
import requests.exceptions
import json
from llm_validation import PetDataValidator, PetValidationError


class PetNutritionLLM:
    def __init__(self, model_name: str = "mistral:7b"):
        try:
            self.model: OllamaLLM = OllamaLLM(
                model=model_name,
                base_url="http://localhost:11434",
                timeout=30,
                format="json",
                stop=[
                    "[INST]",
                    "[/INST]"
                ]

            )
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Could not connect to Ollama service. Please ensure Ollama is running"
            )
        
        self.template: str = (
            "[INST] You are a pet nutritionist with expertise in creating personalized meal plans for pets. "
            "Based on the following pet details, generate a comprehensive and balanced meal plan:\n\n"
            "- **Name:** {name} \n"
            "- **Breed:** {breed} \n"
            "- **Age:** {age} years \n"
            "- **Gender:** {gender} \n"
            "- **Species:** {species} \n"
            "- **Weight:** {weight} kg \n"
            "- **Activity Level:** {activity_level} (Low, Medium, High) \n"
            "- **Health Concerns:** {health_concerns} \n\n"
            "IMPORTANT CONSIDERATIONS:\n"
            "1. Calculate calories based on species, weight, and activity level.\n"
            "   ONLY USE THE GUIDELINES FOR THE SPECIFIC SPECIES ({species}) OF THIS PET:\n\n"
            "   CATS (ONLY USE IF PET IS A CAT):\n"
            "   - Indoor/Low Activity (3-6kg): 200-250 calories/day\n"
            "   - Outdoor/Medium Activity (3-6kg): 250-300 calories/day\n"
            "   - High Activity (3-6kg): 300-400 calories/day\n\n"
            "   DOGS (ONLY USE IF PET IS A DOG):\n"
            "   - Small Dogs (1-10kg):\n"
            "     * Low Activity: 200-400 calories/day\n"
            "     * Medium Activity: 400-600 calories/day\n"
            "     * High Activity: 600-800 calories/day\n"
            "   - Medium Dogs (10-25kg):\n"
            "     * Low Activity: 800-1000 calories/day\n"
            "     * Medium Activity: 1000-1200 calories/day\n"
            "     * High Activity: 1200-1500 calories/day\n"
            "   - Large Dogs (25kg+):\n"
            "     * Low Activity: 1500-1800 calories/day\n"
            "     * Medium Activity: 1800-2200 calories/day\n"
            "     * High Activity: 2200-2500 calories/day\n\n"
            "2. Portion Size Calculations:\n"
            "   - Calculate dry food portions: Daily calories ÷ calories per cup (approximately 400 kcal/cup)\n"
            "   - Calculate wet food portions: Daily calories ÷ calories per can (approximately 250 kcal/can)\n"
            "   - Fresh food portions should be weighed in grams\n"
            "   - Treats should not exceed 10% of daily caloric intake\n\n"
            "3. Activity Level Adjustments:\n"
            "   - Low Activity: Multiply base calories by 0.8\n"
            "   - Medium Activity: Use base calories\n"
            "   - High Activity: Multiply base calories by 1.2\n\n"
            "4. Age Adjustments:\n"
            "   - Puppies/Kittens: Multiply adult calories by 1.5-2\n"
            "   - Senior Pets: Reduce adult calories by 20%\n\n"
            "5. Health Considerations:\n"
            "   - Overweight: Reduce calories by 20%\n"
            "   - Underweight: Increase calories by 20%\n"
            "   - Pregnant/Nursing: Increase calories by 50%\n\n"
            "6. Breed-Specific Needs:\n"
            "   - Small breeds: More frequent, smaller meals\n"
            "   - Large breeds: Anti-bloat considerations\n"
            "   - Brachycephalic breeds: Easy-to-eat food sizes\n"
            "   - Working breeds: Higher protein requirements\n\n"
            "7. Current weight of {weight}kg and activity level of {activity_level} must be used\n"
            "   to calculate final portions using these guidelines.\n\n"
            "REQUIRED RESPONSE ELEMENTS:\n"
            "1. Caloric intake must be specified in calories/day\n"
            "2. Meal plan must include specific times and portion sizes in grams\n"
            "3. Nutrition balance must include all percentages (protein, fat, carbs, fiber, moisture)\n"
            "4. Warnings must include health considerations or 'No specific warnings for this pet'\n"
            "5. Ingredients must list all components of recommended foods\n"
            "6. Feeding guidelines must include frequency, portion control, water intake, and tips\n"
            "7. Supplements must specify recommendations or 'No supplements required'\n"
            "8. Foods to avoid must list specific items or 'Standard diet is appropriate, avoid common harmful foods'\n"
            "9. Transition guidelines must explain how to implement the meal plan\n\n"
            "IMPORTANT SPECIES-SPECIFIC INSTRUCTIONS:\n"
            "1. This pet is a {species}. ONLY provide information relevant to {species}.\n"
            "2. Do NOT mention dietary needs or considerations for any other species.\n"
            "3. All recommendations must be specifically tailored for a {species}.\n"
            "4. Never mention cats if this is a dog, and never mention dogs if this is a cat.\n\n"
            "Consider these factors for the meal plan:\n"
            "1. Age-appropriate portions and nutritional needs\n"
            "2. Activity level and energy requirements\n"
            "3. Species-specific nutritional requirements\n"
            "4. Breed-specific dietary considerations\n\n"
            "IMPORTANT NOTES ABOUT INGREDIENTS:\n"
            "1. Only include natural, whole food ingredients (like meats, vegetables, grains)\n"
            "2. Do not include chemical compounds, preservatives, or synthetic additives\n"
            "3. Keep ingredients simple and recognizable to pet owners\n"
            "4. Example of good ingredients: chicken breast, brown rice, sweet potatoes, carrots\n"
            "5. Focus on primary ingredients that make up the bulk of the meal\n"
            "6. Only include ingredients that are safe and healthy for the pet\n"
            "Consider these factors for the meal plan:\n"
            "1. Age-appropriate portions and nutritional needs\n"
            "2. Activity level and energy requirements\n"
            "3. Species-specific nutritional requirements\n"
            "4. Breed-specific dietary considerations [/INST]\n"
        )

        self.food_journal_template: str = (
            "[INST] Consider this food journal when creating the meal plan:\n\n"
            "{food_journal}\n\n"
            "REQUIRED FOOD JOURNAL ANALYSIS:\n"
            "1. Review and incorporate previously successful meals\n"
            "2. Maintain consistent feeding times from the journal\n"
            "3. Include familiar ingredients in new meal plan\n"
            "4. Note any foods that should be continued or avoided\n"
            "5. Calculate appropriate portion sizes based on recorded amounts\n"
            "6. Consider the spacing between meals\n"
            "7. Evaluate the variety of foods being offered\n"
            "8. Assess the current nutritional balance\n\n"
            "Use this information to create a meal plan that:\n"
            "1. Maintains successful feeding patterns\n"
            "2. Improves upon current diet where needed\n"
            "3. Keeps familiar foods while introducing beneficial changes\n"
            "4. Ensures all nutritional requirements are met\n"
            "5. Provides specific portions and times based on established routine [/INST]\n"
        )
        
        self.existing_recipes_template: str = (
            "[INST] The user already has the following recipe titles saved: {existing_recipes}. "
            "Please ensure that your suggested recipes have DIFFERENT titles than these existing ones. "
            "Create unique recipe names that do not duplicate any of the existing titles. [/INST]\n"
        )

        self.closing_instructions: str = (
            "[INST] Provide a complete JSON response. Every field must be filled with meaningful content. "
            "Empty or missing fields are not acceptable. Use this exact structure:\n"
            "{{\n"
            '  "caloric_intake": "REQUIRED: daily calories with unit",\n'
            '  "meal_plan": {{\n'
            '      "breakfast": "REQUIRED: food with gram portions and time",\n'
            '      "lunch": "REQUIRED: food with gram portions and time",\n'
            '      "dinner": "REQUIRED: food with gram portions and time",\n'
            '      "snacks": "REQUIRED: specify snacks or state No snacks recommended"\n'
            '  }},\n'
            '  "nutrition_balance": {{\n'
            '      "protein": "REQUIRED: percentage",\n'
            '      "fat": "REQUIRED: percentage",\n'
            '      "carbs": "REQUIRED: percentage",\n'
            '      "fiber": "REQUIRED: percentage",\n'
            '      "moisture": "REQUIRED: percentage"\n'
            '  }},\n'
            '  "warnings": "REQUIRED: specific warnings or No specific warnings",\n'
            '  "ingredients": [\n'
            '    {{\n'
            '      "recipe_name": "REQUIRED: simple descriptive name for first recipe",\n'
            '      "ingredients": ["REQUIRED: only whole food ingredients"],\n'
            '      "preparation": ["REQUIRED: simple cooking instructions"],\n'
            '      "description": "REQUIRED: Write at least 2 complete sentences and no more than 4 sentences describing the recipe. Each recipe description MUST be at least 2 full sentences."\n'
            '    }},\n'
            '    {{\n'
            '      "recipe_name": "REQUIRED: simple descriptive name for second recipe",\n'
            '      "ingredients": ["REQUIRED: only whole food ingredients"],\n'
            '      "preparation": ["REQUIRED: simple cooking instructions"],\n'
            '      "description": "REQUIRED: Write at least 2 complete sentences and no more than 4 sentences describing the recipe. Each recipe description MUST be at least 2 full sentences."\n'
            '    }}\n'
            '  ],\n'
            '  "feeding_guidelines": {{\n'
            '      "frequency": "REQUIRED: specific timing",\n'
            '      "portion_control": "REQUIRED: specific guidelines",\n'
            '      "water_intake": "REQUIRED: specific amounts",\n'
            '      "feeding_tips": "REQUIRED: practical advice"\n'
            '  }},\n'
            '  "supplements": "REQUIRED: specific supplements or No supplements required",\n'
            '  "foods_to_avoid": "REQUIRED: specific foods or Standard cautions",\n'
            '  "transition_guidelines": "REQUIRED: specific transition plan"\n'
            "}} [/INST]\n"
        )

    def generate_meal_plan(self, pet_data: Dict, food_journal: Optional[List[Dict]] = None, existing_recipes: Optional[List[str]] = None) -> Dict:
        try:
            # Initialize validator and validate pet data
            validator = PetDataValidator()
            try:
                validated_pet_data = validator.validate_pet_data(pet_data)
            except PetValidationError as validation_error:
                error_response = {
                    "status": "error",
                    "code": 400,
                    "message": str(validation_error),
                }
                return error_response
            
            # Start with base prompt
            full_prompt: str = self.template.format(**validated_pet_data)

            # Append food journal if provided
            if food_journal:
                food_entries: str = "\n".join(
                    [f"- {entry['dateTime']}: {entry['description']} ({entry['quantity']} {entry['quantityUnit']})" 
                     for entry in food_journal]
                )
                full_prompt += self.food_journal_template.format(food_journal=food_entries)
            else:
                full_prompt += self.food_journal_template.format(food_journal="No food journal provided")
                
            # Add existing recipes information if provided
            if existing_recipes and len(existing_recipes) > 0:
                existing_recipes_str: str = ", ".join([f'"{title}"' for title in existing_recipes])
                full_prompt += self.existing_recipes_template.format(existing_recipes=existing_recipes_str)

            # Add final instructions
            full_prompt += self.closing_instructions

            prompt: ChatPromptTemplate = ChatPromptTemplate.from_template(full_prompt)
            chain = prompt | self.model
            response: str = chain.invoke(validated_pet_data)

            # Try to parse the response as JSON
            try:
                # Clean the response string to ensure it's valid JSON
                response = response.strip()
                if response.startswith('```json'):
                    response = response[7:]
                if response.endswith('```'):
                    response = response[:-3]
                response = response.strip()
                
                return json.loads(response)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON response from model: {response}\nError: {str(e)}")
            
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Lost connection to Ollama service. Please ensure Ollama is running and accessible."
            )
        except Exception as e:
            raise Exception(f"Error generating meal plan: {str(e)}")
