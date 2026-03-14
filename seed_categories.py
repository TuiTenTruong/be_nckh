#!/usr/bin/env python
"""Script to seed initial ingredient categories"""
import uuid
import os
from app import create_app, db
from app.models.ingredient import IngredientCategory

def seed_categories():
    """Seed initial ingredient categories"""
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        # Clear existing categories
        IngredientCategory.query.delete()
        db.session.commit()
        
        # Default categories from database schema
        categories = [
            {
                'slug': 'protein',
                'name': 'Chất đạm',
                'icon': '🥩',
                'sort_order': 1
            },
            {
                'slug': 'vegetable',
                'name': 'Rau cu',
                'icon': '🥬',
                'sort_order': 2
            },
            {
                'slug': 'spice',
                'name': 'Gia vi',
                'icon': '🧄',
                'sort_order': 3
            },
            {
                'slug': 'grain',
                'name': 'Ngu coc',
                'icon': '🌾',
                'sort_order': 4
            },
            {
                'slug': 'seafood',
                'name': 'Hai san',
                'icon': '🦐',
                'sort_order': 5
            },
            {
                'slug': 'dairy',
                'name': 'Sua & Trung',
                'icon': '🥚',
                'sort_order': 6
            },
            {
                'slug': 'sauce',
                'name': 'Nuoc cham & Sot',
                'icon': '🫙',
                'sort_order': 7
            },
            {
                'slug': 'other',
                'name': 'Khac',
                'icon': '🥘',
                'sort_order': 8
            },
        ]
        
        # Create categories
        for cat_data in categories:
            category = IngredientCategory(
                id=str(uuid.uuid4()),
                slug=cat_data['slug'],
                name=cat_data['name'],
                icon=cat_data['icon'],
                sort_order=cat_data['sort_order']
            )
            db.session.add(category)
            print(f"Created category: {cat_data['name']}")
        
        db.session.commit()
        print(f"\n✅ Successfully seeded {len(categories)} categories!")

if __name__ == '__main__':
    seed_categories()
