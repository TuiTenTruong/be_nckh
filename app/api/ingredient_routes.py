"""Ingredient API routes"""
from flask import Blueprint, request
from app.services.ingredient_service import IngredientService, IngredientCategoryService
from app.utils.response import success_response, error_response, paginated_response, handle_api_error

# Create blueprints
ingredient_bp = Blueprint('ingredients', __name__, url_prefix='/api/ingredients')
category_bp = Blueprint('categories', __name__, url_prefix='/api/categories')


@ingredient_bp.route('', methods=['GET'])
@handle_api_error
def list_ingredients():
    """
    Get all ingredients with pagination and filtering
    ---
    tags:
      - Ingredients
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: Page number
      - name: per_page
        in: query
        type: integer
        default: 20
        description: Items per page (max 100)
      - name: category_id
        in: query
        type: string
        description: Filter by category UUID
      - name: is_popular
        in: query
        type: boolean
        description: Filter by popular status
      - name: search
        in: query
        type: string
        description: Search by ingredient name
    responses:
      200:
        description: List of ingredients with pagination
      400:
        description: Invalid parameters
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        category_id = request.args.get('category_id', type=str)
        is_popular = request.args.get('is_popular', type=lambda x: x.lower() == 'true' if x else None)
        search = request.args.get('search', type=str)
        
        # Validate pagination
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        ingredients, total = IngredientService.get_all_ingredients(
            page=page,
            per_page=per_page,
            category_id=category_id,
            is_popular=is_popular,
            search=search
        )
        
        return paginated_response(
            items=ingredients,
            total=total,
            page=page,
            per_page=per_page,
            message="Ingredients retrieved successfully"
        )
    
    except Exception as e:
        return error_response(str(e), 400)


@ingredient_bp.route('/<ingredient_id>', methods=['GET'])
@handle_api_error
def get_ingredient(ingredient_id):
    """
    Get a single ingredient by ID
    ---
    tags:
      - Ingredients
    parameters:
      - name: ingredient_id
        in: path
        type: string
        required: true
        description: Ingredient UUID
    responses:
      200:
        description: Ingredient details
      404:
        description: Ingredient not found
    """
    try:
        ingredient = IngredientService.get_ingredient_by_id(ingredient_id)
        
        if not ingredient:
            return error_response("Ingredient not found", 404)
        
        return success_response(data=ingredient, message="Ingredient retrieved successfully")
    
    except Exception as e:
        return error_response(str(e), 400)


@ingredient_bp.route('/popular', methods=['GET'])
@handle_api_error
def get_popular_ingredients():
    """
    Get popular ingredients
    ---
    tags:
      - Ingredients
    parameters:
      - name: limit
        in: query
        type: integer
        default: 10
        description: Maximum number of ingredients to return
    responses:
      200:
        description: List of popular ingredients
      400:
        description: Invalid parameters
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        
        if limit < 1 or limit > 100:
            limit = 10
        
        ingredients = IngredientService.get_popular_ingredients(limit=limit)
        
        return success_response(
            data=ingredients,
            message="Popular ingredients retrieved successfully"
        )
    
    except Exception as e:
        return error_response(str(e), 400)


@ingredient_bp.route('/category/<category_id>', methods=['GET'])
@handle_api_error
def get_ingredients_by_category(category_id):
    """
    Get ingredients by category
    ---
    tags:
      - Ingredients
    parameters:
      - name: category_id
        in: path
        type: string
        required: true
        description: Category UUID
      - name: limit
        in: query
        type: integer
        description: Maximum number of ingredients to return
    responses:
      200:
        description: List of ingredients in category
      404:
        description: Category not found
    """
    try:
        limit = request.args.get('limit', type=int)
        ingredients = IngredientService.get_ingredients_by_category(category_id, limit=limit)
        
        return success_response(
            data=ingredients,
            message="Ingredients by category retrieved successfully"
        )
    
    except Exception as e:
        return error_response(str(e), 400)


