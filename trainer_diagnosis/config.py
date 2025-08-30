# Importation des libraires nécessaires
import os 
from dotenv import load_dotenv

# ====== INITIALISATION ======
load_dotenv()

# ====== PARAMETRAGE ======
class Settings : 
    def __init__(self):
        self.DATASET_PATH = os.getenv("DATASET_PATH","")
        self.EXPERIMENT_NAME = os.getenv("EXPERIMENT_DIAGNOSIS","")
        self.MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "")
        self.MLFLOW_MODEL_NAME = os.getenv("MLFLOW_MODEL_NAME","")
        self.target_column = os.getenv("TARGET_COLUMN","")
        self.pointless_cols = ["Diagnostique", "Traitement"]

settings = Settings()