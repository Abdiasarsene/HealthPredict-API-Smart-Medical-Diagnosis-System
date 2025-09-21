# app/ray_serve/predictor_ray.py  
import logging

# ====== LOGGING =======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== PREDICTION RAY SERVE ======
async def predict_ray(input_df, pipeline_handle):
    if input_df is None or input_df.empty:
        raise ValueError("Input DataFrame is empty")
    
    if pipeline_handle is None:
        raise ValueError("Pipeline handle must be provided for Ray Serve prediction")
    
    try:
        # Appel direct à la pipeline Ray Serve
        result = await pipeline_handle.remote(input_df)
        
        # Minimum result validation
        if not result or "Diagnosis" not in result or "Treatment" not in result:
            raise RuntimeError("Prediction result from Ray Serve invalid")
        
        logger.info("✅ Ray Serve Prediction Done")
        return result
    
    except Exception as e:
        logger.error(f"❌ Error Detected in Ray Serve prediction: {e}")
        logger.exception("⚠️  Stack trace : ")
        raise