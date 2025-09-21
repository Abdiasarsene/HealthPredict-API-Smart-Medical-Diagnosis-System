# app/models_loaders/diagnosis_loader.py
import logging
import mlflow
import bentoml
from api.config import settings

# ====== LOGGING =======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== MLFLOW LOAD FUNCTION ======
def mlflow_diagnosis(path):
    try:
        # MLflow Server
        mlflow.set_tracking_uri(settings.tracking_uri)
        logger.info(f"Tracking Used : {settings.tracking_uri}")
        
        # Upload the model
        model = mlflow.pyfunc.load_model(path)
        if model is None :
            raise RuntimeError("⚠️ MLflow failed")
        return model
    
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.exception("Stack trace : ")

# ====== BENTOML LOAD FUNCTION ======
def bentoml_diagnosis(tag):
    try:
        # BentoML Packages Model
        model = bentoml.sklearn.load_model(tag)
        if model is None:
            raise RuntimeError("⚠️ BentoML failed")
        return model
    
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.exception("Stack trace : ")