@ingredient_bp.route('', methods=['POST'])
@handle_api_error
def create_ingredient():
    """
    Create a new ingredient
    ---
    tags:
      - Ingredients
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - icon
            - category_id
          properties:
            name:
              type: string
              example: "Tomato"
            icon:
              type: string
              example: "🍅"
            category_id:
              type: string
              description: Category UUID
              example: "550e8400-e29b-41d4-a716-446655440000"
            image_url:
              type: string
              example: "https://example.com/tomato.jpg"
            is_popular:
              type: boolean
              default: false
            aliases:
              type: array
              items:
                type: string
              example: ["Tomatoes", "Cherry tomato"]
    responses:
      201:
        description: Ingredient created successfully
      400:
        description: Invalid input or missing required fields
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body is empty", 400)
        
        # Validate required fields
        required_fields = ['name', 'icon', 'category_id']
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}", 400)
        
        ingredient = IngredientService.create_ingredient(
            name=data['name'],
            icon=data['icon'],
            category_id=data['category_id'],
            image_url=data.get('image_url'),
            is_popular=data.get('is_popular', False),
            aliases=data.get('aliases')
        )
        
        return success_response(
            data=ingredient,
            message="Ingredient created successfully",
            status_code=201
        )
    
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@ingredient_bp.route('/<ingredient_id>', methods=['PUT'])
@handle_api_error
def update_ingredient(ingredient_id):
    """
    Update an ingredient
    ---
    tags:
      - Ingredients
    parameters:
      - name: ingredient_id
        in: path
        type: string
        required: true
        description: Ingredient UUID
      - name: body
        in: body
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Tomato"
            icon:
              type: string
              example: "🍅"
            category_id:
              type: string
              description: Category UUID
            image_url:
              type: string
            is_popular:
              type: boolean
            aliases:
              type: array
              items:
                type: string
    responses:
      200:
        description: Ingredient updated successfully
      400:
        description: Invalid input
      404:
        description: Ingredient not found
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body is empty", 400)
        
        ingredient = IngredientService.update_ingredient(ingredient_id, **data)
        
        return success_response(
            data=ingredient,
            message="Ingredient updated successfully"
        )
    
    except ValueError as e:
        return error_response(str(e), 400 if "not found" not in str(e) else 404)
    except Exception as e:
        return error_response(str(e), 500)


@ingredient_bp.route('/<ingredient_id>', methods=['DELETE'])
@handle_api_error
def delete_ingredient(ingredient_id):
    """
    Delete an ingredient
    ---
    tags:
      - Ingredients
    parameters:
      - name: ingredient_id
        in: path
        type: string
        required: true
        description: Ingredient UUID
    responses:
      200:
        description: Ingredient deleted successfully
      404:
        description: Ingredient not found
    """
    try:
        result = IngredientService.delete_ingredient(ingredient_id)
        
        return success_response(
            data=result,
            message="Ingredient deleted successfully"
        )
    
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(str(e), 500)


@ingredient_bp.route('/bulk/create', methods=['POST'])
@handle_api_error
def bulk_create_ingredients():
    """
    Create multiple ingredients at once
    ---
    tags:
      - Ingredients
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: array
          items:
            type: object
            required:
              - name
              - icon
              - category_id
            properties:
              name:
                type: string
                example: "Tomato"
              icon:
                type: string
                example: "🍅"
              category_id:
                type: string
                description: Category UUID
              image_url:
                type: string
              is_popular:
                type: boolean
              aliases:
                type: array
                items:
                  type: string
    responses:
      201:
        description: Ingredients created successfully
      400:
        description: Invalid input or empty array
    """
    try:
        data = request.get_json()
        
        if not data or not isinstance(data, list):
            return error_response("Request body must be an array of ingredients", 400)
        
        if len(data) == 0:
            return error_response("Request body cannot be empty", 400)
        
        ingredients = IngredientService.bulk_create_ingredients(data)
        
        return success_response(
            data=ingredients,
            message=f"{len(ingredients)} ingredients created successfully",
            status_code=201
        )
    
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


# ============================================================================
# CATEGORY ROUTES
# ============================================================================

@category_bp.route('', methods=['GET'])
@handle_api_error
def list_categories():
    """
    Get all ingredient categories
    ---
    tags:
      - Categories
    responses:
      200:
        description: List of all ingredient categories
    """
    try:
        categories = IngredientCategoryService.get_all_categories()
        
        return success_response(
            data=categories,
            message="Categories retrieved successfully"
        )
    
    except Exception as e:
        return error_response(str(e), 400)


