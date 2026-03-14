"""Ingredient service - Business logic"""
import uuid
from app.extensions import db
from app.models.ingredient import Ingredient, IngredientCategory


class IngredientService:
    """Service for ingredient operations"""

    @staticmethod
    def get_all_ingredients(page=1, per_page=20, category_id=None, is_popular=None, search=None):
        """
        Get all ingredients with optional filtering
        
        Args:
            page: Page number (default: 1)
            per_page: Items per page (default: 20)
            category_id: Filter by category ID
            is_popular: Filter by popular status
            search: Search by name or aliases
        
        Returns:
            Tuple of (ingredients list, total count)
        """
        query = Ingredient.query
        
        # Apply filters
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if is_popular is not None:
            query = query.filter_by(is_popular=is_popular)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                db.or_(
                    Ingredient.name.ilike(search_term),
                    Ingredient.aliases.astext.ilike(search_term)
                )
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination
        ingredients = query.order_by(Ingredient.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        ).items
        
        return [ing.to_dict() for ing in ingredients], total

    @staticmethod
    def get_ingredient_by_id(ingredient_id):
        """
        Get ingredient by ID
        
        Args:
            ingredient_id: Ingredient UUID
        
        Returns:
            Ingredient dict or None
        """
        ingredient = Ingredient.query.get(ingredient_id)
        return ingredient.to_dict() if ingredient else None

    @staticmethod
    def get_popular_ingredients(limit=10):
        """
        Get popular ingredients
        
        Args:
            limit: Maximum number of items
        
        Returns:
            List of ingredient dicts
        """
        ingredients = Ingredient.query.filter_by(is_popular=True).limit(limit).all()
        return [ing.to_dict() for ing in ingredients]

    @staticmethod
    def get_ingredients_by_category(category_id, limit=None):
        """
        Get ingredients by category
        
        Args:
            category_id: Category UUID
            limit: Maximum number of items
        
        Returns:
            List of ingredient dicts
        """
        query = Ingredient.query.filter_by(category_id=category_id).order_by(Ingredient.name)
        
        if limit:
            query = query.limit(limit)
        
        ingredients = query.all()
        return [ing.to_dict(include_category=False) for ing in ingredients]

    @staticmethod
    def create_ingredient(name, icon, category_id, image_url=None, is_popular=False, aliases=None):
        """
        Create a new ingredient
        
        Args:
            name: Ingredient name
            icon: Emoji icon
            category_id: Category UUID
            image_url: Optional image URL
            is_popular: Whether ingredient is popular
            aliases: List of alternative names
        
        Returns:
            New ingredient dict
        """
        # Check if ingredient already exists
        existing = Ingredient.query.filter_by(name=name).first()
        if existing:
            raise ValueError(f"Ingredient '{name}' already exists")
        
        # Check if category exists
        category = IngredientCategory.query.get(category_id)
        if not category:
            raise ValueError(f"Category '{category_id}' not found")
        
        ingredient = Ingredient(
            id=str(uuid.uuid4()),
            name=name,
            icon=icon,
            category_id=category_id,
            image_url=image_url,
            is_popular=is_popular,
            aliases=aliases or []
        )
        
        db.session.add(ingredient)
        db.session.commit()
        
        return ingredient.to_dict()

    @staticmethod
    def update_ingredient(ingredient_id, **kwargs):
        """
        Update an ingredient
        
        Args:
            ingredient_id: Ingredient UUID
            **kwargs: Fields to update
        
        Returns:
            Updated ingredient dict
        """
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            raise ValueError(f"Ingredient '{ingredient_id}' not found")
        
        # Validate category if changing it
        if 'category_id' in kwargs:
            category = IngredientCategory.query.get(kwargs['category_id'])
            if not category:
                raise ValueError(f"Category '{kwargs['category_id']}' not found")
        
        # Update fields
        allowed_fields = {'name', 'icon', 'category_id', 'image_url', 'is_popular', 'aliases'}
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(ingredient, key, value)
        
        db.session.commit()
        return ingredient.to_dict()

    @staticmethod
    def delete_ingredient(ingredient_id):
        """
        Delete an ingredient
        
        Args:
            ingredient_id: Ingredient UUID
        
        Returns:
            Success message
        """
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            raise ValueError(f"Ingredient '{ingredient_id}' not found")
        
        db.session.delete(ingredient)
        db.session.commit()
        
        return {"message": f"Ingredient '{ingredient.name}' deleted successfully"}

    @staticmethod
    def bulk_create_ingredients(ingredients_data):
        """
        Create multiple ingredients at once
        
        Args:
            ingredients_data: List of ingredient dicts
        
        Returns:
            List of created ingredient dicts
        """
        created = []
        
        try:
            for data in ingredients_data:
                category = IngredientCategory.query.get(data['category_id'])
                if not category:
                    raise ValueError(f"Category '{data['category_id']}' not found")
                
                ingredient = Ingredient(
                    id=str(uuid.uuid4()),
                    name=data['name'],
                    icon=data['icon'],
                    category_id=data['category_id'],
                    image_url=data.get('image_url'),
                    is_popular=data.get('is_popular', False),
                    aliases=data.get('aliases', [])
                )
                
                db.session.add(ingredient)
                created.append(ingredient.to_dict())
            
            db.session.commit()
            return created
        
        except Exception as e:
            db.session.rollback()
            raise e


