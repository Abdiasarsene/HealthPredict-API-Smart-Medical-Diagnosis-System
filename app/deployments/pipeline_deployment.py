# app/deployments/pipeline_deployment.py
from app.schemas.schema import PatientsData
from ray import serve
import asyncio
import logging
import sys

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== PIPELINE DEPLOYMENT ======
class PipelineDeployment:
    try:
        @serve.deployment
        class Pipeline:
            def __init__(self, diagnosis_handle, treatment_handle):
                self.diagnosis_handle = diagnosis_handle
                self.treatment_handle = treatment_handle

            async def __call__(self, input_dict: dict):
                # --- Cas warmup ---
                if isinstance(input_dict, dict) and input_dict.get("warmup"):
                    return {"status": "Pipeline warmup OK ✅"}

                # ===== Step 1: Diagnosis Prediction =====
                try:
                    diagnosis_result = await asyncio.wait_for(
                        self.diagnosis_handle.remote(input_dict),
                        timeout=10.0
                    )
                except Exception as e:
                    return {"Error": f"Diagnosis failed: {str(e)}"}

                # ===== Step 2: Treatment Prediction =====
                treatment_input = {"Diagnostique": diagnosis_result, **input_dict}
                try:
                    treatment_result = await asyncio.wait_for(
                        self.treatment_handle.remote(treatment_input),
                        timeout=10.0
                    )
                except Exception as e:
                    return {"error": f"Treatment failed: {str(e)}"}

                return {
                    "diagnosis": diagnosis_result,
                    "treatment": treatment_result
                }

        @classmethod
        async def deploy(cls, diagnosis_handle, treatment_handle):
            app = cls.Pipeline.bind(diagnosis_handle, treatment_handle)
            serve.run(app, name="HealthcareApp")
            return serve.get_deployment_handle("Pipeline", app_name="HealthcareApp")

    except Exception as e:
        logger.error(f"❌ Erreur Détectée : {str(e)}")
        logger.exception("⚠️ Stack Trace : ")
        sys.exit(1)