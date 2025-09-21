# api/routes.py
import time
import logging
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from app.schemas.schema import PatientsData
from app.core.data_transformer import normalize_input
from app.services.predictor import predict
from app.services.output_message import format_output

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== INITIALISATION ======
router = APIRouter(prefix="/v1", redirect_slashes=True)

# ====== ENDPOINT ======
@router.post("/predict/examination_result")
async def predict_route(data: PatientsData):
    # Validation des données d'entrée
    try:
        validated_data = PatientsData(**data.dict())
        input_dict = validated_data.dict(by_alias=True)
        logger.info("✅ Inputdata validated")
    except ValidationError as ve:
        logger.error("❌ Validation des données échouées", extra={"Events": "Validation Failed"})
        raise HTTPException(
            status_code=422,
            detail={"Message": "Données d'entrée invalides", "Errors": ve.errors()}
        )

    # Transformation en dataframe
    try:
        input_df = normalize_input(input_dict)
        logger.info("✅ Ready for prediction")
    except Exception as e:
        logger.error(f"❌ Error DataFrame: {e} ")
        raise HTTPException(status_code=500, detail=f"Error DataFrame: {e}")

    # Prediction
    start = time.time()
    try:
        result = await predict(input_df)
        diagnosis_pred = result.get("diagnosis")
        treatment_pred = result.get("treatment")
    except Exception as e:
        logger.critical(f"❌ Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    # Sortie de prédiction
    latency_ms = (time.time() - start) * 1000
    try:
        response = format_output(
            diagnosis_pred=diagnosis_pred,
            treatment_pred=treatment_pred,
            model_type=result.get("model_type", "Unknown"),
            latency_ms=latency_ms
        )
    except Exception as e:
        logger.error(f"❌ Formatage du message échoué : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Formatage du message échoué: {e}")
    
    return response