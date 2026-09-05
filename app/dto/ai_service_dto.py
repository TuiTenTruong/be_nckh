"""DTO - Transform ORM objects thành JSON payload cho AI service"""

from app.utils.media_url import resolve_image_url


class AIServiceDTO:
    """Transform data để gửi sang AI service"""
    
    @staticmethod
    def recipe_to_dict(recipe):
        """
        Transform một Recipe ORM object thành dict cho AI service
        
        Args:
            recipe: Recipe ORM object
            
        Returns:
            dict: {
                "id": "...",
                "name": "...",
                "description": "...",
                "steps": "...",  # Combined steps thành string
                "ingredients": [{"name": "...", "quantity": "...", "unit": "..."}],
                "image_url": "...",
                "cook_time_minutes": 30,
                "difficulty": "...",
                "servings": 4
            }
        """
        # Lấy ingredients
        ingredients_list = []
        for recipe_ingredient in recipe.recipe_ingredients.order_by('sort_order').all():
            if recipe_ingredient.ingredient:
                ingredients_list.append({
                    "name": str(recipe_ingredient.ingredient.name or "").strip(),
                    "quantity": str(recipe_ingredient.quantity or "").strip(),
                    "unit": str(recipe_ingredient.unit or "").strip(),
                })
        
        # Lấy steps và combine thành string
        steps = recipe.steps.order_by('step_number').all()
        steps_text = ""
        for step in steps:
            if step.title:
                steps_text += f"{step.step_number}. {step.title}: {step.description}\n"
            else:
                steps_text += f"{step.step_number}. {step.description}\n"
        
        return {
            "id": str(recipe.id),
            "name": str(recipe.name or "").strip(),
            "description": recipe.description,
            "steps": steps_text.strip(),
            "ingredients": ingredients_list,
            "image_url": resolve_image_url(recipe.image_url, name=recipe.name),
            "cook_time_minutes": recipe.cook_time_minutes,
            "difficulty": recipe.difficulty,
            "servings": recipe.servings,
            "cuisine_type": recipe.cuisine_type
        }
    
    @staticmethod
    def recipes_list_to_dict(recipes):
        """
        Transform danh sách Recipes thành list of dicts
        
        Args:
            recipes (list): Danh sách Recipe ORM objects
            
        Returns:
            list: Danh sách recipe dicts
        """
        return [AIServiceDTO.recipe_to_dict(recipe) for recipe in recipes]
    
    @staticmethod
    def build_ai_request_payload(user_ingredients, recipes):
        """
        Build payload hoàn chỉnh để gửi sang AI service
        
        Args:
            user_ingredients (list): Danh sách tên ingredients người dùng có
            recipes (list): Danh sách Recipe ORM objects
            
        Returns:
            dict: Payload JSON để gửi sang AI service
            {
                "user_ingredients": ["trứng", "cà chua", ...],
                "recipes": [
                    {
                        "id": "...",
                        "name": "...",
                        "description": "...",
                        "steps": "...",
                        "ingredients": [{"name": "...", "quantity": "...", "unit": "..."}],
                        "image_url": "...",
                        "cook_time_minutes": 30
                    }
                ]
            }
        """
        return {
            "user_ingredients": user_ingredients,
            "recipes": AIServiceDTO.recipes_list_to_dict(recipes)
        }
    
    @staticmethod
    def build_ai_request_with_preferences(user_ingredients, recipes, preferences=None):
        """
        Build payload với thêm preferences (nếu có)
        
        Args:
            user_ingredients (list): Danh sách ingredients
            recipes (list): Danh sách Recipe objects
            preferences (dict, optional): User preferences
                {
                    "difficulty": "De|Trung binh|Kho",
                    "cook_time_max": 30,
                    "cuisine_type": "Viet Nam",
                    "diet_tags": ["chay", "it dau mo"]
                }
                
        Returns:
            dict: Payload với preferences
        """
        payload = AIServiceDTO.build_ai_request_payload(user_ingredients, recipes)
        
        if preferences:
            payload["preferences"] = preferences
        
        return payload
