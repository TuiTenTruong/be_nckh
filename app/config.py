"""Application configuration"""
import os

class Config:
    """Base configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    VISION_API_PROVIDER = os.getenv('VISION_API_PROVIDER', 'service_demo')
    SERVICE_DEMO_ENDPOINT = os.getenv(
        'SERVICE_DEMO_ENDPOINT',
        'http://127.0.0.1:5055/mock/scan'
    )
    SERVICE_DEMO_API_KEY = os.getenv('SERVICE_DEMO_API_KEY')
    VISION_API_ENDPOINT = os.getenv('VISION_API_ENDPOINT')
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
