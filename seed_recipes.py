#!/usr/bin/env python
"""Script to seed recipes from final1.json with automatic ingredient categorization"""
import uuid
import os
import json
import re
from app import create_app, db
from app.models.recipe import Recipe
from app.models.recipeStep import RecipeStep
from app.models.ingredient import Ingredient, IngredientCategory
from app.models.recipeIngredient import RecipeIngredient


# Ingredient categorization rules (keyword-based)
CATEGORY_KEYWORDS = {
    'protein': {
        'keywords': ['thịt', 'gà', 'vịt', 'heo', 'bò', 'dê', 'chân', 'sườn', 'ba chỉ', 'phi lê', 
                     'giò', 'xương', 'óc', 'lòng', 'tim', 'gan', 'dạ dày', 'thăn'],
        'name': 'Chất đạm',
        'icon': '🥩',
        'sort_order': 1
    },
    'seafood': {
        'keywords': ['cá', 'tôm', 'cua', 'ghẹ', 'mực', 'bạch tuộc', 'sò', 'hàu', 'ốc', 'ngao', 
                     'nghêu', 'hải sản', 'tép', 'chả cá', 'lóc', 'rô phi', 'thu'],
        'name': 'Hải sản',
        'icon': '🦐',
        'sort_order': 5
    },
    'vegetable': {
        'keywords': ['rau', 'cải', 'xà lách', 'rong', 'tía tô', 'húng', 'ngò', 'hành lá', 
                     'cần', 'mùi', 'diếp', 'dền', 'muống', 'cải thảo', 'bạc hà', 'su su',
                     'bắp cải', 'salad'],
        'name': 'Rau củ',
        'icon': '🥬',
        'sort_order': 2
    },
    'spice': {
        'keywords': ['tỏi', 'hành', 'ớt', 'gừng', 'sả', 'tiêu', 'nghệ', 'mè', 'vừng', 
                     'ngũ vị hương', 'hồi', 'quế', 'hạt nêm', 'bột ngọt', 'đường', 
                     'muối', 'mắm', 'nước mắm', 'tương', 'nước tương', 'dầu', 'giấm',
                     'mẻ', 'cơm mẻ', 'chanh', 'me', 'gia vị', 'bột canh', 'mì chính'],
        'name': 'Gia vị',
        'icon': '🧄',
        'sort_order': 3
    },
    'grain': {
        'keywords': ['gạo', 'nếp', 'bột', 'bún', 'phở', 'miến', 'mì', 'bánh', 'cơm', 
                     'ngô', 'bột mì', 'bột năng', 'bột gạo', 'bánh canh', 'bánh đa',
                     'đậu xanh', 'đậu đỏ', 'đậu nành'],
        'name': 'Ngũ cốc',
        'icon': '🌾',
        'sort_order': 4
    },
    'dairy': {
        'keywords': ['sữa', 'trứng', 'phô mai', 'bơ', 'yaourt', 'kem', 'cheese', 'butter'],
        'name': 'Sữa & Trứng',
        'icon': '🥚',
        'sort_order': 6
    },
    'sauce': {
        'keywords': ['nước chấm', 'sốt', 'tương ớt', 'sa tế', 'mắm tôm', 'mắm ruốc', 
                     'hoisin', 'mayonnaise', 'ketchup'],
        'name': 'Nước chấm & Sốt',
        'icon': '🫙',
        'sort_order': 7
    }
}


def get_category_for_ingredient(ingredient_name):
    """Determine category based on ingredient name using keyword matching"""
    ingredient_lower = ingredient_name.lower()
    
    for category_slug, category_info in CATEGORY_KEYWORDS.items():
        for keyword in category_info['keywords']:
            if keyword in ingredient_lower:
                return category_slug
    
    # Default to 'other' if no match found
    return 'other'


def ensure_categories_exist():
    """Ensure all ingredient categories exist in database"""
    categories = {}
    
    # Define all categories including 'other'
    all_categories = dict(CATEGORY_KEYWORDS)
    all_categories['other'] = {
        'name': 'Khác',
        'icon': '🥘',
        'sort_order': 8
    }
    
    for slug, info in all_categories.items():
        category = IngredientCategory.query.filter_by(slug=slug).first()
        
        if not category:
            category = IngredientCategory(
                id=str(uuid.uuid4()),
                slug=slug,
                name=info['name'],
                icon=info['icon'],
                sort_order=info['sort_order']
            )
            db.session.add(category)
            print(f"   🆕 Created category: {info['name']}")
        
        categories[slug] = category
    
    db.session.commit()
    return categories


