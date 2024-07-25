from pydantic import BaseModel, ValidationError
from sqlalchemy import create_engine, select, Table, MetaData, delete
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql import text

import os
from pathlib import Path
import requests
import json
from .datasource import DataSource
from .models import StructuredDB
from .utils import create_user_response
     
class CsvUpload(BaseModel):

    database: StructuredDB
    data_source: DataSource
    table_name: str
    append: bool | None = False

    def run(self):

        client_url = os.environ['MAJORDOMO_AI_CLIENT_URL']

        if self.database.db_type != 'SQL':
            raise Exception("Incorrect database type")

        match self.data_source.location:

            case "local":
                local_file_name = self.data_source.info.file_name
                os.path.basename(self.data_source.info.file_name)
                my_file = Path(local_file_name)
                if not my_file.is_file():
                    raise ValueError("Input file not found")

                file = {'file': open(local_file_name, 'rb')}
    
                resp  = requests.post(client_url + '/file_upload', files=file)

            case default:
                raise Exception("Incorrect file location type")

        try:
            headers = {"Content-Type": "application/json"}
            result = requests.post(client_url + '/csv_ingestion', data=json.dumps(self.model_dump(mode='json')), headers=headers)

        except Exception as e: raise

        return result

class GenAISQLQuery(BaseModel):

    user_token: str

    database: StructuredDB

    embedding_model : str
    genai_model : str
    table_names: list[str]
    query_str: str

    def run(self):

        client_url = os.environ['MAJORDOMO_AI_CLIENT_URL']

        if self.database.db_type != 'SQL':
            raise Exception("Incorrect database type")

        try:
            headers = {"Content-Type": "application/json"}
            result = requests.post(client_url + '/genai_sql_query', data=json.dumps(self.model_dump(mode='json')), headers=headers)
            response_json = create_user_response(result)

        except Exception as e: raise

        return response_json

def fetch_image_from_sql(database, table, image_id):

    print(table, image_id)

    if database.db_type != 'SQL':
        raise Exception("Incorrect database type")

    # Connect to DB and output data frame
    engine = create_engine(database.info.url + "/" + database.info.name)

    conn = engine.connect()

    metadata = MetaData()

    image_table = Table(table, metadata, autoload_with=engine)

    stmt = select(image_table).where(image_table.c.id == image_id)
    row = conn.execute(stmt)
    return(row.first().data)
