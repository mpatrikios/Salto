from typing import List, Dict, Any, Optional
from bson import ObjectId
import json
from app.extensions import mongo
from app.models.data import BusinessData
from app.services.ai_service import AzureOpenAIService
from app.models.chat import ChatSession
from flask import current_app

def get_user_by_id(user_id):
    try:
        return mongo.db.users.find_one({'_id': ObjectId(user_id)})
    except Exception:
        return None

class DataService:
    """Service for managing business data"""
    
    def get_data_documents(self, instance_name: str) -> List[BusinessData]:
        """Get all business data documents for a specific instance"""
        data_docs = mongo.db.business_data.find({
            'instance_name': instance_name
        })
        
        return [BusinessData.from_mongo(doc) for doc in data_docs]
    
    def get_data_context(self, instance_name: str) -> str:
        """Get a text representation of available data for context"""
        data_docs = self.get_data_documents(instance_name)
        
        if not data_docs:
            return "No business data available yet. Add sample data or explain what data you're looking for."
        
        # Create a summary of available data
        data_summaries = []
        for doc in data_docs:
            # Create a summary of the data fields
            data_summary = {
                "dataset": doc.dataset_name,
                "description": doc.description,
                "fields": list(doc.data.keys()),
                "sample": {k: v for k, v in doc.data.items() if not isinstance(v, dict) and not isinstance(v, list)}
            }
            data_summaries.append(json.dumps(data_summary, default=str))
        
        return "\n\n".join(data_summaries)
    
    def add_data_document(self, data: BusinessData) -> str:
        """Add a new business data document"""
        result = mongo.db.business_data.insert_one(data.to_mongo())
        return str(result.inserted_id)
    
    def delete_all_instance_data(self, instance_name: str) -> int:
        """Delete all data for a specific instance"""
        # Delete business data
        data_result = mongo.db.business_data.delete_many({'instance_name': instance_name})
        
        # Delete chat sessions
        chat_result = mongo.db.chat_sessions.delete_many({'instance_name': instance_name})
        
        # Delete messages
        msg_result = mongo.db.messages.delete_many({'instance_name': instance_name})
        
        return data_result.deleted_count + chat_result.deleted_count + msg_result.deleted_count
    
    def generate_demo_data(self, instance_name: str, chat_id: Optional[str] = None) -> List[str]:
        """Generate and save demo data"""
        from app.services.chat_service import ChatService
        
        ai_service = AzureOpenAIService()
        chat_service = ChatService()
        
        # Generate demo data
        demo_data = ai_service.generate_demo_data()
        
        # Save each dataset
        dataset_ids = []
        for dataset in demo_data.datasets:
            business_data = BusinessData(
                dataset_name=dataset.dataset_name,
                description=dataset.description,
                instance_name=instance_name,
                data=dataset.data
            )
            
            dataset_id = self.add_data_document(business_data)
            dataset_ids.append(dataset_id)
        
        # Create a chat conversation about the demo data if chat_id is provided
        if chat_id:
            # Get chat session or create one if it doesn't exist
            chat_session = mongo.db.chat_sessions.find_one({'_id': ObjectId(chat_id)})
            if not chat_session:
                new_chat = ChatSession(instance_name=instance_name, title="Demo Data Exploration")
                result = mongo.db.chat_sessions.insert_one(new_chat.to_mongo())
                chat_id = str(result.inserted_id)
            
            # Add initial conversation
            chat_service.add_message(
                chat_id, 
                'user', 
                "Salto, what business data is available for me to explore?", 
                instance_name
            )
            
            # Create data description
            data_description = "\n".join([
                f"- **{dataset.dataset_name}**: {dataset.description}" 
                for dataset in demo_data.datasets
            ])
            
            response = f"""
I've loaded some sample business data for the "{instance_name}" instance:

{data_description}

You can ask me questions about this data, such as "Salto, what were our top-selling products?" or "Salto, how have sales trended over time?"

I'm here to help you explore this data and uncover valuable insights for your business.
            """
            
            chat_service.add_message(chat_id, 'assistant', response.strip(), instance_name)
            
            # Update chat title
            chat_service.update_chat_title(chat_id, "Demo Data Exploration")
        
        return dataset_ids
