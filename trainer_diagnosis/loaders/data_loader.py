# Importation des bibliothèques
import logging
import pandas as pd 
from trainer_diagnosis.config import settings
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== IMPORTATION ET ENCODAGE DU LABEL ======
def load_and_encode_dataset():
    try:
        # Chargement des données
        dataset = settings.DATASET_PATH
        if dataset is None:
            raise FileNotFoundError(f"Oups chemin non trouvé : {dataset}")
        data = pd.read_excel(dataset)
        logger.info("✅✅ Jeu de données importé")
        
        # Séparation des features + label
        x = data.drop(columns=settings.pointless_cols)
        y = LabelEncoder().fit_transform(data[settings.target_column])
        
        # Division des données en entrainement et de test 
        x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)
        logger.info("📊 Données divisées en train/test")
        
        return x_train, x_test, y_train, y_test, data
    except Exception as e: 
        logger.error(f"Erreur : {str(e)}")
        logger.exception("Stack trace : ")
        raise e 