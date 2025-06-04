import os
from pathlib import Path
from dotenv import load_dotenv

# Chemin absolu vers .env
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class Settings : 
    def __init__(self) :
        self.MLFLOW_TRACKING_URI= os.getenv("MLFLOW_TRACKING_URI")
        self.MLFLOW_MODEL_NAME = os.getenv("MLFLOW_MODEL_NAME")
        self.MLFLOW_MODEL_VERSION = os.getenv("MLFLOW_MODEL_VERSION")
    
        self.API_TITLE = os.getenv("API_TITLE")
        self.API_VERSION = os.getenv("API_VERSION")
        self.API_DESCRIPTION = os.getenv("API_DESCRIPTION")

settings = Settings()   