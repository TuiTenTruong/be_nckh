"""API error handlers"""
from flask import Flask, jsonify, request


def register_error_handlers(app):
    """Register error handlers for the Flask app"""
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        if request.path.startswith('/static/'):
            return error.get_response()

        return jsonify({
            'success': False,
            'message': 'Resource not found',
            'errors': str(error)
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 errors"""
        return jsonify({
            'success': False,
            'message': 'Method not allowed',
            'errors': str(error)
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'errors': str(error)
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors"""
        return jsonify({
            'success': False,
            'message': 'Bad request',
            'errors': str(error)
        }), 400
