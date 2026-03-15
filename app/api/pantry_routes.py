"""Pantry API routes"""
from flask import Blueprint, request
from app.services.pantry_service import PantryService
from app.utils.response import success_response, error_response, handle_api_error


pantry_bp = Blueprint('pantry', __name__, url_prefix='/api/pantry')


def _get_user_id():
    """Resolve user identifier from request"""
    return request.headers.get('X-User-Id') or request.args.get('user_id') or 'anonymous'


@pantry_bp.route('', methods=['GET'])
@handle_api_error
def get_pantry():
    """
    Get pantry items for user
    ---
    tags:
      - Pantry
    parameters:
      - name: X-User-Id
        in: header
        type: string
        required: false
        description: User identifier
    responses:
      200:
        description: Pantry list
    """
    items = PantryService.get_pantry(_get_user_id())
    return success_response(data=items, message='Pantry retrieved successfully')


@pantry_bp.route('', methods=['POST'])
@handle_api_error
def add_pantry_item():
    """
    Add ingredient to pantry
    ---
    tags:
      - Pantry
    parameters:
      - name: X-User-Id
        in: header
        type: string
        required: false
        description: User identifier
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - ingredient_id
            - quantity
          properties:
            ingredient_id:
              type: string
              example: "550e8400-e29b-41d4-a716-446655440000"
            quantity:
              type: string
              example: "500g"
    responses:
      201:
        description: Pantry item added successfully
      400:
        description: Invalid input
      404:
        description: Ingredient not found
    """
    data = request.get_json()
    if not data:
        return error_response('Request body is empty', 400)

    if 'ingredient_id' not in data:
        return error_response('Missing required field: ingredient_id', 400)

    if 'quantity' not in data:
        return error_response('Missing required field: quantity', 400)

    try:
        item = PantryService.add_item(
            user_id=_get_user_id(),
            ingredient_id=data['ingredient_id'],
            quantity=data['quantity']
        )
    except ValueError as exc:
        return error_response(str(exc), 404)

    return success_response(
        data=item,
        message='Pantry item saved successfully',
        status_code=201
    )


@pantry_bp.route('/<pantry_item_id>', methods=['DELETE'])
@handle_api_error
def delete_pantry_item(pantry_item_id):
    """
    Delete pantry item by ID
    ---
    tags:
      - Pantry
    parameters:
      - name: pantry_item_id
        in: path
        type: string
        required: true
        description: Pantry item UUID
      - name: X-User-Id
        in: header
        type: string
        required: false
        description: User identifier
    responses:
      200:
        description: Pantry item deleted successfully
      404:
        description: Pantry item not found
    """
    try:
        result = PantryService.delete_item(_get_user_id(), pantry_item_id)
    except ValueError as exc:
        return error_response(str(exc), 404)

    return success_response(data=result, message='Pantry item deleted successfully')
