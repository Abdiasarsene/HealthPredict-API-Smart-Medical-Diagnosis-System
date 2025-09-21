# app/fallback/fallback_loader.py
import asyncio
import logging
from app.models_loaders.diagnosis_loader import mlflow_diagnosis, bentoml_diagnosis
from app.models_loaders.treatment_loader import mlflow_treatment, bentoml_treatment
from app.config import settings
from app.services import predictor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def preload_models(timeout: float = 10.0):
    diagnosis_model = None
    treatment_model = None
    diagnosis_mode = "mlflow"

    # ===== Diagnosis Model =====
    try:
        logger.info("🔃 Loading Diagnosis MLflow")
        diagnosis_model = await asyncio.wait_for(
            asyncio.to_thread(mlflow_diagnosis, settings.mlflow_maladie),
            timeout=timeout
        )
        logger.info("✅ Diagnosis MLflow Loaded")
    except Exception as e:
        logger.warning(f"⚠️  Warning : {str(e)}")
        diagnosis_mode = "bentoml"
        try:
            logger.info("🔃 Diagnosis BentoML Fallback")
            diagnosis_model = bentoml_diagnosis(settings.bentoml_maladie)
            logger.info("✅ Diagnosis BentoML Loaded")
        except Exception as e:
            logger.critical(f"❌ Diagnosis Fallback Failed: {str(e)}", exc_info=True)

    # ===== Treatment Model =====
    if diagnosis_mode == "mlflow":
        # On reste cohérent : tenter MLflow d'abord
        try:
            logger.info("🔃 Loading Treatment MLflow")
            treatment_model = await asyncio.wait_for(
                asyncio.to_thread(mlflow_treatment, settings.mlflow_traitement),
                timeout=timeout
            )
            logger.info("✅ Treatment MLflow Loaded")
        except Exception as e:
            logger.warning(f"⚠️ Warning : {e}")
            logger.info("🔃 Forcing Treatment BentoML Fallback")
            try:
                treatment_model = bentoml_treatment(settings.bentoml_traitement)
                logger.info("✅ Treatment BentoML Loaded")
            except Exception as e:
                logger.critical(f"❌ Treatment Fallback Failed: {str(e)}", exc_info=True)

    else:  
        # Si diagnosis est en fallback, alors treatment aussi directement
        try:
            logger.info("🔃 Skipping MLflow, using Treatment BentoML directly")
            treatment_model = bentoml_treatment(settings.bentoml_traitement)
            logger.info("✅ Treatment BentoML Loaded")
        except Exception as e:
            logger.critical(f"❌ Treatment Fallback Failed: {str(e)}", exc_info=True)

    # Si les deux modèles sont bien chargés
    if diagnosis_mode is not None and treatment_model is not None:
        predictor.fallback_models_ready = True
        logger.info("✅ Fallback models are ready (flag set to True)")
    else:
        predictor.fallback_models_ready = False
        logger.critical("❌ Models failed to load, fallback_models_ready=False")
    
    return diagnosis_model, treatment_model