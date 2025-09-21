# app/events/events_pipeline.py
import ray
import asyncio
import logging
from ray import serve
from fastapi import FastAPI
from app.events.events_diagnosis import get_diagnosis
from app.events.events_treatement import get_treatment
from app.deployments.pipeline_deployment import PipelineDeployment
from app.fallback_fastapi.loader_fallback import preload_models 

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== INITIALIZE ======
pipeline_handle = None
fallback_models_cache = {"diagnosis": None, "treatment": None}
fallback_models_ready = False  

# ====== GETTERS ======
def get_pipeline():
    return pipeline_handle

def get_fallback_models():
    if fallback_models_ready:
        return fallback_models_cache["diagnosis"], fallback_models_cache["treatment"]
    return None, None

# ====== STARTUP EVENTS ======
def register_startup_events(app: FastAPI, ray_timeout: int = 20):
    @app.on_event("startup")
    async def startup_events():
        global pipeline_handle, fallback_models_cache, fallback_models_ready

        async def _start_ray_pipeline():
            global pipeline_handle

            # Get Handle Models Ray
            _, _, diagnosis_handle = get_diagnosis()
            _, _, treatment_handle = get_treatment()

            # Deploy pipeline 
            pipeline_handle = await PipelineDeployment.deploy(diagnosis_handle, treatment_handle)

            # Warmup minimal
            dummy_input = {"patient_id": "dummy", "symptoms": ["test"]}
            try:
                await pipeline_handle.remote(dummy_input)
                logger.info("✅ Ray Pipeline warmup OK")
            except Exception as e:
                logger.warning(f"⚠️ Warmup dummy failed: {e}")
                logger.exception("⚠️ Warmup stack trace:")

        try:
            logger.info("🔃 Deploying Ray Serve Pipeline")
            # Init Ray Serve
            ray.init(address="auto", ignore_reinit_error=True)
            serve.start(detached=True)

            # Timeout pour éviter de bloquer le startup
            await asyncio.wait_for(_start_ray_pipeline(), timeout=ray_timeout)
            logger.info("✅ Ray Serve Pipeline Deployed")

        except asyncio.TimeoutError:
            logger.error(f"❌ Ray Serve startup timed out after {ray_timeout}s")
        except Exception as e:
            logger.error(f"❌ Ray Serve failed during startup: {str(e)}")
            logger.exception("⚠️ Ray Serve startup stack trace:")
        finally:
            # Préchargement fallback FastAPI si Ray échoue
            if pipeline_handle is None and not fallback_models_ready:
                try:
                    logger.info("🔃 Attempting FastAPI fallback preload...")
                    diagnosis_model, treatment_model = await preload_models()

                    # === LOG DETAILS ===
                    if diagnosis_model is None:
                        logger.error("❌ Diagnosis model preload returned None")
                    else:
                        logger.info("✅ Diagnosis model successfully preloaded")

                    if treatment_model is None:
                        logger.error("❌ Treatment model preload returned None")
                    else:
                        logger.info("✅ Treatment model successfully preloaded")

                    # === UPDATE CACHE ===
                    fallback_models_cache["diagnosis"] = diagnosis_model
                    fallback_models_cache["treatment"] = treatment_model

                    if diagnosis_model and treatment_model:
                        fallback_models_ready = True
                        logger.info("✅ FastAPI fallback activated")
                        logger.info("✅ Models Loaded and Ready")
                    else:
                        logger.critical(
                            "❌ Fallback preload did not initialize both models: "
                            f"diagnosis={diagnosis_model}, treatment={treatment_model}"
                        )
                except Exception as e:
                    logger.critical(f"❌ FastAPI fallback preload failed: {str(e)}")
                    logger.exception("⚠️ FastAPI preload stack trace:")
