"""Recipe Suggestion Service - Business logic layer"""
import unicodedata
from difflib import SequenceMatcher

from app.repositories.recipe_repository import RecipeRepository
from app.dto.ai_service_dto import AIServiceDTO
import logging

logger = logging.getLogger(__name__)


class RecipeSuggestionService:
    """Service xử lý logic gợi ý công thức món ăn"""
    
    def __init__(self):
        """Initialize với repository"""
        self.recipe_repo = RecipeRepository()
    
    def generate_recipe_suggestion(self, user_ingredients, preferences=None, limit_recipes=None):
        """
        Generate recipe suggestion dựa trên ingredients người dùng có
        
        Flow:
        1. Query recipes từ DB (có thể filter theo preferences)
        2. Tính điểm tương đồng nguyên liệu trực tiếp trong BE
        3. Trả về best recipe + alternatives theo format cũ
        
        Args:
            user_ingredients (list): Danh sách tên ingredients người dùng có
                Ví dụ: ["trứng", "cà chua", "hành lá"]
            preferences (dict, optional): User preferences
                {
                    "difficulty": "De|Trung binh|Kho",
                    "cook_time_max": 30,
                    "cuisine_type": "Viet Nam"
                }
            limit_recipes (int, optional): Giới hạn số recipes query từ DB
                
        Returns:
            dict: Recipe suggestion kết quả
                {
                    "best_recipe": {...},
                    "reason": "...",
                    "missing_ingredients": [...],
                    "substitutions": [...],
                    "instructions": "...",
                    "alternative_recipes": [...]
                }
                
        Raises:
            ValueError: Nếu input không hợp lệ
        """
        # Validate input
        if not user_ingredients or len(user_ingredients) == 0:
            raise ValueError("Danh sách nguyên liệu không được rỗng")
        
        logger.info(f"Generating suggestion for ingredients: {user_ingredients}")
        
        # Step 1: Query recipes từ database
        # Có thể optimize bằng cách chỉ lấy recipes có chứa ít nhất 1 ingredient
        recipes = self._query_recipes(user_ingredients, preferences, limit_recipes)
        
        if not recipes:
            logger.warning("No recipes found in database")
            return {
                "best_recipe": None,
                "recipe_id": None,
                "reason": "Không tìm thấy công thức phù hợp trong cơ sở dữ liệu",
                "image_url": None,
                "cook_time_minutes": None,
                "difficulty": None,
                "servings": None,
                "matched_ingredients": [],
                "missing_ingredients": [],
                "substitutions": [],
                "instructions": [],
                "alternative_recipes": []
            }
        
        logger.info(f"Found {len(recipes)} recipes from database")

        scored_candidates = self._rank_recipes(user_ingredients, recipes)
        if not scored_candidates:
            return {
                "best_recipe": None,
                "recipe_id": None,
                "reason": "Không tìm thấy công thức phù hợp với nguyên liệu hiện có",
                "image_url": None,
                "cook_time_minutes": None,
                "difficulty": None,
                "servings": None,
                "matched_ingredients": [],
                "missing_ingredients": [],
                "substitutions": [],
                "instructions": [],
                "alternative_recipes": []
            }

        return self._build_db_suggestion_response(scored_candidates)
    
    def _query_recipes(self, user_ingredients, preferences, limit):
        """
        Query recipes từ database với filtering
        
        Args:
            user_ingredients (list): Ingredients người dùng có
            preferences (dict): User preferences
            limit (int): Limit số recipes
            
        Returns:
            list: Recipe ORM objects
        """
        # Strategy 2: Ưu tiên recipes có chứa ingredients người dùng có
        # Giúp giảm số candidate cần chấm điểm tương đồng
        recipes = self.recipe_repo.search_recipes_by_ingredients(
            ingredient_names=user_ingredients,
            limit=limit or 50  # Default 50 recipes
        )
        
        # Nếu không tìm thấy recipe nào có chứa ingredient, fallback về all recipes
        if not recipes:
            logger.info("No matching recipes, fallback to all recipes")
            recipes = self.recipe_repo.get_recipes_with_ingredients(limit=limit or 50)

        if preferences:
            recipes = self._apply_preferences(recipes, preferences)
            logger.info("Recipes after preference filter: %s", len(recipes))
        
        return recipes

    @staticmethod
    def _normalize_text(text):
        normalized = unicodedata.normalize('NFD', str(text or '').strip().lower())
        without_accents = ''.join(ch for ch in normalized if unicodedata.category(ch) != 'Mn')
        return ' '.join(without_accents.split())

    def _ingredient_similarity(self, user_name, recipe_name):
        user_norm = self._normalize_text(user_name)
        recipe_norm = self._normalize_text(recipe_name)

        if not user_norm or not recipe_norm:
            return 0.0

        if user_norm == recipe_norm:
            return 1.0

        if user_norm in recipe_norm or recipe_norm in user_norm:
            return 0.92

        user_tokens = set(user_norm.split())
        recipe_tokens = set(recipe_norm.split())
        token_overlap = len(user_tokens & recipe_tokens) / max(1, len(recipe_tokens))
        sequence_ratio = SequenceMatcher(None, user_norm, recipe_norm).ratio()

        return max(token_overlap, sequence_ratio)

    def _extract_recipe_ingredient_names(self, recipe):
        names = []
        for item in recipe.recipe_ingredients.order_by('sort_order').all():
            if item.ingredient and item.ingredient.name:
                names.append(str(item.ingredient.name).strip())
        return names

    def _rank_recipes(self, user_ingredients, recipes):
        normalized_user = [self._normalize_text(name) for name in user_ingredients if str(name).strip()]
        normalized_user = [name for name in normalized_user if name]

        if not normalized_user:
            return []

        scored = []
        for recipe in recipes:
            recipe_ingredient_names = self._extract_recipe_ingredient_names(recipe)
            if not recipe_ingredient_names:
                continue

            matched_recipe_ingredients = []
            matched_user_names = []
            missing_ingredients = []

            for recipe_ingredient_name in recipe_ingredient_names:
                best_user_name = None
                best_similarity = 0.0
                for user_name in normalized_user:
                    similarity = self._ingredient_similarity(user_name, recipe_ingredient_name)
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_user_name = user_name

                if best_similarity >= 0.72:
                    matched_recipe_ingredients.append(recipe_ingredient_name)
                    if best_user_name:
                        matched_user_names.append(best_user_name)
                else:
                    missing_ingredients.append(recipe_ingredient_name)

            if not matched_recipe_ingredients:
                continue

            total_recipe_ingredients = len(recipe_ingredient_names)
            matched_count = len(matched_recipe_ingredients)
            missing_count = len(missing_ingredients)

            coverage_score = matched_count / max(1, total_recipe_ingredients)
            availability_score = matched_count / max(1, len(normalized_user))
            match_score = round((coverage_score * 0.8) + (availability_score * 0.2), 4)

            scored.append({
                "recipe": recipe,
                "match_score": match_score,
                "matched_count": matched_count,
                "missing_count": missing_count,
                "matched_recipe_ingredients": matched_recipe_ingredients,
                "matched_user_ingredients": list(dict.fromkeys(matched_user_names)),
                "missing_ingredients": missing_ingredients
            })

        scored.sort(
            key=lambda item: (
                item["match_score"],
                item["matched_count"],
                -item["missing_count"]
            ),
            reverse=True
        )
        return scored

    def _build_db_suggestion_response(self, scored_candidates):
        best = scored_candidates[0]
        best_recipe = best["recipe"]

        best_recipe_payload = {
            "id": str(best_recipe.id),
            "name": str(best_recipe.name or "").strip(),
            "match_score": best["match_score"],
            "matched_ingredients": best["matched_recipe_ingredients"],
            "matched_count": best["matched_count"],
            "total_ingredients": best["matched_count"] + best["missing_count"],
            "image_url": best_recipe.image_url,
            "cook_time_minutes": best_recipe.cook_time_minutes,
            "difficulty": best_recipe.difficulty,
            "servings": best_recipe.servings
        }

        alternatives = []
        for candidate in scored_candidates[1:4]:
            recipe = candidate["recipe"]
            alternatives.append({
                "id": str(recipe.id),
                "name": str(recipe.name or "").strip(),
                "matched_count": candidate["matched_count"],
                "missing_count": candidate["missing_count"],
                "image_url": recipe.image_url,
                "cook_time_minutes": recipe.cook_time_minutes,
                "difficulty": recipe.difficulty,
                "description": recipe.description
            })

        recipe_dict = AIServiceDTO.recipe_to_dict(best_recipe)
        instructions = [
            line.strip() for line in recipe_dict.get("steps", "").split('\n') if line.strip()
        ]

        return {
            "best_recipe": best_recipe_payload,
            "recipe_id": str(best_recipe.id),
            "reason": (
                f"Tìm thấy công thức khớp {best['matched_count']}/"
                f"{best['matched_count'] + best['missing_count']} nguyên liệu cần thiết."
            ),
            "image_url": best_recipe.image_url,
            "cook_time_minutes": best_recipe.cook_time_minutes,
            "difficulty": best_recipe.difficulty,
            "servings": best_recipe.servings,
            "matched_ingredients": best["matched_recipe_ingredients"],
            "missing_ingredients": best["missing_ingredients"],
            "substitutions": [],
            "instructions": instructions,
            "alternative_recipes": alternatives
        }

    def _apply_preferences(self, recipes, preferences):
        filtered = recipes

        difficulty = (preferences or {}).get('difficulty')
        if difficulty:
            difficulty_norm = self._normalize_text(difficulty)
            filtered = [
                recipe for recipe in filtered
                if self._normalize_text(recipe.difficulty) == difficulty_norm
            ]

        cook_time_max = (preferences or {}).get('cook_time_max')
        if isinstance(cook_time_max, int):
            filtered = [
                recipe for recipe in filtered
                if recipe.cook_time_minutes is not None and recipe.cook_time_minutes <= cook_time_max
            ]

        cuisine_type = (preferences or {}).get('cuisine_type')
        if cuisine_type:
            cuisine_norm = self._normalize_text(cuisine_type)
            filtered = [
                recipe for recipe in filtered
                if self._normalize_text(recipe.cuisine_type) == cuisine_norm
            ]

        diet_tags = (preferences or {}).get('diet_tags')
        if isinstance(diet_tags, list) and diet_tags:
            required_tags = {self._normalize_text(tag) for tag in diet_tags if str(tag).strip()}
            filtered = [
                recipe for recipe in filtered
                if required_tags.issubset({self._normalize_text(tag) for tag in (recipe.diet_tags or [])})
            ]

        return filtered if filtered else recipes
    
    def get_recipe_detail(self, recipe_id):
        """
        Lấy chi tiết một recipe
        
        Args:
            recipe_id (str): Recipe ID
            
        Returns:
            dict: Recipe detail hoặc None
        """
        recipe = self.recipe_repo.get_recipe_by_id(recipe_id)
        if not recipe:
            return None
        
        return AIServiceDTO.recipe_to_dict(recipe)
