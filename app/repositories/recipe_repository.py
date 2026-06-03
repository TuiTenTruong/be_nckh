"""Recipe repository - Database query layer"""
from app.models.recipe import Recipe
from app.models.recipeIngredient import RecipeIngredient
from app.models.recipeStep import RecipeStep
from app.models.ingredient import Ingredient


class RecipeRepository:
    """Repository for Recipe database operations"""
    
    @staticmethod
    def get_all_recipes():
        """
        Lấy tất cả công thức từ database
        Join với RecipeIngredient và Ingredient để lấy đầy đủ thông tin
        
        Returns:
            list: Danh sách Recipe objects
        """
        recipes = Recipe.query.all()
        return recipes
    
    @staticmethod
    def get_recipe_by_id(recipe_id):
        """
        Lấy một công thức theo ID
        
        Args:
            recipe_id (str): ID của recipe
            
        Returns:
            Recipe: Recipe object hoặc None
        """
        return Recipe.query.get(recipe_id)
    
    @staticmethod
    def get_recipes_with_ingredients(limit=None):
        """
        Lấy danh sách recipes kèm ingredients
        Optimize query bằng cách eager load relationships
        
        Args:
            limit (int, optional): Giới hạn số lượng recipes
            
        Returns:
            list: Danh sách Recipe objects với ingredients đã được load
        """
        query = Recipe.query
        
        if limit:
            query = query.limit(limit)
        
        recipes = query.all()
        
        # Eager load ingredients để tránh N+1 query problem
        for recipe in recipes:
            # Access relationships để trigger loading
            _ = recipe.recipe_ingredients.all()
        
        return recipes
    
    @staticmethod
    def get_recipe_ingredients(recipe_id):
        """
        Lấy tất cả ingredients của một recipe
        
        Args:
            recipe_id (str): ID của recipe
            
        Returns:
            list: Danh sách RecipeIngredient objects
        """
        return RecipeIngredient.query.filter_by(
            recipe_id=recipe_id
        ).order_by(
            RecipeIngredient.sort_order
        ).all()
    
    @staticmethod
    def get_recipe_steps(recipe_id):
        """
        Lấy tất cả steps của một recipe
        
        Args:
            recipe_id (str): ID của recipe
            
        Returns:
            list: Danh sách RecipeStep objects
        """
        return RecipeStep.query.filter_by(
            recipe_id=recipe_id
        ).order_by(
            RecipeStep.step_number
        ).all()
    
    @staticmethod
    def search_recipes_by_ingredients(ingredient_names, limit=None):
        """
        Tìm kiếm recipes có chứa các ingredients được chỉ định
        
        Args:
            ingredient_names (list): Danh sách tên ingredients
            limit (int, optional): Giới hạn kết quả
            
        Returns:
            list: Danh sách Recipe objects
        """
        # Join Recipe -> RecipeIngredient -> Ingredient
        query = Recipe.query.join(
            RecipeIngredient, Recipe.id == RecipeIngredient.recipe_id
        ).join(
            Ingredient, RecipeIngredient.ingredient_id == Ingredient.id
        ).filter(
            Ingredient.name.in_(ingredient_names)
        ).distinct()
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_featured_recipes(limit=10):
        """
        Lấy các công thức nổi bật
        
        Args:
            limit (int): Số lượng recipes
            
        Returns:
            list: Danh sách Recipe objects
        """
        return Recipe.query.filter_by(
            is_featured=True
        ).limit(limit).all()
