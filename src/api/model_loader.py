import logging
import mlflow
import mlflow.pyfunc
from src.api.config_api import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_model():
    """
    Charge un modèle MLflow à partir du nom et de la version spécifiée dans les varibales d'environemment 
    """
    
    try : 
        # Définir l'URI de tracking de MLflow
        if not settings.MLFLOW_TRACKING_URI:
            raise ValueError("❌ MLFLOW_TRACKING_URI non défini dans le fichier .env")
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        logger.info(f"📡 MLflow Tracking URI :  {settings.MLFLOW_TRACKING_URI}")
        
        # Construire l'URI du modèle
        if not settings.MLFLOW_MODEL_NAME: 
            raise ValueError("❌ Nom du modèle non défini")
        model_uri = f"models:/{settings.MLFLOW_MODEL_NAME}/{settings.MLFLOW_MODEL_VERSION}"
        
        logger.info(f"📡 Chargement du modèle depuis : {model_uri}")
        model = mlflow.pyfunc.load_model(model_uri)
        
        logger.info(f"✅ Modèle MLflow chargé avec succès")
        return model
    
    except Exception as e: 
        logger.error(f"❌ Erreur lors du chargement du modèle MLflow : {str(e)}")
        raise e