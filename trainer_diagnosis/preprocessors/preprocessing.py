# Importation des bibliotèqus utiles
import logging
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from category_encoders import CatBoostEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== PRETRAIMENT DES DONNEES ======
def build_preprocessing_pipeline(data):
    try:
        # Séparation des features numériques et catégorielles
        features = data.drop(columns=["Diagnostique", "Traitement"])
        num_cols = features.select_dtypes(include=["int64", "float64"]).columns.tolist()
        cat_cols = features.select_dtypes(include=['object']).columns.tolist()
        
        # Log des colonnes catégorielles et numériques
        logger.info(f"📊 Colonnes numériques : {num_cols}")
        logger.info(f"📊 Colonnes catégorielles : {cat_cols}")
        
        # Colonnes numériques
        num_pipeline = Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scaler", RobustScaler())
        ])
        
        # Colonnes catégorielles
        cat_pipeline = Pipeline([
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("encoder", CatBoostEncoder())
        ])
        
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", num_pipeline, num_cols),
                ("cat", cat_pipeline, cat_cols)
            ]
        )
        logger.info("✅ Prétraitement terminé")

        return preprocessor
    except Exception as e : 
        logger.error(f"Erreur : {str(e)}")
        logger.exception("Stack trace : ")