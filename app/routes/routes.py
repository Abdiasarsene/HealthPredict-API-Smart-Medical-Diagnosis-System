# api/routes.py
import asyncio
import logging
from fastapi import APIRouter, HTTPException
from app.schemas.schemas import PatientsData
from app.config_api import settings
from app.services.predictor import make_prediction
from app.model_loader import (
    load_mlflow_model, 
    load_bentoml_model,
    load_treatment_model_mlflow,
    load_treatment_model_bentoml
    )
import mlflow

# Logger
logger = logging.getLogger(__name__)
router = APIRouter()

# Variables globales
diagnosis_model = None
treatment_model = None
model_type = None

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

@router.on_event('startup')
async def startup_event():
    global diagnosis_model, treatment_model, model_type
    logger.info("🚀 Démarrage de l'API...")

    # === Chargement modèle de diagnostique ===
    try:
        diagnosis_model = await asyncio.wait_for(
            asyncio.to_thread(load_mlflow_model, settings.MLFLOW_MODEL), 
            timeout=10.0
        )
        logger.info("✅ Modèle de diagnostique MLflow chargé avec succès")
    except Exception as e:
        logger.warning(f"⚠️ Échec MLflow - Diagnostique : {str(e)}")
        try:
            diagnosis_model = load_bentoml_model(settings.BENTOML_MODEL)
            model_type = "BentoML"
            logger.info("✅ Fallback vers BentoML - Diagnostique OK")
        except Exception as bentoml_error:
            logger.critical(f"❌ Échec total : {bentoml_error}")
            raise RuntimeError(f"Impossible de charger un modèle : {e} / {bentoml_error}")
    
    # === Chargement modèle de tratement ===
    try:
        treatment_model = await asyncio.wait_for(
            asyncio.to_thread(load_treatment_model_mlflow, settings.MLFLOW_MODEL_TRAITEMENT),
            timeout=10.0
        )
        logger.info("✅✅ Modèle de traitement MLflow chargé")
        model_type = "MLflow"
    except Exception as e:
        logger.warning(f"⚠️Echec MLflow - Traitement : {str(e)}")
        try: 
            treatment_model = load_treatment_model_bentoml(settings.BENTOML_MODEL_TRAITEMENT)
            logger.info("✅✅ Fallback vers BentoML - Traitement OK")
            model_type = "BentoML"
        except Exception as e:
            logger.critical(f"❌ Impossible de charger le modèle de traitement : {bentoml_error}")
            raise RuntimeError(f"Error critique - Traitement : {e} / {bentoml_error}")


@router.post("/v1/disease")
async def predict_disease(data: PatientsData):
    global diagnosis_model,treatment_model, model_type
    try:
        input_dict = data.dict(by_alias=True)
        prediction = make_prediction(diagnosis_model,treatment_model, model_type, input_dict)
        return {
            "Diagnostique Trouvé": prediction["Diagnostique Trouvé"],
            "Traitement Adéquat": prediction['Traitement Adéquat'],
            "Statut": "Success",
            "Modèle Utilisé": model_type
        }
    except Exception as e:
        logger.error(f"Erreur de prédiction : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur serveur lors de la prédiction")
