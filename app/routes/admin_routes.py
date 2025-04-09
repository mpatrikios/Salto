from flask import Blueprint, request, jsonify, render_template, session, current_app, redirect, url_for
from functools import wraps

"""Admin routes for managing the application"""
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

"""Only allow access to admin routes if the user is logged in as an admin"""
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin', False):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password')
        
        # Check if the password matches the admin password
        if password == current_app.config['ADMIN_PASSWORD']:
            session['is_admin'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('admin/login.html', error='Invalid password')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout', methods=['GET'])
def logout():
    """Admin logout"""
    session.pop('is_admin', None)
    return redirect(url_for('chat.index'))

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def dashboard():
    """Admin dashboard"""
    return render_template('admin/dashboard.html')

@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    """Admin settings page"""
    from app.services.data_service import DataService
    
    if request.method == 'POST':
        instance_name = request.form.get('instance_name', 'Default Instance')
        api_key = request.form.get('api_key', '')
        api_endpoint = request.form.get('api_endpoint', '')
        deployment = request.form.get('deployment', 'gpt-4')
        
        # Update session
        session['instance_name'] = instance_name
        
        # In a real app, you would securely store these values
        # For now, just set them in the current application config
        current_app.config['AZURE_OPENAI_API_KEY'] = api_key
        current_app.config['AZURE_OPENAI_ENDPOINT'] = api_endpoint
        current_app.config['AZURE_OPENAI_DEPLOYMENT'] = deployment
        
        return redirect(url_for('admin.settings', success=True))
    
    return render_template('admin/settings.html', 
                          instance_name=session.get('instance_name', 'Default Instance'),
                          api_key=current_app.config.get('AZURE_OPENAI_API_KEY', ''),
                          api_endpoint=current_app.config.get('AZURE_OPENAI_ENDPOINT', ''),
                          deployment=current_app.config.get('AZURE_OPENAI_DEPLOYMENT', 'gpt-4'))

@admin_bp.route('/clear-data', methods=['POST'])
@admin_required
def clear_data():
    """Clear all data for the current instance"""
    from app.services.data_service import DataService
    
    instance_name = session.get('instance_name', 'Default Instance')
    data_service = DataService()
    
    count = data_service.delete_all_instance_data(instance_name)
    
    return jsonify({
        'success': True,
        'deleted_count': count,
        'message': f'Successfully deleted all data for instance "{instance_name}"'
    })