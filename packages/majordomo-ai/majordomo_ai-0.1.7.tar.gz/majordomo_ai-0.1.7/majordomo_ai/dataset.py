from enum import Enum, IntEnum
from pydantic import BaseModel

import requests
import json
import os

from .utils import create_user_response

class IndexTypeEnum(str, Enum):
    vector_db = "vector_db" 
    simple_list = "simple_list" 

class Dataset(BaseModel):
    name : str
    provider : str
    index_type : IndexTypeEnum
    embedding_model : str  | None = ''

    def retrieve_nodes(self, user_token, query_str, top_k):
        client_url = os.environ['MAJORDOMO_AI_CLIENT_URL']

        request_body = DatasetRetrieve(
                user_token=user_token,
                query_str=query_str,
                top_k=top_k,
                dataset=self
                )

        try:
            headers = {"Content-Type": "application/json"}
            result = requests.post(client_url + '/vectordb_retrieve', data=json.dumps(request_body.model_dump(mode='json')), headers=headers)
            print(result.content)
            response_json = create_user_response(result)
        except Exception as e: raise

        return response_json

    def summarize_document(self, user_token, summary_dataset, genai_model, summary_instruction):

        client_url = os.environ['MAJORDOMO_AI_CLIENT_URL']

        request_body = SummarizeDocument(
                user_token=user_token,
                dataset=self,
                summary_dataset=summary_dataset,
                genai_model=genai_model,
                summary_instruction=summary_instruction,
                )

        try:
            headers = {"Content-Type": "application/json"}
            result = requests.post(client_url + '/summarize_document', data=json.dumps(request_body.model_dump(mode='json')), headers=headers)
            response_json = create_user_response(result)
        except Exception as e: raise

        return response_json

    def delete(self, user_token):

        client_url = os.environ['MAJORDOMO_AI_CLIENT_URL']

        request_body = DatasetDelete(
                user_token=user_token,
                dataset=self
                )

        try:
            headers = {"Content-Type": "application/json"}
            result = requests.post(client_url + '/dataset_delete', data=json.dumps(request_body.model_dump(mode='json')), headers=headers)
            response_json = create_user_response(result)
        except Exception as e: raise

        return response_json

class DatasetDelete(BaseModel):

    user_token : str
    dataset : Dataset

class DatasetRetrieve(BaseModel):

    user_token : str

    dataset : Dataset
    query_str : str
    top_k : int | None = 2
    
class SummarizeDocument(BaseModel):
    user_token : str

    dataset : Dataset
    genai_model: str
    summary_dataset : Dataset
    summary_instruction : str
