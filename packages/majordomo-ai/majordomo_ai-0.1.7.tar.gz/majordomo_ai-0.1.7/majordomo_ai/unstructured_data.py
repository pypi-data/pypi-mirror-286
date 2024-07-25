import os
import json
import requests
from pydantic import BaseModel, ValidationError

from .datasource import DataSource
from .dataset import *
from .models import *
from .utils import create_user_response
from pathlib import Path

class TextIngestionType(str, Enum):
    base = "Base" 
    summary ="Summary" 

class PDFExtractorTypeEnum(str, Enum):
    llamaparse = "LlamaParse"
    pymupdf = "PyMuPDF"
    pdf2image = "PDF2Image"

class TextIngestion(BaseModel):

    user_token : str

    ingestion_type : TextIngestionType | None = "Base"

    # Location of input data.
    data_source: DataSource

    # Document handling.
    pdf_extractor: PDFExtractorTypeEnum | None = "PyMuPDF"
    chunking_type : str | None = 'normal'
    chunk_size : int | None = 1024
    genai_model : str | None = ''

    # Mandatory index where parsed data is stored.
    dataset : Dataset

    def run(self):

        client_url = os.environ['MAJORDOMO_AI_CLIENT_URL']

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
               pass

        try:
            headers = {"Content-Type": "application/json"}
            result = requests.post(client_url + '/text_ingestion', data=json.dumps(self.model_dump(mode='json')), headers=headers)
            print(result.content)
            response_json = create_user_response(result)
        except Exception as e: raise

        return response_json

class ImageIngestion(BaseModel):

    user_token : str

    # Location of input data.
    data_source: DataSource

    # Document handling.
    pdf_extractor: PDFExtractorTypeEnum | None = "PDF2Image"
    embedding_model: str 

    # VectorDB Index where parsed data is stored.
    dataset : Dataset
    dimensions : int | None = 384

    # Database where images are stored.
    image_database : StructuredDB
    table_name : str

    def run(self):

        client_url = os.environ['MAJORDOMO_AI_CLIENT_URL']

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
               pass

        try:
            headers = {"Content-Type": "application/json"}
            result = requests.post(client_url + '/image_ingestion', data=json.dumps(self.model_dump(mode='json')), headers=headers)
            response_json = create_user_response(result)
        except Exception as e: raise

        return response_json

