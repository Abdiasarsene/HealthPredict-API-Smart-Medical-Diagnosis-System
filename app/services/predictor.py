# Importations des libraires importantes
import pandas as pd
from fastapi import HTTPException

diagnosis_mapping = {
    0 : "l'Asthme",
    1 : "COVID_19",
    2 : "Diabète",
    3 : "la Grippe",
    4 : "l'Hypertension"
}

traitement_mapping ={
    0 : "Chirurgie",
    1 : "Médicament",
    2 : "Thérapie",
    3 : "Suivi"
}
def make_prediction(diagnosis_model, treatment_model, model_type: str, input_dict: dict):
    print("Données de prédiction ✅✅")
    input_df = pd.DataFrame([input_dict])
    
    if model_type in ["MLflow", "BentoML"]:
        try:
            # 🧠 1. Prédiction de la maladie
            disease_pred = diagnosis_model.predict(input_df)
            disease_class = int(disease_pred[0])
            disease_name = diagnosis_mapping.get(disease_class, "Maladie Inconnue")
            
            # 💊 2. Prédiction du traitement à partir du diagnostique
            treatment_pred = treatment_model.predict(input_df)
            treatment_class = int(treatment_pred[0])
            treatment_name = traitement_mapping.get(treatment_class, "Traitement Inconnu")
            return {
                "Diagnostique Trouvé" : disease_name,
                "Traitement Adéquat": treatment_name
            }
        except Exception as e:
            print(f"🎯 Erreur lors de la prédiction {e}")
            raise HTTPException(status_code=500, detail=f"Erreur pendant la prédiction : {e}")
    raise HTTPException(status_code=500, detail="Modèle non initialisé correctement")