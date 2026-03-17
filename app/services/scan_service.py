"""Scan service - Business logic"""
import uuid
import unicodedata
from app.extensions import db
from app.models.ingredient import Ingredient
from app.models.scan import ScanSession
from app.services.vision_service import VisionService


class ScanService:
    """Service for scan operations"""

    @staticmethod
    def create_scan(image_bytes, filename, user_id='anonymous'):
        """Create scan session and return matched ingredients"""
        detections, provider = VisionService.detect_ingredients(image_bytes, filename)
        matched = ScanService._match_ingredients(detections)

        session = ScanSession(
            id=str(uuid.uuid4()),
            user_id=user_id,
            image_name=filename,
            vision_provider=provider,
            raw_detections=detections,
            matched_ingredients=matched
        )

        db.session.add(session)
        db.session.commit()

        return session.to_dict()

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
