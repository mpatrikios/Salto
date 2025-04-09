from flask import Blueprint, request, jsonify, render_template, current_app, session
from app.services.chat_service import ChatService
from bson.objectid import ObjectId
from bson.errors import InvalidId

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')
chat_service = ChatService()

@chat_bp.route('/', methods=['GET'])
def index():
    
    """
    Description:
        Renders the main chat page with all chat sessions
    """
    instance_name = session.get('instance_name', 'Default Instance')
    chats = chat_service.get_chat_sessions(instance_name)
    return render_template('index.html', chats=chats, active_chat=None, instance_name=instance_name)

@chat_bp.route('/<chat_id>', methods=['GET'])
def view_chat(chat_id):
    """
    Description:
        Renders the chat page for a specific chat session using chat_id
    """
    instance_name = session.get('instance_name', 'Default Instance')
    
    try:
        # Validate ObjectId
        ObjectId(chat_id)
    except InvalidId:
        return jsonify({'error': 'Invalid chat ID format'}), 400
    
    # Get chat and messages
    chat = chat_service.get_chat_by_id(chat_id)
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404
    
    chats = chat_service.get_chat_sessions(instance_name)
    messages = chat_service.get_messages(chat_id)
    
    return render_template('index.html', 
                          chats=chats, 
                          active_chat=chat, 
                          messages=messages, 
                          instance_name=instance_name)

@chat_bp.route('/create', methods=['POST'])
def create_chat():
    """
        Description:
            Creates a new chat session and returns its details
    """
    instance_name = session.get('instance_name', 'Default Instance')
    
    chat = chat_service.create_chat(instance_name)
    return jsonify({
        'id': chat.id,
        'title': chat.title,
        'created_at': chat.created_at,
        'instance_name': chat.instance_name
    })

@chat_bp.route('/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    """
        Description:
            Deletes chat session by chat_id
    """
    try:
        # Validate ObjectId
        ObjectId(chat_id)
    except InvalidId:
        return jsonify({'error': 'Invalid chat ID format'}), 400
    
    success = chat_service.delete_chat(chat_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to delete chat'}), 500

@chat_bp.route('/<chat_id>/messages', methods=['GET'])
def get_messages(chat_id):
    """
        Description:
            Retrieves all messages for a specific chat session using chat_id
    """
    try:
        # Validate ObjectId
        ObjectId(chat_id)
    except InvalidId:
        return jsonify({'error': 'Invalid chat ID format'}), 400
    
    messages = chat_service.get_messages(chat_id)
    return jsonify([{
        'id': msg.id,
        'role': msg.role,
        'content': msg.content,
        'timestamp': msg.timestamp
    } for msg in messages])

@chat_bp.route('/<chat_id>/send', methods=['POST'])
def send_message(chat_id):
    """
    Description:
        Sends a message in chat session and returns the response
    """
    instance_name = session.get('instance_name', 'Default Instance')
    data = request.json
    
    if not data or 'message' not in data:
        return jsonify({'error': 'Message content is required'}), 400
    
    query = data['message']
    
    try:
        # Validate ObjectId
        ObjectId(chat_id)
    except InvalidId:
        return jsonify({'error': 'Invalid chat ID format'}), 400
    
    # Check if API key is configured
    if not current_app.config['AZURE_OPENAI_API_KEY']:
        return jsonify({'error': 'Azure OpenAI API key is not configured. Please update settings.'}), 400
    
    # Process the query
    response_message = chat_service.process_query(chat_id, query, instance_name)
    
    return jsonify({
        'id': response_message.id,
        'role': response_message.role,
        'content': response_message.content,
        'timestamp': response_message.timestamp
    })