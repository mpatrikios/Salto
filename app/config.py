import os
from datetime import timedelta

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # MongoDB settings
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/salto')
    
    # Azure OpenAI settings
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4')
    AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '2023-05-15')
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Admin settings
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin1234')  # Change in production!


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/salto_dev')


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/salto_test')


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # Ensure these are set in production
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    
    # Production security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True