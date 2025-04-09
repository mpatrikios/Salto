from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

""" 
Buisness Data stores buisness-related data( e.g. Company ID, dataset anem, company name, data dict, etc.)
Dataset Schema/Demo Data are not necessary once we are using Azure OpenAI API. These are simply used to
generate demo data for the user to see how the application works. However, if we want to offer tiered pricing in the future
for models trained on company data/past company conversations, we can use a version of these. 
"""

class BusinessData(BaseModel):
    id: Optional[str] = None
    dataset_name: str
    description: str
    instance_name: str = "Default Instance"
    data: Dict[str, Any] = {}
    created_at: int = Field(default_factory=lambda: int(datetime.now().timestamp() * 1000))
    
    class Config:
        arbitrary_types_allowed = True
        
    @staticmethod
    def from_mongo(data: Dict[str, Any]) -> 'BusinessData':
        """
        Args: 
            data (Dict[str, Any]): MongoDB document data
        Returns:
            BusinessData: Converted BusinessData model
        
        Description:
            This method converts a MongoDB document to a BusinessData model.
            It extracts core fields and all remaining fields as data.
        """
        if not data:
            return None
        
        # Extract core fields
        result = BusinessData(
            id=str(data['_id']),
            dataset_name=data.get('dataset_name', 'Unknown Dataset'),
            description=data.get('description', ''),
            instance_name=data.get('instance_name', 'Default Instance'),
            created_at=data.get('created_at', int(datetime.now().timestamp() * 1000))
        )
        
        # Extract all remaining fields as data
        for key, value in data.items():
            if key not in ['_id', 'dataset_name', 'description', 'instance_name', 'created_at']:
                result.data[key] = value
                
        return result
    
    def to_mongo(self) -> Dict[str, Any]:
        """
        Args:
            None
        Returns:
            Dict[str, Any]: MongoDB document data
        
        Description:
            This method converts the BusinessData model to a dictionary format suitable for MongoDB.
            It excludes the 'id' field and converts it to ObjectId if it exists.
        """
        # Start with the basic fields
        data = {
            'dataset_name': self.dataset_name,
            'description': self.description,
            'instance_name': self.instance_name,
            'created_at': self.created_at
        }
        
        # Add the actual business data
        data.update(self.data)
        
        # Convert id to ObjectId if it exists
        if self.id:
            data['_id'] = ObjectId(self.id)
            
        return data


class DatasetSchema(BaseModel):
    """Model representing a dataset schema for AI-generated data"""
    dataset_name: str
    description: str
    data: Dict[str, Any]


class DemoDataRequest(BaseModel):
    """Model representing a request for demo data generation"""
    datasets: List[DatasetSchema]