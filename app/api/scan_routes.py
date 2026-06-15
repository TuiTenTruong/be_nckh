"""Scan API routes"""
from flask import Blueprint, request
from app.services.scan_service import ScanService
from app.utils.response import success_response, error_response, handle_api_error


scan_bp = Blueprint('scan', __name__, url_prefix='/api/scan')


def _get_user_id():
    """Resolve user identifier from request"""
    return request.headers.get('X-User-Id') or request.args.get('user_id') or 'anonymous'


@scan_bp.route('', methods=['POST'])
@handle_api_error
def create_scan():
    """
    Scan ingredients from uploaded image and get recipe suggestions
    ---
    tags:
      - Scan
    consumes:
      - multipart/form-data
    parameters:
      - name: image
        in: formData
        type: file
        required: true
        description: Image to scan for ingredients
      - name: X-User-Id
        in: header
        type: string
        required: false
        description: User identifier
      - name: difficulty
        in: formData
        type: string
        required: false
        description: Preferred difficulty (De|Trung binh|Kho)
      - name: cook_time_max
        in: formData
        type: integer
        required: false
        description: Maximum cooking time in minutes
      - name: cuisine_type
        in: formData
        type: string
        required: false
        description: Preferred cuisine type
    responses:
      201:
        description: Scan completed with recipe suggestions
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
                ingredients:
                  type: array
                matched_ingredient_names:
                  type: array
                recipe_suggestion:
                  type: object
                  properties:
                    best_recipe:
                      type: object
                    reason:
                      type: string
                    missing_ingredients:
                      type: array
                    alternative_recipes:
                      type: array
      400:
        description: Missing or empty image file
    """
    image_file = request.files.get('image')
    if not image_file:
        return error_response('Missing image file', 400)

    image_bytes = image_file.read()
    if not image_bytes:
        return error_response('Image file is empty', 400)

    # Parse optional preferences từ form data
    preferences = _parse_preferences(request.form)

    session = ScanService.create_scan(
        image_bytes=image_bytes,
        filename=image_file.filename or 'upload.jpg',
        user_id=_get_user_id(),
        preferences=preferences
    )

    return success_response(
        data=session,
        message='Scan completed with recipe suggestions',
        status_code=201
    )


def _parse_preferences(form_data):
    """Parse user preferences from form data"""
    preferences = {}
    
    if form_data.get('difficulty'):
        preferences['difficulty'] = form_data['difficulty']
    
    if form_data.get('cook_time_max'):
        try:
            preferences['cook_time_max'] = int(form_data['cook_time_max'])
        except ValueError:
            pass
    
    if form_data.get('cuisine_type'):
        preferences['cuisine_type'] = form_data['cuisine_type']
    
    if form_data.get('diet_tags'):
        # Expect comma-separated tags: "chay,it dau mo"
        tags = form_data['diet_tags'].split(',')
        preferences['diet_tags'] = [t.strip() for t in tags if t.strip()]
    
    return preferences if preferences else None


@scan_bp.route('/<scan_id>', methods=['GET'])
@handle_api_error
def get_scan(scan_id):
    """
    Get one scan session by ID
    ---
    tags:
      - Scan
    parameters:
      - name: scan_id
        in: path
        type: string
        required: true
        description: Scan session UUID
    responses:
      200:
        description: Scan session details with recipe suggestions
      404:
        description: Scan session not found
    """
    session = ScanService.get_scan_by_id(scan_id)
    if not session:
        return error_response('Scan session not found', 404)

    return success_response(data=session, message='Scan session retrieved successfully')
