"""Application configuration"""
import os

class Config:
    """Base configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    
    # AI Service Base URL for recipe suggestion and chat
    AI_SERVICE_BASE_URL = os.getenv(
        'AI_SERVICE_BASE_URL',
        'http://127.0.0.1:8000'
    )

    # AI Service (food-ai-service) Endpoint for vision analysis
    AI_SERVICE_ENDPOINT = os.getenv(
        'AI_SERVICE_ENDPOINT',
        f"{os.getenv('AI_SERVICE_BASE_URL', 'http://127.0.0.1:8000').rstrip('/')}/api/ai/analyze-image"
    )
    
    # AI Service Timeout (seconds)
    AI_SERVICE_TIMEOUT = int(os.getenv('AI_SERVICE_TIMEOUT', 30))

    # Public URL for resolving relative image paths in API responses
    API_PUBLIC_URL = os.getenv('API_PUBLIC_URL', 'http://127.0.0.1:5000')
    
    # Legacy config (kept for backward compatibility)
    VISION_API_PROVIDER = os.getenv('VISION_API_PROVIDER', 'food_ai_service')
    SERVICE_DEMO_ENDPOINT = os.getenv('SERVICE_DEMO_ENDPOINT')
    SERVICE_DEMO_API_KEY = os.getenv('SERVICE_DEMO_API_KEY')
    VISION_API_ENDPOINT = os.getenv('VISION_API_ENDPOINT', 'http://127.0.0.1:8000/api/ai/analyze-image')
    VISION_API_KEY = os.getenv('VISION_API_KEY')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:161104@localhost:3306/nckh'
    )
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