@category_bp.route('/<category_id>', methods=['GET'])
@handle_api_error
def get_category(category_id):
    """
    Get a single category by ID
    ---
    tags:
      - Categories
    parameters:
      - name: category_id
        in: path
        type: string
        required: true
        description: Category UUID
    responses:
      200:
        description: Category details
      404:
        description: Category not found
    """
    try:
        category = IngredientCategoryService.get_category_by_id(category_id)
        
        if not category:
            return error_response("Category not found", 404)
        
        return success_response(data=category, message="Category retrieved successfully")
    
    except Exception as e:
        return error_response(str(e), 400)


@category_bp.route('/slug/<slug>', methods=['GET'])
@handle_api_error
def get_category_by_slug(slug):
    """
    Get a category by slug
    ---
    tags:
      - Categories
    parameters:
      - name: slug
        in: path
        type: string
        required: true
        description: Category slug (e.g., 'protein', 'vegetable')
    responses:
      200:
        description: Category details
      404:
        description: Category not found
    """
    try:
        category = IngredientCategoryService.get_category_by_slug(slug)
        
        if not category:
            return error_response("Category not found", 404)
        
        return success_response(data=category, message="Category retrieved successfully")
    
    except Exception as e:
        return error_response(str(e), 400)


@category_bp.route('', methods=['POST'])
@handle_api_error
def create_category():
    """
    Create a new category
    ---
    tags:
      - Categories
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - slug
            - name
          properties:
            slug:
              type: string
              description: Unique slug (e.g., 'protein', 'vegetable')
              example: "protein"
            name:
              type: string
              example: "Protein"
            icon:
              type: string
              example: "🍗"
            sort_order:
              type: integer
              default: 0
              example: 1
    responses:
      201:
        description: Category created successfully
      400:
        description: Invalid input or missing required fields
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body is empty", 400)
        
        # Validate required fields
        required_fields = ['slug', 'name']
        for field in required_fields:
            if field not in data:
                return error_response(f"Missing required field: {field}", 400)
        
        category = IngredientCategoryService.create_category(
            slug=data['slug'],
            name=data['name'],
            icon=data.get('icon'),
            sort_order=data.get('sort_order', 0)
        )
        
        return success_response(
            data=category,
            message="Category created successfully",
            status_code=201
        )
    
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)


@category_bp.route('/<category_id>', methods=['PUT'])
@handle_api_error
def update_category(category_id):
    """
    Update a category
    ---
    tags:
      - Categories
    parameters:
      - name: category_id
        in: path
        type: string
        required: true
        description: Category UUID
      - name: body
        in: body
        schema:
          type: object
          properties:
            slug:
              type: string
              example: "protein"
            name:
              type: string
              example: "Protein"
            icon:
              type: string
              example: "🍗"
            sort_order:
              type: integer
              example: 1
    responses:
      200:
        description: Category updated successfully
      400:
        description: Invalid input
      404:
        description: Category not found
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Request body is empty", 400)
        
        category = IngredientCategoryService.update_category(category_id, **data)
        
        return success_response(
            data=category,
            message="Category updated successfully"
        )
    
    except ValueError as e:
        return error_response(str(e), 400 if "not found" not in str(e) else 404)
    except Exception as e:
        return error_response(str(e), 500)


@category_bp.route('/<category_id>', methods=['DELETE'])
@handle_api_error
def delete_category(category_id):
    """
    Delete a category
    ---
    tags:
      - Categories
    parameters:
      - name: category_id
        in: path
        type: string
        required: true
        description: Category UUID
    responses:
      200:
        description: Category deleted successfully
      404:
        description: Category not found
    """
    try:
        result = IngredientCategoryService.delete_category(category_id)
        
        return success_response(
            data=result,
            message="Category deleted successfully"
        )
    
    except ValueError as e:
        return error_response(str(e), 404 if "not found" in str(e) else 400)
    except Exception as e:
        return error_response(str(e), 500)
