# app/services/predictor.py
import logging
from ray import get

from app.events.events_pipeline import get_pipeline, fallback_models_ready, fallback_models_cache
from app.fallback_fastapi.predictor_fallback import if_ray_serve_fails
from app.fallback_fastapi.loader_fallback import preload_models
from app.ray_serve.predictor_ray import predict_ray

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== ORCHESTRATOR ======
async def predict(input_df):
    if input_df is None or input_df.empty:
        raise ValueError("Input DataFrame is empty")

    # ====== TRY RAY SERVE ======
    pipeline_handle = get_pipeline()
    if pipeline_handle:
        try:
            result = await predict_ray(input_df, pipeline_handle)
            result["model_type"] = "RayServe"
            logger.info("✅ Prediction done using Ray Serve")
            return result
        except Exception as e:
            logger.warning(f"⚠️ Ray Serve failed during prediction: {e}")
            logger.exception("🔎 Full Ray Serve exception trace:")
            logger.info("🔃 Falling back to FastAPI models")

    # ====== FALLBACK FASTAPI ======
    logger.info("🔍 Checking fallback models readiness")
    if fallback_models_ready:
        logger.info("✅ Fallback models ready flag is True")
    else:
        logger.warning("⚠️ fallback_models_ready=False, need to load fallback models")

    # Vérifier si les modèles sont en cache
    diagnosis_model = fallback_models_cache.get("diagnosis")
    treatment_model = fallback_models_cache.get("treatment")

    if not diagnosis_model or not treatment_model:
        logger.info("🔃 Preloading fallback models...")
        try:
            diagnosis_model, treatment_model = await preload_models()
            fallback_models_cache["diagnosis"] = diagnosis_model
            fallback_models_cache["treatment"] = treatment_model
            logger.info("✅ Fallback models preloaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to preload fallback models: {e}")
            logger.exception("🔎 Full stack trace during preload_models()")
            raise RuntimeError(f"Fallback models loading failed: {e}")

    # Après preload, vérifier à nouveau
    diagnosis_model = fallback_models_cache.get("diagnosis")
    treatment_model = fallback_models_cache.get("treatment")
    if diagnosis_model and treatment_model:
        logger.info("✅ Using fallback models for prediction")
        return if_ray_serve_fails(input_df, diagnosis_model, treatment_model)

    # ====== NO MODEL AVAILABLE ======
    logger.critical(
        "❌ No prediction model available: Ray Serve not deployed "
        "and fallback models not ready"
    )
    logger.exception("🔎 Fallback models and Ray Serve both unavailable")
    raise RuntimeError(
        "No prediction model available: Ray Serve not deployed and fallback not ready"
    )
