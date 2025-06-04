# Importation des bibliothèques
import os
import logging
import pandas as pd 
from src.model.config_ml import settings

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== CHARGEMENT DU JEU DE DONNEES ======
def load_dataset():
    dataset_path = settings.DATASET_PATH
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Le fichier {dataset_path} est introvable")
    
    try : 
        df = pd.read_excel(dataset_path)
        logger.info(f"✅✅ Données chargées avec succès")
        return df
    except Exception as e: 
        raise ValueError(f"Erreur lors du chargement des données : {e}")