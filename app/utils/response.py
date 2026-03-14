"""Utility functions for API responses"""
from flask import jsonify
from functools import wraps


def success_response(data=None, message="Success", status_code=200):
    """
    Create a standardized success response
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
    
    Returns:
        Flask response
    """
    response = {
        'success': True,
        'message': message,
        'data': data
    }
    return jsonify(response), status_code


def error_response(message="Error", status_code=400, errors=None):
    """
    Create a standardized error response
    
    Args:
        message: Error message
        status_code: HTTP status code
        errors: Additional error details
    
    Returns:
        Flask response
    """
    response = {
        'success': False,
        'message': message,
        'errors': errors
    }
    return jsonify(response), status_code


def paginated_response(items, total, page, per_page, message="Success"):
    """
    Create a paginated response
    
    Args:
        items: List of items
        total: Total count
        page: Current page
        per_page: Items per page
        message: Success message
    
    Returns:
        Flask response
    """
    response = {
        'success': True,
        'message': message,
        'data': items,
        'pagination': {
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }
    }
    return jsonify(response), 200


def handle_api_error(f):
    """Decorator to handle API errors"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return error_response(str(e), 500)
    return decorated_function
