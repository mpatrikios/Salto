# app/__init__.py
from flask import Flask, redirect, url_for
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from app.extensions import mongo, login_manager
from app.models.user import User
from app.services.data_service import get_user_by_id

load_dotenv()

def load_user(user_id):
    user_data = get_user_by_id(user_id)
    if user_data:
        return User(user_data)
    return None

# This function is needed by Flask-Login to load the user
@login_manager.user_loader
def load_user(user_id):
    # Use the `get_user_by_id` function from your service layer
    user_data = get_user_by_id(user_id)
    if user_data:
        return User(user_data)  # Assuming `User` is your User class that wraps the Mongo data
    return None

def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app.config.from_object(f'app.config.{config_name.capitalize()}Config')

    mongo.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes.chat_routes import chat_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.data_routes import data_bp

    @app.route('/')
    def index():
        return redirect(url_for('chat.index'))

    app.register_blueprint(chat_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(data_bp)

    @app.template_filter('format_date')
    def format_date(value):
        if isinstance(value, int) or isinstance(value, float):
            value = datetime.fromtimestamp(value / 1000)
        return value.strftime('%Y-%m-%d %H:%M')

    @app.errorhandler(404)
    def page_not_found(e):
        return {'error': 'Page not found'}, 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return {'error': 'Internal server error'}, 500

    return app
