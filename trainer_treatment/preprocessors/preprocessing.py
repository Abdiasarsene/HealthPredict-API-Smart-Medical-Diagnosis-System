# Importation des libraires nécessaires
import logging
from trainer_treatment.config import settings
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import KNNImputer, SimpleImputer
from category_encoders import CatBoostEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== PREPROCESSING ======
def get_preprocessing(data):
    try:
        features = data.drop(columns=settings.target_column)
        num_cols = features.select_dtypes(include=['int64', 'int32', 'float64']).columns.tolist()
        cat_cols = features.select_dtypes(include=['object']).columns.tolist()
        
        # Pipeline
        num_transformer = Pipeline([
            ("impute", KNNImputer(n_neighbors=3)),
            ("scale", MinMaxScaler())
        ])
        
        cat_transformer = Pipeline([
            ("impute", SimpleImputer(strategy='most_frequent')),
            ("encoder", CatBoostEncoder())
        ])
        
        preprocessor = ColumnTransformer([
            ('num', num_transformer, num_cols),
            ('cat', cat_transformer, cat_cols)
        ])
        logger.info("✅ Preprocessing done")
        return preprocessor
    
    except Exception as e:
        logger.error(f"Erreur : {str(e)}")
        logger.exception("Stack trace : ")