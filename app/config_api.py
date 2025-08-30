import os
from dotenv import load_dotenv

# Chemin absolu vers .env
load_dotenv()

class Settings : 
    def __init__(self) :
        self.MLFLOW_TRACKING_URI= os.getenv("MLFLOW_TRACKING_URI")
        self.MLFLOW_MODEL_NAME = os.getenv("MLFLOW_MODEL_NAME")
        self.MLFLOW_MODEL_VERSION = os.getenv("MLFLOW_MODEL_VERSION")
        self.MLFLOW_MODEL = os.getenv("MLFLOW_MODEL")
        self.BENTOML_MODEL = os.getenv("BENTOML_MODEL")
        self.MLFLOW_MODEL_TRAITEMENT = os.getenv("MLFLOW_MODEL_TRAITEMENT")
        self.BENTOML_MODEL_TRAITEMENT = os.getenv("BENTOML_MODEL_TRAITEMENT")
    
        self.API_TITLE = os.getenv("API_TITLE")
        self.API_VERSION = os.getenv("API_VERSION")
        self.API_DESCRIPTION = os.getenv("API_DESCRIPTION")

settings = Settings()