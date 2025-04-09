from flask import Blueprint, request, jsonify, session, current_app
from app.services.data_service import DataService
from app.models.data import BusinessData
from bson.objectid import ObjectId
from bson.errors import InvalidId

data_bp = Blueprint('data', __name__, url_prefix='/data')
data_service = DataService()

@data_bp.route('/list', methods=['GET'])
def list_data():
    """
    Description:
        Returns a list of all data documents for the current instance
    """
    instance_name = session.get('instance_name', 'Default Instance')
    data_docs = data_service.get_data_documents(instance_name)
    
    return jsonify([{
        'id': doc.id,
        'dataset_name': doc.dataset_name,
        'description': doc.description,
        'created_at': doc.created_at
    } for doc in data_docs])

@data_bp.route('/<doc_id>', methods=['GET'])
def get_data(doc_id):
    """
    Description:
        Gets a specific data document by its ID
    """
    try:
        # Validate ObjectId
        ObjectId(doc_id)
    except InvalidId:
        return jsonify({'error': 'Invalid document ID format'}), 400
    
    doc = next((d for d in data_service.get_data_documents(session.get('instance_name', 'Default Instance')) 
                if d.id == doc_id), None)
    
    if not doc:
        return jsonify({'error': 'Document not found'}), 404
    
    return jsonify({
        'id': doc.id,
        'dataset_name': doc.dataset_name,
        'description': doc.description,
        'data': doc.data,
        'created_at': doc.created_at
    })

@data_bp.route('/generate-demo', methods=['POST'])
def generate_demo():
    """
    Description:
        Generates demo data for the current instance
    """
    instance_name = session.get('instance_name', 'Default Instance')
    
    # Check if API key is configured
    if not current_app.config['AZURE_OPENAI_API_KEY']:
        return jsonify({'error': 'Azure OpenAI API key is not configured. Please update settings.'}), 400
    
    # Get chat_id from request (optional)
    data = request.json or {}
    chat_id = data.get('chat_id')
    
    try:
        # Generate demo data
        dataset_ids = data_service.generate_demo_data(instance_name, chat_id)
        
        return jsonify({
            'success': True,
            'dataset_count': len(dataset_ids),
            'dataset_ids': dataset_ids,
            'message': f'Successfully generated {len(dataset_ids)} demo datasets'
        })
    except Exception as e:
        current_app.logger.error(f"Error generating demo data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@data_bp.route('/add', methods=['POST'])
def add_data():
    """
    Description:
        Adds a new data document to the database by creating a BuisnessData model
        and saving it to the database.
    """
    instance_name = session.get('instance_name', 'Default Instance')
    data = request.json
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    # Validate required fields
    if 'dataset_name' not in data or 'description' not in data:
        return jsonify({'error': 'dataset_name and description are required'}), 400
    
    try:
        # Create business data model
        business_data = BusinessData(
            dataset_name=data['dataset_name'],
            description=data['description'],
            instance_name=instance_name
        )
        
        # Add any additional data fields
        for key, value in data.items():
            if key not in ['dataset_name', 'description', 'instance_name']:
                business_data.data[key] = value
        
        # Save to database
        doc_id = data_service.add_data_document(business_data)
        
        return jsonify({
            'success': True,
            'id': doc_id,
            'message': f'Successfully added dataset "{data["dataset_name"]}"'
        })
    except Exception as e:
        current_app.logger.error(f"Error adding data document: {str(e)}")
        return jsonify({'error': str(e)}), 500