class IngredientCategoryService:
    """Service for ingredient category operations"""

    @staticmethod
    def get_all_categories():
        """
        Get all ingredient categories
        
        Returns:
            List of category dicts
        """
        categories = IngredientCategory.query.order_by(IngredientCategory.sort_order).all()
        return [cat.to_dict() for cat in categories]

    @staticmethod
    def get_category_by_id(category_id):
        """
        Get category by ID
        
        Args:
            category_id: Category UUID
        
        Returns:
            Category dict or None
        """
        category = IngredientCategory.query.get(category_id)
        return category.to_dict() if category else None

    @staticmethod
    def get_category_by_slug(slug):
        """
        Get category by slug
        
        Args:
            slug: Category slug
        
        Returns:
            Category dict or None
        """
        category = IngredientCategory.query.filter_by(slug=slug).first()
        return category.to_dict() if category else None

    @staticmethod
    def create_category(slug, name, icon=None, sort_order=0):
        """
        Create a new category
        
        Args:
            slug: Unique slug
            name: Category name
            icon: Emoji icon
            sort_order: Display order
        
        Returns:
            New category dict
        """
        # Check if category already exists
        existing = IngredientCategory.query.filter_by(slug=slug).first()
        if existing:
            raise ValueError(f"Category with slug '{slug}' already exists")
        
        category = IngredientCategory(
            id=str(uuid.uuid4()),
            slug=slug,
            name=name,
            icon=icon,
            sort_order=sort_order
        )
        
        db.session.add(category)
        db.session.commit()
        
        return category.to_dict()

    @staticmethod
    def update_category(category_id, **kwargs):
        """
        Update a category
        
        Args:
            category_id: Category UUID
            **kwargs: Fields to update
        
        Returns:
            Updated category dict
        """
        category = IngredientCategory.query.get(category_id)
        if not category:
            raise ValueError(f"Category '{category_id}' not found")
        
        allowed_fields = {'slug', 'name', 'icon', 'sort_order'}
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(category, key, value)
        
        db.session.commit()
        return category.to_dict()

    @staticmethod
    def delete_category(category_id):
        """
        Delete a category
        
        Args:
            category_id: Category UUID
        
        Returns:
            Success message
        """
        category = IngredientCategory.query.get(category_id)
        if not category:
            raise ValueError(f"Category '{category_id}' not found")
        
        # Check if category has ingredients
        if category.ingredients.count() > 0:
            raise ValueError(f"Cannot delete category '{category.name}' - it has ingredients")
        
        db.session.delete(category)
        db.session.commit()
        
        return {"message": f"Category '{category.name}' deleted successfully"}
