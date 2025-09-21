# app/models_loaders/treatment_loader.py
import logging
import mlflow
import bentoml
from app.config import settings

# ======= LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== TREATMENT MODEL FUNCITON ======
def mlflow_treatment(path):
    try:
        # MLflow
        mlflow.set_tracking_uri(settings.tracking_uri)
        logger.info(f"Tracking Used : {settings.tracking_uri}")
        
        # Upload
        model = mlflow.pyfunc.load_model(path)
        if model is None:
            raise RuntimeError("⚠️ Mlflow failed")
        return model
    
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.exception("Stack trace :")

# ====== BENTOML FUNCTION ======
def bentoml_treatment(tag):
    try:
        # BentoML Packaged Model
        model = bentoml.sklearn.load_model(tag)
        if model is None:
            raise RuntimeError("⚠️ BentoML failed")
        return model 
    
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.exception("Stack trace : ")
