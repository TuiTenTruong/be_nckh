"""Recipe API routes"""
from flask import Blueprint, request
from app.services.recipe_service import RecipeService
from app.utils.response import success_response, error_response, paginated_response, handle_api_error


recipe_bp = Blueprint('recipes', __name__, url_prefix='/api/recipes')


@recipe_bp.route('', methods=['GET'])
@handle_api_error
def list_recipes():
    """
    Get recipes with pagination and filtering
    ---
    tags:
      - Recipes
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
      - name: search
        in: query
        type: string
        description: Search by recipe name
      - name: difficulty
        in: query
        type: string
        description: Filter by difficulty (Easy, Medium, Hard)
      - name: is_featured
        in: query
        type: boolean
        description: Filter by featured status
    responses:
      200:
        description: List of recipes with pagination
      400:
        description: Invalid parameters
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', type=str)
    difficulty = request.args.get('difficulty', type=str)
    is_featured = request.args.get('is_featured', type=lambda x: x.lower() == 'true' if x else None)

    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 20

    recipes, total = RecipeService.get_all_recipes(
        page=page,
        per_page=per_page,
        search=search,
        difficulty=difficulty,
        is_featured=is_featured
    )

    return paginated_response(
        items=recipes,
        total=total,
        page=page,
        per_page=per_page,
        message='Recipes retrieved successfully'
    )


@recipe_bp.route('/<recipe_id>', methods=['GET'])
@handle_api_error
def get_recipe(recipe_id):
    """
    Get recipe detail by ID
    ---
    tags:
      - Recipes
    parameters:
      - name: recipe_id
        in: path
        type: string
        required: true
        description: Recipe UUID
      - name: include_ingredients
        in: query
        type: boolean
        default: true
        description: Include ingredients in response
      - name: include_steps
        in: query
        type: boolean
        default: true
        description: Include cooking steps in response
    responses:
      200:
        description: Recipe details
      404:
        description: Recipe not found
    """
    include_ingredients = request.args.get('include_ingredients', 'true').lower() == 'true'
    include_steps = request.args.get('include_steps', 'true').lower() == 'true'

    recipe = RecipeService.get_recipe_by_id(
        recipe_id,
        include_ingredients=include_ingredients,
        include_steps=include_steps
    )
    if not recipe:
        return error_response('Recipe not found', 404)

    return success_response(data=recipe, message='Recipe retrieved successfully')


@recipe_bp.route('/random', methods=['GET'])
@handle_api_error
def get_random_recipes():
    """
    Get random recipes
    ---
    tags:
      - Recipes
    parameters:
      - name: limit
        in: query
        type: integer
        default: 4
        description: Maximum number of recipes to return
    responses:
      200:
        description: Random recipes list
      400:
        description: Invalid parameters
    """
    limit = request.args.get('limit', 4, type=int)
    if limit < 1 or limit > 100:
        limit = 4

    recipes = RecipeService.get_random_recipes(limit=limit)
    return success_response(data=recipes, message='Random recipes retrieved successfully')


@recipe_bp.route('', methods=['POST'])
@handle_api_error
def create_recipe():
    """
    Create a new recipe with optional ingredients and steps
    ---
    tags:
      - Recipes
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - description
            - image_url
            - cook_time_minutes
            - difficulty
          properties:
            name:
              type: string
              example: "Spaghetti Carbonara"
            description:
              type: string
              example: "Classic Italian pasta dish"
            image_url:
              type: string
              example: "https://example.com/carbonara.jpg"
            cook_time_minutes:
              type: integer
              example: 30
            difficulty:
              type: string
              enum: ["Easy", "Medium", "Hard"]
              example: "Medium"
            servings:
              type: integer
              default: 2
              example: 2
            cuisine_type:
              type: string
              example: "Italian"
            diet_tags:
              type: array
              items:
                type: string
              example: ["Vegetarian", "Dairy-free"]
            is_featured:
              type: boolean
              default: false
            ingredients:
              type: array
              items:
                type: object
            steps:
              type: array
              items:
                type: object
    responses:
      201:
        description: Recipe created successfully
      400:
        description: Invalid input or missing required fields
    """
    data = request.get_json()
    if not data:
        return error_response('Request body is empty', 400)

    required_fields = ['name', 'description', 'image_url', 'cook_time_minutes', 'difficulty']
    for field in required_fields:
        if field not in data:
            return error_response(f'Missing required field: {field}', 400)

    recipe = RecipeService.create_recipe(
        name=data['name'],
        description=data['description'],
        image_url=data['image_url'],
        cook_time_minutes=data['cook_time_minutes'],
        difficulty=data['difficulty'],
        servings=data.get('servings', 2),
        cuisine_type=data.get('cuisine_type'),
        diet_tags=data.get('diet_tags', []),
        is_featured=data.get('is_featured', False),
        ingredients=data.get('ingredients'),
        steps=data.get('steps')
    )

    return success_response(data=recipe, message='Recipe created successfully', status_code=201)


@recipe_bp.route('/<recipe_id>', methods=['PUT'])
@handle_api_error
def update_recipe(recipe_id):
    """
    Update recipe and optionally replace ingredients/steps
    ---
    tags:
      - Recipes
    parameters:
      - name: recipe_id
        in: path
        type: string
        required: true
        description: Recipe UUID
      - name: body
        in: body
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Spaghetti Carbonara"
            description:
              type: string
            image_url:
              type: string
            cook_time_minutes:
              type: integer
            difficulty:
              type: string
            servings:
              type: integer
            cuisine_type:
              type: string
            diet_tags:
              type: array
              items:
                type: string
            is_featured:
              type: boolean
    responses:
      200:
        description: Recipe updated successfully
      400:
        description: Invalid input
      404:
        description: Recipe not found
    """
    data = request.get_json()
    if not data:
        return error_response('Request body is empty', 400)

    try:
        recipe = RecipeService.update_recipe(recipe_id, **data)
    except ValueError as exc:
        message = str(exc)
        return error_response(message, 404 if 'not found' in message else 400)

    return success_response(data=recipe, message='Recipe updated successfully')


@recipe_bp.route('/<recipe_id>', methods=['DELETE'])
@handle_api_error
def delete_recipe(recipe_id):
    """
    Delete recipe
    ---
    tags:
      - Recipes
    parameters:
      - name: recipe_id
        in: path
        type: string
        required: true
        description: Recipe UUID
    responses:
      200:
        description: Recipe deleted successfully
      404:
        description: Recipe not found
    """
    try:
        result = RecipeService.delete_recipe(recipe_id)
    except ValueError as exc:
        return error_response(str(exc), 404)

    return success_response(data=result, message='Recipe deleted successfully')


@recipe_bp.route('/<recipe_id>/ingredients', methods=['GET'])
@handle_api_error
def list_recipe_ingredients(recipe_id):
    """
    Get ingredients of one recipe from recipe_ingredients table
    ---
    tags:
      - Recipes
    parameters:
      - name: recipe_id
        in: path
        type: string
        required: true
        description: Recipe UUID
    responses:
      200:
        description: List of ingredients in the recipe
      404:
        description: Recipe not found
    """
    try:
        items = RecipeService.get_recipe_ingredients(recipe_id)
    except ValueError as exc:
        return error_response(str(exc), 404)

    return success_response(data=items, message='Recipe ingredients retrieved successfully')


@recipe_bp.route('/<recipe_id>/ingredients', methods=['POST'])
@handle_api_error
def add_recipe_ingredient(recipe_id):
    """
    Add one item to recipe_ingredients
    ---
    tags:
      - Recipes
    parameters:
      - name: recipe_id
        in: path
        type: string
        required: true
        description: Recipe UUID
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - ingredient_name
            - amount
          properties:
            ingredient_name:
              type: string
              example: "Pasta"
            amount:
              type: string
              example: "400g"
            ingredient_id:
              type: string
              description: Ingredient UUID (optional)
            is_optional:
              type: boolean
              default: false
            sort_order:
              type: integer
              default: 0
    responses:
      201:
        description: Recipe ingredient added successfully
      400:
        description: Invalid input or missing required fields
      404:
        description: Recipe not found
    """
    data = request.get_json()
    if not data:
        return error_response('Request body is empty', 400)

    required_fields = ['ingredient_name', 'amount']
    for field in required_fields:
        if field not in data:
            return error_response(f'Missing required field: {field}', 400)

    try:
        item = RecipeService.add_recipe_ingredient(
            recipe_id=recipe_id,
            ingredient_name=data['ingredient_name'],
            amount=data['amount'],
            ingredient_id=data.get('ingredient_id'),
            is_optional=data.get('is_optional', False),
            sort_order=data.get('sort_order', 0)
        )
    except ValueError as exc:
        message = str(exc)
        return error_response(message, 404 if 'not found' in message else 400)

    return success_response(data=item, message='Recipe ingredient added successfully', status_code=201)


@recipe_bp.route('/<recipe_id>/ingredients/<recipe_ingredient_id>', methods=['PUT'])
@handle_api_error
def update_recipe_ingredient(recipe_id, recipe_ingredient_id):
    """
    Update one row in recipe_ingredients
    ---
    tags:
      - Recipes
    parameters:
      - name: recipe_id
        in: path
        type: string
        required: true
        description: Recipe UUID
      - name: recipe_ingredient_id
        in: path
        type: string
        required: true
        description: RecipeIngredient UUID
      - name: body
        in: body
        schema:
          type: object
          properties:
            ingredient_name:
              type: string
            amount:
              type: string
            ingredient_id:
              type: string
            is_optional:
              type: boolean
            sort_order:
              type: integer
    responses:
      200:
        description: Recipe ingredient updated successfully
      400:
        description: Invalid input
      404:
        description: Recipe or ingredient not found
    """
    data = request.get_json()
    if not data:
        return error_response('Request body is empty', 400)

    try:
        item = RecipeService.update_recipe_ingredient(recipe_id, recipe_ingredient_id, **data)
    except ValueError as exc:
        message = str(exc)
        return error_response(message, 404 if 'not found' in message else 400)

    return success_response(data=item, message='Recipe ingredient updated successfully')


@recipe_bp.route('/<recipe_id>/ingredients/<recipe_ingredient_id>', methods=['DELETE'])
@handle_api_error
def delete_recipe_ingredient(recipe_id, recipe_ingredient_id):
    """
    Delete one row from recipe_ingredients
    ---
    tags:
      - Recipes
    parameters:
      - name: recipe_id
        in: path
        type: string
        required: true
        description: Recipe UUID
      - name: recipe_ingredient_id
        in: path
        type: string
        required: true
        description: RecipeIngredient UUID
    responses:
      200:
        description: Recipe ingredient deleted successfully
      404:
        description: Recipe or ingredient not found
    """
    try:
        result = RecipeService.delete_recipe_ingredient(recipe_id, recipe_ingredient_id)
    except ValueError as exc:
        return error_response(str(exc), 404)

    return success_response(data=result, message='Recipe ingredient deleted successfully')


@recipe_bp.route('/<recipe_id>/steps', methods=['GET'])
@handle_api_error
def list_recipe_steps(recipe_id):
    """
    Get steps of one recipe
    ---
    tags:
      - Recipes
    parameters:
      - name: recipe_id
        in: path
        type: string
        required: true
        description: Recipe UUID
    responses:
      200:
        description: List of cooking steps in the recipe
      404:
        description: Recipe not found
    """
    try:
        items = RecipeService.get_recipe_steps(recipe_id)
    except ValueError as exc:
        return error_response(str(exc), 404)

    return success_response(data=items, message='Recipe steps retrieved successfully')


@recipe_bp.route('/<recipe_id>/steps', methods=['POST'])
@handle_api_error
def add_recipe_step(recipe_id):
    """
    Add one step to recipe_steps
    ---
    tags:
      - Recipes
    parameters:
      - name: recipe_id
        in: path
        type: string
        required: true
        description: Recipe UUID
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - description
          properties:
            description:
              type: string
              example: "Boil water in a large pot"
            step_number:
              type: integer
              example: 1
            title:
              type: string
              example: "Boil water"
            image_url:
              type: string
            duration_minutes:
              type: integer
              example: 10
            tip:
              type: string
              example: "Use filtered water for better taste"
    responses:
      201:
        description: Recipe step added successfully
      400:
        description: Invalid input or missing required fields
      404:
        description: Recipe not found
    """
    data = request.get_json()
    if not data:
        return error_response('Request body is empty', 400)

    if 'description' not in data:
        return error_response('Missing required field: description', 400)

    try:
        item = RecipeService.add_recipe_step(
            recipe_id=recipe_id,
            description=data['description'],
            step_number=data.get('step_number'),
            title=data.get('title'),
            image_url=data.get('image_url'),
            duration_minutes=data.get('duration_minutes'),
            tip=data.get('tip')
        )
    except ValueError as exc:
        return error_response(str(exc), 404)

    return success_response(data=item, message='Recipe step added successfully', status_code=201)


@recipe_bp.route('/<recipe_id>/steps/<step_id>', methods=['PUT'])
@handle_api_error
def update_recipe_step(recipe_id, step_id):
    """
    Update one row in recipe_steps
    ---
    tags:
      - Recipes
    parameters:
      - name: recipe_id
        in: path
        type: string
        required: true
        description: Recipe UUID
      - name: step_id
        in: path
        type: string
        required: true
        description: RecipeStep UUID
      - name: body
        in: body
        schema:
          type: object
          properties:
            description:
              type: string
            step_number:
              type: integer
            title:
              type: string
            image_url:
              type: string
            duration_minutes:
              type: integer
            tip:
              type: string
    responses:
      200:
        description: Recipe step updated successfully
      400:
        description: Invalid input
      404:
        description: Recipe or step not found
    """
    data = request.get_json()
    if not data:
        return error_response('Request body is empty', 400)

    try:
        item = RecipeService.update_recipe_step(recipe_id, step_id, **data)
    except ValueError as exc:
        return error_response(str(exc), 404)

    return success_response(data=item, message='Recipe step updated successfully')


@recipe_bp.route('/<recipe_id>/steps/<step_id>', methods=['DELETE'])
@handle_api_error
def delete_recipe_step(recipe_id, step_id):
    """
    Delete one row from recipe_steps
    ---
    tags:
      - Recipes
    parameters:
      - name: recipe_id
        in: path
        type: string
        required: true
        description: Recipe UUID
      - name: step_id
        in: path
        type: string
        required: true
        description: RecipeStep UUID
    responses:
      200:
        description: Recipe step deleted successfully
      404:
        description: Recipe or step not found
    """
    try:
        result = RecipeService.delete_recipe_step(recipe_id, step_id)
    except ValueError as exc:
        return error_response(str(exc), 404)

    return success_response(data=result, message='Recipe step deleted successfully')
