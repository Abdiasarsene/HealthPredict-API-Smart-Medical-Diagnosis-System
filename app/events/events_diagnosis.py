# app/events/events_diagnosis.py
import logging 
import asyncio
from fastapi import FastAPI
from ray import serve

from app.config import settings
from app.models_loaders.diagnosis_loader import mlflow_diagnosis, bentoml_diagnosis
from app.deployments.diagnosis_deployment import DiagnosisDeployment

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== INITALIZE ======
diagnosis_model = None
diagnosis_type = None
diagnosis_handle = None

# ====== EVENTS DIAGNOSIS MODEL ======
def get_diagnosis():
    return diagnosis_model, diagnosis_type, diagnosis_handle

def register_startup_events(app:FastAPI):
    @app.on_event("startup")
    async def startup_event():
        global diagnosis_model, diagnosis_type, diagnosis_handle
        
        # MLflow
        try:
            logger.info("🔃 Loading MLflow Diagnosis")
            diagnosis_model = await asyncio.wait_for(asyncio.to_thread(mlflow_diagnosis, settings.mlflow_maladie), timeout=10.0)
            diagnosis_type = "MLflow"
            logger.info("✅ Diagnosis Model loaded")
        except Exception as e:
            logger.warning(f"⚠️  Warning : {str(e)}")
            
            # BentoML en fallback
            try:        
                logger.info("🔃 BentoML fallback Starting")
                diagnosis_model = bentoml_diagnosis(settings.bentoml_maladie)
                diagnosis_type = "BentoML"
                logger.info("✅ Diagnosis Model loaded")
            except Exception:
                logger.critical(f"❌ Critical : {str(e)}")
                logger.exception("Stack trace : ")
        
        # Deploy Ray Serve
        logger.info("🔃 Deploying Diagnosis Ray Serve")
        diagnosis_deployment = DiagnosisDeployment.deploy(diagnosis_model, diagnosis_type)
        serve.run(diagnosis_deployment, name="HealtcareApp")
        diagnosis_handle = serve.get_deployment_handle("Diagnosis", app_name="HealthcareApp")
