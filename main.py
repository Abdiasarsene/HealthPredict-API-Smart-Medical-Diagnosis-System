from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.sklearn
import pandas as pd
from typing import Dict

app = FastAPI(
    title="Health Predict App",
    description="Prédiction des maladies à partir des données médicales."
)

model_uri = "mlruns/785681529560409716/3a8daef69e284135ad68e38d7d2e3949/artifacts/Logistic_Regression"
model = mlflow.sklearn.load_model(model_uri)
print("Modèle Logistic Regression chargé avec succès ✅")

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
        }])

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

        return {"Diagnostic": message}

    except Exception as e:
        return {"detail": f"Erreur de prédiction : {str(e)}"}
