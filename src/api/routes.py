from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.api.schemas import PatientsData
from src.api.database import insert_patient_data
from src.api.diagnosis import make_prediction

router = APIRouter()

@router.post("/v1/disease")
async def predict_disease(data: PatientsData, background_tasks : BackgroundTasks): 
    try: 
        message, prediction_code = make_prediction(data)
        background_tasks.add_task(insert_patient_data, data, message)
        return {
            "Diagnostique" : message,
            "Code" : prediction_code,
            "Statut" : "Success"
        }
        
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))
