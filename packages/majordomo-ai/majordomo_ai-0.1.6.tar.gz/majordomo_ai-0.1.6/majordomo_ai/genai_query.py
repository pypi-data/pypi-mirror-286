import os
import json
import requests
from pydantic import BaseModel, ValidationError

from .datasource import DataSource
from .models import *
from .dataset import *
from .utils import create_user_response
from pathlib import Path

class QueryModeEnum(str, Enum):
    refine = "refine" 
    compact = "compact" 
    accumulate = "accumulate" 

class GenAIIndexQuery(BaseModel):

    user_token : str

    dataset : Dataset
    top_k : int | None = 2

    embedding_model : str
    genai_model : str
    temperature : float | None = 1.0
    query_mode : str | None = 'compact'

    query_str : str

    def run(self):
        
        client_url = os.environ['MAJORDOMO_AI_CLIENT_URL']

        try:
            headers = {"Content-Type": "application/json"}
            result = requests.post(client_url + '/genai_index_query', data=json.dumps(self.model_dump(mode='json')), headers=headers)
            print(result.content)
            response_json = create_user_response(result)
        except Exception as e: raise

        return response_json

class ImageQuery(BaseModel):

    user_token : str

    embedding_model : str

    dataset : Dataset

    query_str : str

    def run(self):

        client_url = os.environ['MAJORDOMO_AI_CLIENT_URL']
        
        try:
            headers = {"Content-Type": "application/json"}
            result = requests.post(client_url + '/image_query', data=json.dumps(self.model_dump(mode='json')), headers=headers)
            response_json = create_user_response(result)
        except Exception as e: raise

        return response_json
