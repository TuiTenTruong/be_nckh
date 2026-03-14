"""Flask application factory"""
from flask import Flask
from app.extensions import db, cors
from app.config import config
from app.api.ingredient_routes import ingredient_bp, category_bp
from app.errors.handlers import register_error_handlers


def create_app(config_name='development'):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(ingredient_bp)
    app.register_blueprint(category_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
