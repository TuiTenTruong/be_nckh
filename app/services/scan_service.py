"""Scan service - Business logic"""
import uuid
import unicodedata
import logging
from app.extensions import db
from app.models.ingredient import Ingredient
from app.models.scan import ScanSession
from app.services.vision_service import VisionService
from app.services.recipe_suggestion_service import RecipeSuggestionService

logger = logging.getLogger(__name__)


class ScanService:
    """Service for scan operations"""

    @staticmethod
    def create_scan(image_bytes, filename, user_id='anonymous', preferences=None):
        """
        Create scan session: detect ingredients → get recipe suggestions
        
        Flow:
        1. Call AI service để phát hiện nguyên liệu từ ảnh
        2. Match với database ingredients
        3. Query DB để lấy gợi ý công thức dựa trên nguyên liệu đã phát hiện
        4. Lưu session và trả về kết quả
        
        Args:
            image_bytes: Raw image bytes
            filename: Original filename
            user_id: User identifier
            preferences: Optional user preferences for recipe filtering
            
        Returns:
            dict: Scan result với ingredients và recipe suggestion
        """
        # Step 1: Call food-ai-service để phát hiện nguyên liệu
        detections, vision_ai_suggestion, provider = VisionService.detect_ingredients(image_bytes, filename)
        
        # Step 2: Match detected ingredients với database
        matched = ScanService._match_ingredients(detections)
        
        # Step 3: Lấy danh sách tên ingredients đã match để gọi recipe suggestion
        matched_ingredient_names = ScanService._extract_matched_ingredient_names(matched)
        logger.info(f"Matched ingredient names: {matched_ingredient_names}")
        
        # Step 4: Query DB để lấy gợi ý công thức
        recipe_suggestion = None
        if matched_ingredient_names:
            logger.info(f"Calling recipe suggestion for {len(matched_ingredient_names)} ingredients")
            recipe_suggestion = ScanService._get_recipe_suggestion(
                ingredient_names=matched_ingredient_names,
                preferences=preferences
            )
            logger.info(f"Recipe suggestion result: {recipe_suggestion is not None}")
            if recipe_suggestion:
                logger.info(f"Best recipe: {recipe_suggestion.get('best_recipe')}")
        else:
            logger.info("No matched ingredients found, skipping recipe suggestion")

        # Step 5: Lưu session
        session = ScanSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            image_name=filename,
            vision_provider=provider,
            raw_detections=detections,
            matched_ingredients=matched,
            ai_suggestion=vision_ai_suggestion,  # Vision AI suggestion (legacy)
            recipe_suggestion=recipe_suggestion  # Recipe suggestion từ RAG
        )

        db.session.add(session)
        db.session.commit()
        
        logger.info(f"Session saved with id: {session.id}")

        return session.to_dict()
    
    @staticmethod
    def _extract_matched_ingredient_names(matched_ingredients):
        """
        Trích xuất tên ingredients đã match thành công
        
        Args:
            matched_ingredients: List of matched ingredient dicts
            
        Returns:
            list: List of ingredient names
        """
        names = []
        for item in matched_ingredients:
            if item.get('matched') and item.get('ingredient'):
                ingredient = item['ingredient']
                name = ingredient.get('name')
                if name:
                    names.append(name)
        return names
    
    @staticmethod
    def _get_recipe_suggestion(ingredient_names, preferences=None):
        """
        Gọi RecipeSuggestionService để lấy gợi ý công thức
        
        Args:
            ingredient_names: List of ingredient names
            preferences: Optional user preferences
            
        Returns:
            dict: Recipe suggestion hoặc None nếu lỗi
        """
        try:
            suggestion_service = RecipeSuggestionService()
            result = suggestion_service.generate_recipe_suggestion(
                user_ingredients=ingredient_names,
                preferences=preferences,
                limit_recipes=30  # Giới hạn để tăng tốc
            )
            logger.info(f"Successfully got recipe suggestion for {len(ingredient_names)} ingredients")
            return result
        except ValueError as e:
            logger.warning(f"Validation error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting recipe suggestion: {e}")
            return {
                "error": True,
                "error_code": "INTERNAL_ERROR", 
                "message": str(e),
                "best_recipe": None,
                "alternative_recipes": []
            }

    @staticmethod
    def get_scan_by_id(scan_id):
        """Get scan session by ID"""
        session = ScanSession.query.get(scan_id)
        return session.to_dict() if session else None

    @staticmethod
    def _normalize_name(name):
        """Normalize ingredient name for matching"""
        normalized = unicodedata.normalize('NFD', (name or '').strip().lower())
        without_accents = ''.join(ch for ch in normalized if unicodedata.category(ch) != 'Mn')
        return ' '.join(without_accents.split())

    @staticmethod
    def _build_ingredient_lookup():
        """Build in-memory lookup by name and aliases"""
        lookup = {}
        ingredients = Ingredient.query.all()

        for ingredient in ingredients:
            ingredient_data = ingredient.to_dict(include_category=True)

            names = [ingredient.name]
            if ingredient.aliases and isinstance(ingredient.aliases, list):
                names.extend(ingredient.aliases)

            for name in names:
                normalized = ScanService._normalize_name(name)
                if normalized:
                    lookup[normalized] = ingredient_data

        return lookup

    @staticmethod
    def _match_ingredients(detections):
        """Match vision detections against ingredients table"""
        lookup = ScanService._build_ingredient_lookup()
        matched = []

        for item in detections:
            raw_name = item.get('name', '')
            confidence = item.get('confidence')
            normalized = ScanService._normalize_name(raw_name)

            ingredient = lookup.get(normalized)
            matched.append({
                'detected_name': raw_name,
                'normalized_name': normalized,
                'confidence': confidence,
                'matched': ingredient is not None,
                'ingredient': ingredient
            })

        return matched
