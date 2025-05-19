from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.sklearn
import pandas as pd
from typing import Dict
from database import insert_patient_data
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=5)

app = FastAPI()

model = mlflow.pyfunc.load_model("models:/Random/2")

class PatientsData(BaseModel):
    Temperature : float
    Pulse : float
    BloodPressure : float
    SpO2 : float
    RespiratoryRate : float
    BMI : float
    FastingGlucose : float
    Cholesterol : float
    StressLevel : float

@app.post("/predi")
def predict_diagnosis(data: PatientsData):
    try:
        input_data = pd.DataFrame([{
            'Temperature': data.Temperature,
            'Pulse': data.Pulse,
            'BloodPressure': data.BloodPressure,
            'SpO2': data.SpO2,
            'RespiratoryRate': data.RespiratoryRate,
            'BMI': data.BMI,
            'FastingGlucose': data.FastingGlucose,
            'Cholesterol': data.Cholesterol,
            'StressLevel': data.StressLevel
        }]).values

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
        executor.submit(insert_patient_data, data, message)
        print('Prédiction et Insertion avec succès✅✅')

        return {"Diagnostic": message}
        print('Prédiction et Insertion avec succès✅✅')


    except Exception as e:
        return {"detail": f"Erreur de prédiction : {str(e)}"}
