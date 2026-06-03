"""Recipe Suggestion API Routes"""
from flask import Blueprint, request, jsonify
from app.services.recipe_suggestion_service import RecipeSuggestionService
import logging

logger = logging.getLogger(__name__)

# Create blueprint
recipe_suggestion_bp = Blueprint('recipe_suggestion', __name__, url_prefix='/api/recipe')


@recipe_suggestion_bp.route('/suggest', methods=['POST'])
def suggest_recipe():
    """
    Gợi ý công thức món ăn dựa trên ingredients
    ---
    tags:
      - Recipe Suggestion
    summary: Suggest recipe based on user ingredients
    description: |
      Truy vấn dữ liệu công thức trong DB và xếp hạng theo mức độ khớp nguyên liệu.
      
      Flow:
      1. Nhận danh sách ingredients từ user
      2. Query recipes từ database
      3. Tính điểm tương đồng nguyên liệu trực tiếp tại backend
      4. Trả về best recipe + alternatives
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - ingredients
          properties:
            ingredients:
              type: array
              items:
                type: string
              example: ["trứng", "cà chua", "hành lá", "tỏi"]
              description: Danh sách tên nguyên liệu người dùng có
            preferences:
              type: object
              description: Optional preferences để filter recipes
              properties:
                difficulty:
                  type: string
                  enum: ["De", "Trung binh", "Kho"]
                  example: "De"
                cook_time_max:
                  type: integer
                  example: 30
                  description: Thời gian nấu tối đa (phút)
                cuisine_type:
                  type: string
                  example: "Viet Nam"
                diet_tags:
                  type: array
                  items:
                    type: string
                  example: ["chay"]
            limit_recipes:
              type: integer
              example: 50
              description: Giới hạn số recipes query từ DB (default 50)
    responses:
      200:
        description: Successfully generated recipe suggestion
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                best_recipe:
                  type: object
                  properties:
                    id:
                      type: string
                      example: "abc-123-xyz"
                    name:
                      type: string
                      example: "Trứng chiên cà chua"
                    match_score:
                      type: number
                      example: 0.95
                    image_url:
                      type: string
                    servings:
                      type: integer
                reason:
                  type: string
                  example: "Bạn có đủ 8/10 nguyên liệu cần thiết..."
                missing_ingredients:
                  type: array
                  items:
                    type: string
                  example: ["muối", "tiêu"]
                substitutions:
                  type: array
                  items:
                    type: object
                    properties:
                      original:
                        type: string
                      replacement:
                        type: string
                      reason:
                        type: string
                instructions:
                  type: string
                  example: "1. Đánh trứng...\n2. Xào cà chua..."
                alternative_recipes:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                      name:
                        type: string
                      match_score:
                        type: number
      400:
        description: Invalid request (missing ingredients)
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Danh sách nguyên liệu không được rỗng"
      500:
        description: Internal server error
    """
    try:
        # Parse request body
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400
        
        # Validate required fields
        ingredients = data.get('ingredients')
        if not ingredients:
            return jsonify({
                "success": False,
                "error": "Field 'ingredients' is required"
            }), 400
        
        if not isinstance(ingredients, list) or len(ingredients) == 0:
            return jsonify({
                "success": False,
                "error": "Field 'ingredients' must be a non-empty array"
            }), 400
        
        # Optional fields
        preferences = data.get('preferences')
        limit_recipes = data.get('limit_recipes')
        
        logger.info(f"Recipe suggestion request: {len(ingredients)} ingredients")
        
        # Call service
        service = RecipeSuggestionService()
        result = service.generate_recipe_suggestion(
            user_ingredients=ingredients,
            preferences=preferences,
            limit_recipes=limit_recipes
        )
        
        return jsonify({
            "success": True,
            "data": result
        }), 200
        
    except ValueError as e:
        # Validation errors
        logger.warning(f"Validation error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
        
    except Exception as e:
        # Unexpected errors
        logger.error(f"Unexpected error in suggest_recipe: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "detail": str(e)
        }), 500


@recipe_suggestion_bp.route('/detail/<recipe_id>', methods=['GET'])
def get_recipe_detail(recipe_id):
    """
    Lấy chi tiết một recipe
    ---
    tags:
      - Recipe Suggestion
    summary: Get recipe detail by ID
    parameters:
      - name: recipe_id
        in: path
        required: true
        type: string
        description: Recipe ID
    responses:
      200:
        description: Recipe detail
        schema:
          type: object
          properties:
            success:
              type: boolean
            data:
              type: object
              properties:
                id:
                  type: string
                name:
                  type: string
                description:
                  type: string
                steps:
                  type: string
                ingredients:
                  type: array
                  items:
                    type: object
      404:
        description: Recipe not found
    """
    try:
        service = RecipeSuggestionService()
        recipe = service.get_recipe_detail(recipe_id)
        
        if not recipe:
            return jsonify({
                "success": False,
                "error": "Recipe not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": recipe
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting recipe detail: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@recipe_suggestion_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint cho recipe suggestion service
    ---
    tags:
      - Recipe Suggestion
    summary: Health check for DB-based recipe suggestion
    responses:
      200:
        description: Health check result
        schema:
          type: object
          properties:
            success:
              type: boolean
            service_status:
              type: object
              properties:
                status:
                  type: string
                  example: "healthy"
                message:
                  type: string
    """
    try:
        return jsonify({
            "success": True,
            "service_status": {
                "status": "healthy",
                "message": "Recipe suggestion is using DB matching (no LLM call)"
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
