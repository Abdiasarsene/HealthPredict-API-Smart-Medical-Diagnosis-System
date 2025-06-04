import os 
from pathlib import Path
from dotenv import load_dotenv

# Chemin absolu vers .env
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class Settings : 
    def __init__(self):
        self.DATASET_PATH = os.getenv("DATASET_PATH")
        self.MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME","default_experiment")
        self.MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
        self.ARTIFACT_PATH = os.getenv("ARTIFACT_PATH")
        self.MLFLOW_MODEL_NAME = os.getenv("MLFLOW_MODEL_NAME")

settings = Settings()