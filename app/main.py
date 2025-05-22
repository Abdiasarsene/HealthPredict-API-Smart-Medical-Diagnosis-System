#  Importation des bibliothèques
import os 
import logging
import pandas as pd
import mlflow.sklearn
from typing import Dict
from dotenv import load_dotenv
from app.schemas import PatientsData
from pydantic_settings import BaseSettings
from app.database import init_db, insert_patient_data
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI, HTTPException, BackgroundTasks

# ====== VARIABLE D'ENVIRONNEMENT ======
load_dotenv()
model_name = os.getenv("MODEL_NAME")
model_version = os.getenv("MODEL_VERSION")
api_title = os.getenv("API_TITLE")
api_description = os.getenv("API_DESCRIPTION")
api_version = os.getenv("API_VERSION")

# ====== CONFIGURATION  ======
class Setting(BaseSettings): 
    mlflow_model_name : str = model_name
    mlflow_model_version : str = model_version
    max_workers : int = 5
    
    class Config:
        env_file = ".env"
        extra = "allow"
settings = Setting()

# ====== LOGGING ======
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== CREATION DE L'API ======
app = FastAPI(
    title = api_title,
    description= api_description,
    version= api_version
)

# ====== INSTRUMENTATION DE L'APPLICATION ======
instrumntator = Instrumentator()
instrumntator.instrument(app).expose(app)

@app.on_event('startup')
async def startup_event():
    print("L'application démarre")

# ====== HOME ======
@app.get("/home")
async def homepage():
    return{"Status":"OK ✅✅"}

# ====== CHARGEMENT DU MODELE AU DEMARRAGE ======
model =  None

@app.on_event("startup")
async def load_model() : 
    global model
    try:
        model = mlflow.pyfunc.load_model(f"models:/{settings.mlflow_model_name}/{settings.mlflow_model_version}")
        logger.info("✅ Modèle chargé ")
        return model
    except Exception as e: 
        logger.error(f"❌ Erreur de chargement du modèle {str(e)}")
        raise e

# ====== ENDPOINTS ======
@app.post("/v1/desease")
async def predict_diagnosis(
    data: PatientsData,
    background_tasks : BackgroundTasks
):
    try:
        global model
        input_data = pd.DataFrame([data.dict()])
        prediction = model.predict(input_data)
        predicted_class = int(prediction[0])
        
        diagnosis_mapping = {
            0: "l'Asthme",
            1: "COVID-19",
            2: "Diabète",
            3: "la Grippe",
            4: "l'Hypertension"
        }
        message = f"Le patient souffre de {diagnosis_mapping.get(predicted_class, 'une maladie inconnue')}."
        
        # Insertion en tâche de fond sans bloquer
        logging.info("📢 Début de l'insertion des données ...")
        # background_tasks.add_task(insert_patient_data, data, message)
        insert_patient_data(data, message)
        logger.info('✅ INsertion envoyée en tâche de fond !')
        return {"Diagnostic": message,
                "Code" : predicted_class,
                "Statut": "Success"
        }
    
    except Exception as e:
        logger.error(f"Erreur de prédiction : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")