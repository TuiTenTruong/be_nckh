"""Flask application factory"""
import os

from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, cors, swagger
from app.config import config
from app.api.ingredient_routes import ingredient_bp, category_bp
from app.api.recipe_routes import recipe_bp
from app.api.scan_routes import scan_bp
from app.api.pantry_routes import pantry_bp
from app.api.chat_routes import chat_bp
from app.api.recipe_suggestion_routes import recipe_suggestion_bp
from app.errors.handlers import register_error_handlers


def create_app(config_name='development'):
    """Create and configure Flask application"""
    # Load environment variables from be/.env for local development.
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    load_dotenv(env_path)

    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    
    # Configure Swagger/Flasgger - only for spec generation, not UI
    swagger.config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: rule.rule.startswith("/api/"),
                "model_filter": lambda tag: True,
            }
        ],
        "swagger_ui": False,  # Disable built-in UI - we use custom CDN-based UI
        "specs_route": "/apispec.json",
        "description": "Swagger spec for Ingredient & Recipe API",
    }
    
    swagger.template = {
        "swagger": "2.0",
        "info": {
            "title": "Ingredient & Recipe API",
            "description": "API documentation for ingredient and recipe services - Auto-generated Swagger from Python docstrings",
            "version": "1.0.0",
            "contact": {
                "name": "API Support",
            }
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "tags": [
            {
                "name": "Ingredients",
                "description": "Ingredient management endpoints"
            },
            {
                "name": "Categories",
                "description": "Ingredient category management endpoints"
            },
            {
                "name": "Recipes",
                "description": "Recipe management endpoints"
            },
            {
                "name": "Scan",
                "description": "Ingredient scan endpoints"
            },
            {
                "name": "Pantry",
                "description": "User pantry endpoints"
            },
            {
                "name": "Chat",
                "description": "Mock chat endpoints for frontend integration"
            },
            {
                "name": "Recipe Suggestion",
                "description": "AI-powered recipe suggestion endpoints"
            }
        ]
    }
    
    # Initialize Flasgger for spec generation only
    swagger.init_app(app)
    
    # Register custom Swagger UI with CDN resources
    from app.swagger_ui import swagger_bp
    app.register_blueprint(swagger_bp)
    
    # Register blueprints
    app.register_blueprint(ingredient_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(scan_bp)
    app.register_blueprint(pantry_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(recipe_suggestion_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
