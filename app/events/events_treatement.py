# app/events/events_pipeline.py
import logging
import asyncio
from fastapi import FastAPI
from ray import serve

from app.config import settings
from app.models_loaders.treatment_loader import mlflow_treatment, bentoml_treatment
from app.deployments.treatment_deployment import TreatmentDeployment

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== INITIALIZE ======
treatment_model = None
treatment_type = None
treatment_handle = None

# ====== EVENTS TREATENT ======
def get_treatment():
    return treatment_model, treatment_type, treatment_handle

def register_startup_events(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        global treatment_model, treatment_type, treatment_handle
        
        # MLflow
        try:
            logger.info("🔃 Loading Treatment Model")
            treatment_model = await asyncio.wait_for(asyncio.to_thread(mlflow_treatment, settings.mlflow_traitement), timeout=10.0)
            treatment_type = "MLflow"
            logger.info("✅ Treatment Model loaded")
        except Exception as e:
            logger.warning(f"⚠️  Warning : {str(e)}")
            
            # BentoML fallback
            try:
                logger.info("🔃 Treatment BentoML fallback")
                treatment_model = bentoml_treatment(settings.bentoml_traitement)
                treatment_type = "BentoML"
                logger.info("✅ Treatment Model Loaded")
            except Exception as e:
                logger.critical(f"❌ Critical : ;{str(e)}")
                logger.exception("Stack trace : ")
        
        # Deploy
        logger.info("🔃 Deploying Treatment Ray Serve")
        treatment_deployment = TreatmentDeployment.deploy(treatment_model, treatment_type)
        serve.run(treatment_deployment, name="HealthcareApp")
        treatment_handle = serve.get_deployment_handle("Treatment", app_name="HealthcareApp")
