import pandas as pd
from src.api.model_loader import load_model

model = load_model()

diagnosis_mapping = {
    0 : "l'Asthme",
    1 : "COVID_19",
    2 : "Diabète",
    3 : "la Grippe",
    4 : "l'Hypertension"
}

# Lazy load
_model = None

def get_model():
    global _model
    if _model is None:
        _model = load_model()
    return _model

def make_prediction(data):
    input_df = pd.DataFrame([data.dict()])
    prediction = model.predict(input_df)
    predicted_class = int(prediction[0])
    message = f"Le patient souffre de {diagnosis_mapping.get(predicted_class, "Une maladie inconnue")}"
    return message, predicted_class