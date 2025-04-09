# app/extensions.py
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_pymongo import PyMongo
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mongo = PyMongo()

def init_mongo(app):
    try:
        # More robust connection configuration
        mongo.init_app(
            app, 
            uri=app.config.get('MONGO_URI', 'mongodb://127.0.0.1:27017/salto'),
            connect=True,  # Force immediate connection
            serverSelectionTimeoutMS=5000
        )
        logger.info("MongoDB initialized successfully")
    except Exception as e:
        logger.error(f"MongoDB Initialization Error: {e}")
        raise
    
login_manager = LoginManager()
