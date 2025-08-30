# Importation des librairies nécessaires
import logging
import pandas as pd
from trainer_treatment.config import settings
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== LOAD + SPLIT ======
def load_and_encode():
    try:
        # Load data
        data = pd.read_excel(settings.dataset)
        logger.info("✅ Data loaded")

        # Data Preparation
        x = data.drop(columns=settings.target_column)
        y = LabelEncoder().fit_transform(data[settings.target_column])

        # Split
        x_train, x_test, y_train, y_test = train_test_split(x, y,random_state=42, test_size=0.2)
        logger.info("✅ Split done")
        return x_train, x_test, y_train, y_test, data
    
    except Exception as e:
        logger.error(f"Erreur : {str(e)}")
        logger.exception("Stack trace : ")