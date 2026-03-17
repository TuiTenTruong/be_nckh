"""Recipe services - Business logic"""
import uuid
from app.extensions import db
from app.models.recipe import Recipe
from app.models.recipeIngredient import RecipeIngredient
from app.models.recipeStep import RecipeStep
from app.models.ingredient import Ingredient


class RecipeService:
    """Service for recipe operations"""

    @staticmethod
    def get_all_recipes(page=1, per_page=20, search=None, difficulty=None, is_featured=None):
        """Get recipes with pagination and optional filters"""
        query = Recipe.query

        if search:
            search_term = f"%{search}%"
            query = query.filter(Recipe.name.ilike(search_term))

        if difficulty:
            query = query.filter_by(difficulty=difficulty)

        if is_featured is not None:
            query = query.filter_by(is_featured=is_featured)

        total = query.count()

        recipes = query.order_by(Recipe.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        ).items

        return [recipe.to_dict() for recipe in recipes], total

    @staticmethod
    def get_random_recipes(limit=4):
        """Get random recipes from database"""
        recipes = Recipe.query.order_by(db.func.rand()).limit(limit).all()
        return [recipe.to_dict() for recipe in recipes]

    @staticmethod
    def get_recipe_by_id(recipe_id, include_ingredients=True, include_steps=True):
        """Get a recipe by ID"""
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return None

        return recipe.to_dict(
            include_ingredients=include_ingredients,
            include_steps=include_steps
        )

    @staticmethod
    def create_recipe(
        name,
        description,
        image_url,
        cook_time_minutes,
        difficulty,
        servings=2,
        cuisine_type=None,
        diet_tags=None,
        is_featured=False,
        ingredients=None,
        steps=None
    ):
        """Create a recipe with optional ingredients and steps"""
        recipe = Recipe(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            image_url=image_url,
            cook_time_minutes=cook_time_minutes,
            difficulty=difficulty,
            servings=servings,
            cuisine_type=cuisine_type,
            diet_tags=diet_tags or [],
            is_featured=is_featured
        )

        db.session.add(recipe)

        try:
            if ingredients:
                RecipeService._upsert_recipe_ingredients(recipe.id, ingredients, clear_existing=False)

            if steps:
                RecipeService._upsert_recipe_steps(recipe.id, steps, clear_existing=False)

            db.session.commit()
            return recipe.to_dict(include_ingredients=True, include_steps=True)

        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def update_recipe(recipe_id, **kwargs):
        """Update recipe and optionally replace ingredients/steps"""
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            raise ValueError(f"Recipe '{recipe_id}' not found")

        allowed_fields = {
            'name',
            'description',
            'image_url',
            'cook_time_minutes',
            'difficulty',
            'servings',
            'cuisine_type',
            'diet_tags',
            'is_featured',
            'total_favorites',
            'total_views'
        }

        ingredients = kwargs.pop('ingredients', None)
        steps = kwargs.pop('steps', None)

        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(recipe, key, value)

        try:
            if ingredients is not None:
                RecipeService._upsert_recipe_ingredients(recipe_id, ingredients, clear_existing=True)

            if steps is not None:
                RecipeService._upsert_recipe_steps(recipe_id, steps, clear_existing=True)

            db.session.commit()
            return recipe.to_dict(include_ingredients=True, include_steps=True)

        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def delete_recipe(recipe_id):
        """Delete recipe by ID"""
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            raise ValueError(f"Recipe '{recipe_id}' not found")

        db.session.delete(recipe)
        db.session.commit()
        return {'message': f"Recipe '{recipe.name}' deleted successfully"}

    @staticmethod
    def get_recipe_ingredients(recipe_id):
        """Get all ingredients for a recipe"""
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            raise ValueError(f"Recipe '{recipe_id}' not found")

        items = recipe.recipe_ingredients.order_by(RecipeIngredient.sort_order.asc()).all()
        return [item.to_dict(include_ingredient=True) for item in items]

    @staticmethod
    def add_recipe_ingredient(recipe_id, ingredient_name, amount, ingredient_id=None, is_optional=False, sort_order=0):
        """Add one ingredient row to recipe_ingredients"""
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            raise ValueError(f"Recipe '{recipe_id}' not found")

        if ingredient_id:
            ingredient = Ingredient.query.get(ingredient_id)
            if not ingredient:
                raise ValueError(f"Ingredient '{ingredient_id}' not found")

        row = RecipeIngredient(
            id=str(uuid.uuid4()),
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            ingredient_name=ingredient_name,
            amount=amount,
            is_optional=is_optional,
            sort_order=sort_order
        )

        db.session.add(row)
        db.session.commit()
        return row.to_dict(include_ingredient=True)

    @staticmethod
    def update_recipe_ingredient(recipe_id, recipe_ingredient_id, **kwargs):
        """Update one ingredient row in recipe_ingredients"""
        row = RecipeIngredient.query.filter_by(id=recipe_ingredient_id, recipe_id=recipe_id).first()
        if not row:
            raise ValueError(f"Recipe ingredient '{recipe_ingredient_id}' not found")

        if 'ingredient_id' in kwargs and kwargs['ingredient_id']:
            ingredient = Ingredient.query.get(kwargs['ingredient_id'])
            if not ingredient:
                raise ValueError(f"Ingredient '{kwargs['ingredient_id']}' not found")

        allowed_fields = {'ingredient_id', 'ingredient_name', 'amount', 'is_optional', 'sort_order'}
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(row, key, value)

        db.session.commit()
        return row.to_dict(include_ingredient=True)

    @staticmethod
    def delete_recipe_ingredient(recipe_id, recipe_ingredient_id):
        """Delete one ingredient row from recipe_ingredients"""
        row = RecipeIngredient.query.filter_by(id=recipe_ingredient_id, recipe_id=recipe_id).first()
        if not row:
            raise ValueError(f"Recipe ingredient '{recipe_ingredient_id}' not found")

        db.session.delete(row)
        db.session.commit()
        return {'message': 'Recipe ingredient deleted successfully'}

    @staticmethod
    def get_recipe_steps(recipe_id):
        """Get all steps of a recipe"""
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            raise ValueError(f"Recipe '{recipe_id}' not found")

        steps = RecipeStep.query.filter_by(recipe_id=recipe_id).order_by(RecipeStep.step_number.asc()).all()
        return [step.to_dict() for step in steps]

    @staticmethod
    def add_recipe_step(recipe_id, description, title=None, image_url=None, duration_minutes=None, tip=None, step_number=None):
        """Add one step to recipe_steps"""
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            raise ValueError(f"Recipe '{recipe_id}' not found")

        if step_number is None:
            current_count = RecipeStep.query.filter_by(recipe_id=recipe_id).count()
            step_number = current_count + 1

        step = RecipeStep(
            id=str(uuid.uuid4()),
            recipe_id=recipe_id,
            step_number=step_number,
            title=title,
            description=description,
            image_url=image_url,
            duration_minutes=duration_minutes,
            tip=tip
        )

        db.session.add(step)
        db.session.commit()
        return step.to_dict()

    @staticmethod
    def update_recipe_step(recipe_id, step_id, **kwargs):
        """Update one step in recipe_steps"""
        step = RecipeStep.query.filter_by(id=step_id, recipe_id=recipe_id).first()
        if not step:
            raise ValueError(f"Recipe step '{step_id}' not found")

        allowed_fields = {'step_number', 'title', 'description', 'image_url', 'duration_minutes', 'tip'}
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(step, key, value)

        db.session.commit()
        return step.to_dict()

    @staticmethod
    def delete_recipe_step(recipe_id, step_id):
        """Delete one step from recipe_steps"""
        step = RecipeStep.query.filter_by(id=step_id, recipe_id=recipe_id).first()
        if not step:
            raise ValueError(f"Recipe step '{step_id}' not found")

        db.session.delete(step)
        db.session.commit()
        return {'message': 'Recipe step deleted successfully'}

    @staticmethod
    def _upsert_recipe_ingredients(recipe_id, ingredients, clear_existing=False):
        """Insert or replace recipe ingredients in bulk"""
        if clear_existing:
            RecipeIngredient.query.filter_by(recipe_id=recipe_id).delete()

        for index, item in enumerate(ingredients):
            ingredient_id = item.get('ingredient_id')
            if ingredient_id:
                ingredient = Ingredient.query.get(ingredient_id)
                if not ingredient:
                    raise ValueError(f"Ingredient '{ingredient_id}' not found")

            amount = item.get('amount')

            row = RecipeIngredient(
                id=str(uuid.uuid4()),
                recipe_id=recipe_id,
                ingredient_id=ingredient_id,
                amount=amount,
                is_optional=item.get('is_optional', False),
                sort_order=item.get('sort_order', index)
            )
            db.session.add(row)

    @staticmethod
    def _upsert_recipe_steps(recipe_id, steps, clear_existing=False):
        """Insert or replace recipe steps in bulk"""
        if clear_existing:
            RecipeStep.query.filter_by(recipe_id=recipe_id).delete()

        for index, item in enumerate(steps):
            description = item.get('description')
            if not description:
                raise ValueError('Each step needs description')

            step = RecipeStep(
                id=str(uuid.uuid4()),
                recipe_id=recipe_id,
                step_number=item.get('step_number', index + 1),
                title=item.get('title'),
                description=description,
                image_url=item.get('image_url'),
                duration_minutes=item.get('duration_minutes'),
                tip=item.get('tip')
            )
            db.session.add(step)
