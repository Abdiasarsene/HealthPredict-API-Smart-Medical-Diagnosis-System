# deployments/diagnosis_deployment.py
import sys
import logging
from ray import serve
import asyncio

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== RAY SERVE DIAGNOSIS MODEL ======
class DiagnosisDeployment:
    try:
        @serve.deployment
        class Diagnosis:
            def __init__(self, model, model_type):
                self.model = model
                self.model_type = model_type
            
            # Call Predictor + Timeout to avoid blocking
            async def __call__(self, input_dict: dict):
                try:
                    return await asyncio.wait_for(
                        asyncio.to_thread(
                            self.model.predict,
                            self.model_type,
                            input_dict
                        ),
                        timeout=10.0
                    )
                except asyncio.TimeoutError:
                    return {"Error": "Prediction timed out"}
        
        @classmethod
        def deploy(cls, model, model_type): 
            # Bind le modèle à Ray Serve
            return cls.Diagnosis.bind(model, model_type)

    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.exception("⚠️ Stack Trace")
        sys.exit(1)