def seed_recipes():
    """Seed recipes from final1.json with proper categorization"""
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        # Step 1: Ensure categories exist
        print("🏷️  Checking ingredient categories...")
        categories = ensure_categories_exist()
        
        # Load JSON data
        with open('final1.json', 'r', encoding='utf-8') as f:
            recipes_data = json.load(f)
        
        print(f"\n📚 Loading {len(recipes_data)} recipes from final1.json...")
        
        # Track statistics
        created_recipes = 0
        created_ingredients = 0
        created_steps = 0
        category_stats = {slug: 0 for slug in categories.keys()}
        
        # Keep track of existing ingredients to avoid duplicates
        ingredient_cache = {}
        
        for idx, recipe_data in enumerate(recipes_data, 1):
            try:
                # Create recipe
                recipe = Recipe(
                    id=str(uuid.uuid4()),
                    name=recipe_data.get('name', 'Món ăn không tên'),
                    description=recipe_data.get('description', ''),
                    image_url=recipe_data.get('url', ''),  # Use URL as placeholder for image
                    cook_time_minutes=30,  # Default value
                    difficulty='Trung binh',  # Default difficulty
                    servings=2,
                    cuisine_type='Viet Nam',
                    diet_tags=[]
                )
                db.session.add(recipe)
                created_recipes += 1
                
                # Create ingredients and recipe_ingredients
                ingredients_list = recipe_data.get('ingredients', [])
                for sort_idx, ingredient_name in enumerate(ingredients_list, 1):
                    ingredient_name_clean = ingredient_name.strip()
                    
                    if ingredient_name_clean in ingredient_cache:
                        ingredient = ingredient_cache[ingredient_name_clean]
                    else:
                        # Check if ingredient exists in database
                        ingredient = Ingredient.query.filter_by(name=ingredient_name_clean).first()
                        
                        if not ingredient:
                            # Determine category for new ingredient
                            category_slug = get_category_for_ingredient(ingredient_name_clean)
                            category = categories[category_slug]
                            
                            # Create new ingredient with category
                            ingredient = Ingredient(
                                id=str(uuid.uuid4()),
                                name=ingredient_name_clean,
                                icon='🥘',  # Default icon
                                category_id=category.id,
                                is_popular=False,
                                aliases=[]
                            )
                            db.session.add(ingredient)
                            created_ingredients += 1
                            category_stats[category_slug] += 1
                        
                        # Add to cache
                        ingredient_cache[ingredient_name_clean] = ingredient
                    
                    # Create recipe-ingredient relationship
                    recipe_ingredient = RecipeIngredient(
                        id=str(uuid.uuid4()),
                        recipe_id=recipe.id,
                        ingredient_id=ingredient.id,
                        quantity='1',
                        unit='vừa đủ',
                        is_optional=False,
                        sort_order=sort_idx
                    )
                    db.session.add(recipe_ingredient)
                
                # Create recipe steps
                instructions = recipe_data.get('instructions', [])
                for step_idx, instruction in enumerate(instructions, 1):
                    # Extract title from instruction if it starts with "Bước X:"
                    title = None
                    description = instruction
                    
                    match = re.match(r'Bước\s+\d+:\s*(.+)', instruction)
                    if match:
                        # If instruction has "Bước X: Title. Description" format
                        content = match.group(1)
                        parts = content.split('.', 1)
                        if len(parts) > 1:
                            title = parts[0].strip()
                            description = parts[1].strip()
                        else:
                            description = content
                    
                    step = RecipeStep(
                        id=str(uuid.uuid4()),
                        recipe_id=recipe.id,
                        step_number=step_idx,
                        title=title,
                        description=description,
                        image_url=None,
                        duration_minutes=None,
                        tip=None
                    )
                    db.session.add(step)
                    created_steps += 1
                
                # Commit every 10 recipes to avoid memory issues
                if idx % 10 == 0:
                    db.session.commit()
                    print(f"  ✓ Processed {idx}/{len(recipes_data)} recipes...")
            
            except Exception as e:
                print(f"  ✗ Error processing recipe '{recipe_data.get('name', 'unknown')}': {e}")
                db.session.rollback()
                continue
        
        # Final commit
        db.session.commit()
        
        # Print statistics
        print(f"\n✅ Successfully imported:")
        print(f"   • {created_recipes} recipes")
        print(f"   • {created_ingredients} new ingredients")
        print(f"   • {created_steps} recipe steps")
        print(f"   • Total unique ingredients: {len(ingredient_cache)}")
        
        print(f"\n📊 Ingredients by category:")
        for slug, count in category_stats.items():
            if count > 0:
                category = categories[slug]
                print(f"   {category.icon} {category.name}: {count} ingredients")


if __name__ == '__main__':
    seed_recipes()
