from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

"""A chat session represents a conversation between a user and the AI model.
Each message is an exchange in that conversation, including data about the role, content, and timestap. 
The instance_name, is the name of the tenant/company to help distinguish between
data from different companies using the same pplication. Each tenant has its own data and chat sessions."""

class ChatSession(BaseModel):

    id: Optional[str] = None
    title: str = "New Salto Chat"
    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    last_message_at: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    instance_name: str = "Default Instance"
    
    class Config:
        arbitrary_types_allowed = True
        
    @staticmethod
    def from_mongo(data: Dict[str, Any]) -> 'ChatSession':
        """
        Args:
            data (Dict[str, Any]): MongoDB document data
        Returns:
            ChatSession: Converted ChatSession model
            
        Description:
            This method converts a MongoDB document to a ChatSession model.
        """
        if not data:
            return None
            
            return ChatSession(
                id=str(data['_id']),
                title=data.get('title', 'New Salto Chat'),
                created_at=data.get('created_at'),
                last_message_at=data.get('last_message_at'),
                instance_name=data.get('instance_name', 'Default Instance')
            )
    
    def to_mongo(self) -> Dict[str, Any]:
        """
        Args:
            None
        Returns:
            Dict[str, Any]: MongoDB document data
            
        Description:
            This method converts the ChatSession model to a dictionary format suitable for MongoDB.
            It excludes the 'id' field and converts it to ObjectId if it exists.
        """
        data = self.dict(exclude={'id'})
        
        # Convert id to ObjectId if it exists
        if self.id:
            data['_id'] = ObjectId(self.id)
            
        return data


class Message(BaseModel):
    """Model representing a message in a chat"""
    id: Optional[str] = None
    chat_id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    instance_name: str = "Default Instance"
    
    class Config:
        arbitrary_types_allowed = True
        
    @staticmethod
    def from_mongo(data: Dict[str, Any]) -> 'Message':
        """
        Args:
            data (Dict[str, Any]): MongoDB document data
        Returns:
            Message: Converted Message model
            
        Description:
            This method converts a MongoDB document to a Message model.
        """
        if not data:
            return None
        
        return Message(
            id=str(data['_id']),
            chat_id=data.get('chat_id'),
            role=data.get('role'),
            content=data.get('content'),
            timestamp=data.get('timestamp'),
            instance_name=data.get('instance_name', 'Default Instance')
        )
    
    def to_mongo(self) -> Dict[str, Any]:
        """
        Args:
            None
        Returns:
            Dict[str, Any]: MongoDB document data
            
        Description:
            This method converts the Message model to a dictionary format suitable for MongoDB.
            It excludes the 'id' field and converts it to ObjectId if it exists.
        """
        data = self.dict(exclude={'id'})
        
        # Convert id to ObjectId if it exists
        if self.id:
            data['_id'] = ObjectId(self.id)
            
        return data