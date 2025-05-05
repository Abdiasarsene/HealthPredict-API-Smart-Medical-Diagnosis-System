from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.sklearn
import pandas as pd
from typing import Dict
from database import insert_patient_data

app = FastAPI(
    title="Health Predict App",
    description="Prédiction des maladies à partir des données médicales."
)

model = mlflow.pyfunc.load_model("models:/Logistic_Regression/Production")
print("Modèle Regression Logistique chargé avec succès ✅")

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

# Initialisation de l'application
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API HealthPredict"}

# Début de prédiction
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

        # Prédiction
        prediction = model.predict(input_data)
        predicted_class = int(prediction[0])

        # Dictionnaire des diagnostics
        diagnosis_mapping = {
            0: "l'Asthme",
            1: "COVID-19",
            2: "Diabète",
            3: "la Grippe",
            4: "l'Hypertension"
        }

        # Message lisible pour l'utilisateur
        message = f"Le patient souffre de {diagnosis_mapping.get(predicted_class, 'une maladie inconnue')}."

        # Enregistrer dans la base de données
        insert_patient_data(data, message)
        
        return {"Diagnostic": message}

    except Exception as e:
        return {"detail": f"Erreur de prédiction : {str(e)}"}
