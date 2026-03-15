"""Pantry service - Business logic"""
import uuid
from app.extensions import db
from app.models.ingredient import Ingredient
from app.models.pantry import PantryItem


class PantryService:
    """Service for pantry operations"""

    @staticmethod
    def get_pantry(user_id):
        """Get pantry list for one user"""
        items = PantryItem.query.filter_by(user_id=user_id).order_by(PantryItem.created_at.desc()).all()
        return [item.to_dict() for item in items]

    @staticmethod
    def add_item(user_id, ingredient_id, quantity):
        """Add or update pantry item"""
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            raise ValueError(f"Ingredient '{ingredient_id}' not found")

        existing = PantryItem.query.filter_by(user_id=user_id, ingredient_id=ingredient_id).first()
        if existing:
            existing.quantity = str(quantity)
            db.session.commit()
            return existing.to_dict()

        item = PantryItem(
            id=str(uuid.uuid4()),
            user_id=user_id,
            ingredient_id=ingredient_id,
            quantity=str(quantity)
        )
        db.session.add(item)
        db.session.commit()
        return item.to_dict()

    @staticmethod
    def delete_item(user_id, pantry_item_id):
        """Delete pantry item by ID"""
        item = PantryItem.query.filter_by(id=pantry_item_id, user_id=user_id).first()
        if not item:
            raise ValueError(f"Pantry item '{pantry_item_id}' not found")

        db.session.delete(item)
        db.session.commit()

        return {'message': 'Pantry item deleted successfully'}
