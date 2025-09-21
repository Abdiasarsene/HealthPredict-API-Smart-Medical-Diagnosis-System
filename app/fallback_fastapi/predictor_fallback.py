# app/fallback_fastapi/fallback_predict.py  
import logging

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== FALLBACK PREDICTION ======
def if_ray_serve_fails(input_df, diagnosis_model, treatment_model):
    # DataFrale
    if input_df is None or input_df.empty:
        raise ValueError("Input DataFrame Empty")
    
    # Load models
    if diagnosis_model is None or treatment_model is None:
        raise ValueError("Models must be provided for fallback prediction")

    try:
        # ===== Predict Diagnosis =====
        diagnosis_result = diagnosis_model.predict(input_df)

        # ===== Prepare Treatment Input =====
        treatment_input = input_df.copy()
        treatment_input["Diagnostique"] = diagnosis_result

        # ===== Predict Treatment =====
        treatment_result = treatment_model.predict(treatment_input)

        # ===== Return result =====
        logger.info("✅ Prediction Done")
        return {
            "diagnosis": diagnosis_result,
            "treatment": treatment_result
        }
    
    except Exception as e:
        logger.error(f"❌ Error Detected : {str(e)}")
        logger.exception("⚠️  Stack trace : ")