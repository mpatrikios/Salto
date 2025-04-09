from typing import List, Dict, Any, Optional
from bson import ObjectId
from app import mongo
from app.models.chat import ChatSession, Message
from app.services.ai_service import AzureOpenAIService
from flask import current_app
import json


class ChatService:
    """Service for managing chat sessions and messages"""
    
    def __init__(self):
        self.ai_service = AzureOpenAIService()
    
    def get_chat_sessions(self, instance_name: str) -> List[ChatSession]:
        """Get all chat sessions for a specific instance"""
        chat_docs = mongo.db.chat_sessions.find({
            'instance_name': instance_name
        }).sort('last_message_at', -1)
        
        return [ChatSession.from_mongo(doc) for doc in chat_docs]
    
    def get_chat_by_id(self, chat_id: str) -> Optional[ChatSession]:
        """Get a chat session by ID"""
        chat_doc = mongo.db.chat_sessions.find_one({'_id': ObjectId(chat_id)})
        return ChatSession.from_mongo(chat_doc) if chat_doc else None
    
    def create_chat(self, instance_name: str) -> ChatSession:
        """Create a new chat session"""
        chat = ChatSession(
            title="New Salto Chat",
            instance_name=instance_name
        )
        
        result = mongo.db.chat_sessions.insert_one(chat.to_mongo())
        chat.id = str(result.inserted_id)
        
        return chat
    
    def update_chat_title(self, chat_id: str, title: str) -> bool:
        """Update the title of a chat session"""
        result = mongo.db.chat_sessions.update_one(
            {'_id': ObjectId(chat_id)},
            {'$set': {'title': title}}
        )
        
        return result.modified_count > 0
    
    def update_chat_last_message(self, chat_id: str) -> bool:
        """Update the last message timestamp of a chat session"""
        from datetime import datetime
        
        result = mongo.db.chat_sessions.update_one(
            {'_id': ObjectId(chat_id)},
            {'$set': {'last_message_at': int(datetime.now().timestamp() * 1000)}}
        )
        
        return result.modified_count > 0
    
    def delete_chat(self, chat_id: str) -> bool:
        """Delete a chat session and all its messages"""
        # Delete the chat session
        chat_result = mongo.db.chat_sessions.delete_one({'_id': ObjectId(chat_id)})
        
        # Delete all messages in this chat
        msg_result = mongo.db.messages.delete_many({'chat_id': chat_id})
        
        return chat_result.deleted_count > 0
    
    def get_messages(self, chat_id: str) -> List[Message]:
        """Get all messages for a specific chat session"""
        message_docs = mongo.db.messages.find({
            'chat_id': chat_id
        }).sort('timestamp', 1)
        
        return [Message.from_mongo(doc) for doc in message_docs]
    
    def add_message(self, chat_id: str, role: str, content: str, instance_name: str) -> Message:
        """Add a new message to a chat session"""
        # Update chat title if this is the first user message
        chat = self.get_chat_by_id(chat_id)
        if role == 'user' and chat and chat.title == "New Salto Chat":
            new_title = content if len(content) <= 30 else content[:27] + "..."
            self.update_chat_title(chat_id, new_title)
        
        # Create and save the message
        message = Message(
            chat_id=chat_id,
            role=role,
            content=content,
            instance_name=instance_name
        )
        
        result = mongo.db.messages.insert_one(message.to_mongo())
        message.id = str(result.inserted_id)
        
        # Update the chat's last message timestamp
        self.update_chat_last_message(chat_id)
        
        return message
    
    def process_query(self, chat_id: str, query: str, instance_name: str) -> Message:
        """Process a user query and generate a response"""
        from app.services.data_service import DataService
        
        # Get data context
        data_service = DataService()
        data_context = data_service.get_data_context(instance_name)
        
        # Add user message
        self.add_message(chat_id, 'user', query, instance_name)
        
        # Get conversation history (limited to last 6 messages for context)
        messages = self.get_messages(chat_id)[-6:]
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages if msg.role in ['user', 'assistant']
        ]
        
        try:
            # Generate AI response
            response = self.ai_service.process_user_query(
                query, 
                conversation_history, 
                data_context, 
                instance_name
            )
            
            # Add assistant message
            return self.add_message(chat_id, 'assistant', response, instance_name)
        except Exception as e:
            current_app.logger.error(f"Error processing query: {str(e)}")
            # Add error message
            error_msg = "I'm sorry, I couldn't process your query. Please check the API key or try reformulating your question. - Salto"
            return self.add_message(chat_id, 'assistant', error_msg, instance_name)