import json
import openai
from typing import List, Dict, Any, Optional
from app import mongo
from app.models.data import DemoDataRequest, DatasetSchema
from datetime import datetime
from flask import current_app


class AzureOpenAIService:
    def __init__(self):
        self.client = None
    
    def generate_response(self, messages):
        # Mock response for testing
        return "This is a mock response from the AI service for testing purposes."
    
    def generate_demo_data(self):
        # Mock demo data
        return DemoDataRequest(datasets=[
            DatasetSchema(
                dataset_name="Sales Data",
                description="Sample sales data for testing",
                data={"total_sales": 15000, "products": ["Product A", "Product B"]}
            ),
            DatasetSchema(
                dataset_name="Customer Data",
                description="Sample customer information",
                data={"total_customers": 250, "regions": ["North", "South"]}
            )
        ])