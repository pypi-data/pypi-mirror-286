from enum import Enum, IntEnum
from pydantic import BaseModel
from typing import Optional
from .datasource import DataSource

class SQLDatabase(BaseModel):
    url : str
    name: str

class DBTypeEnum(str, Enum):
    sql = 'SQL'

class StructuredDB(BaseModel):
    db_type: DBTypeEnum
    info: SQLDatabase

class MetaQueryResponse(BaseModel):
    response: str
    metadata: str

class QueryResponse(BaseModel):
    response: str

class ImageQueryResponse(BaseModel):
    response: list

class VectorDBAccessRequest(BaseModel):
    user_token: str
    dataset: str
    operation: str

class VectorDBAccessResponse(BaseModel):
    vectordb_provider: str
    vectordb_access_key: str
    vectordb_endpoint: dict
    monitoring_public_key: str
    monitoring_secret_key: str
    monitoring_host: str

class AccessInfoRequest(BaseModel):

    user_token: str
    llm_model: str
    embedding_model: str
    dataset: str
    operation: str

class AccessInfoResponse(BaseModel):

    user: str
    cost_tags: str
    embedding_model_provider: str
    embedding_model_access_key: str
    llm_model_provider: str
    llm_model_access_key: str
    vectordb_provider: str
    vectordb_access_key: str
    vectordb_endpoint: dict
    monitoring_public_key: str
    monitoring_secret_key: str
    monitoring_host: str
