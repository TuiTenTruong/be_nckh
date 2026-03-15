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
    Scan ingredients from uploaded image
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
        description: Image to scan
      - name: X-User-Id
        in: header
        type: string
        required: false
        description: User identifier
    responses:
      201:
        description: Scan completed successfully
      400:
        description: Missing image file
    """
    image_file = request.files.get('image')
    if not image_file:
        return error_response('Missing image file', 400)

    image_bytes = image_file.read()
    if not image_bytes:
        return error_response('Image file is empty', 400)

    session = ScanService.create_scan(
        image_bytes=image_bytes,
        filename=image_file.filename or 'upload.jpg',
        user_id=_get_user_id()
    )

    return success_response(
        data=session,
        message='Scan completed successfully',
        status_code=201
    )


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
        description: Scan session details
      404:
        description: Scan session not found
    """
    session = ScanService.get_scan_by_id(scan_id)
    if not session:
        return error_response('Scan session not found', 404)

    return success_response(data=session, message='Scan session retrieved successfully')
