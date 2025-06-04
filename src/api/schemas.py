from pydantic import BaseModel, Field
from enum import Enum

# ==== DEFINITION DES COLONNES CATEGORIELLES ====
class PresenceStatus(str, Enum):
    present = "Présent"
    absent = "Absent"

# ====== SCHEMA D'ENTREE ======
class PatientsData(BaseModel):
    Temperature: float = Field(..., lt=45.0, description="Température corporelle en °C, valeur maximale réaliste")
    Pulse: float = Field(..., lt=250.0, description="Fréquence cardiaque, évite des valeurs extrêmes")
    BloodPressure: float = Field(..., lt=300.0, description="Pression artérielle systolique, seuil réaliste")
    SpO2: float = Field(..., lt=101.0, description="Saturation en oxygène, maximum réaliste de 100%")
    RespiratoryRate: float = Field(..., lt=60.0, description="Fréquence respiratoire, évite les valeurs anormales")
    BMI: float = Field(..., lt=100.0, description="Indice de masse corporelle, empêche des valeurs extrêmes")
    FastingGlucose: float = Field(..., lt=300.0, description="Glycémie à jeun, limite supérieure réaliste")
    Cholesterol: float = Field(..., lt=400.0, description="Cholestérol total, seuil pour éviter les aberrations")
    StressLevel: float = Field(..., lt=10.0, description="Niveau de stress sur une échelle de 1 à 10")
    Fatigue_intense : PresenceStatus
    Frissons: PresenceStatus
    Perte_gout_odorat : PresenceStatus
    Toux_seche : PresenceStatus

class Config:
    allow_population_by_field_name = True


# Exemple de schéma : 

# {
#     "Temperature": 37.2,
#     "Pulse": 75.0,
#     "BloodPressure": 120.0,
#     "SpO2": 98.0,
#     "RespiratoryRate": 16.0,
#     "BMI": 23.5,
#     "FastingGlucose": 90.0,
#     "Cholesterol": 180.0,
#     "StressLevel": 4.0,
#     "Fatigue_intense": "Absent",
#     "Frissons": "Absent",
#     "Perte_gout_odorat": "Absent",
#     "Toux_seche": "Absent"
# }

# {
#     "Temperature": 38.5,
#     "Pulse": 95.0,
#     "BloodPressure": 130.0,
#     "SpO2": 93.0,
#     "RespiratoryRate": 22.0,
#     "BMI": 26.5,
#     "FastingGlucose": 110.0,
#     "Cholesterol": 210.0,
#     "StressLevel": 7.0,
#     "Fatigue_intense": "Présent",
#     "Frissons": "Présent",
#     "Perte_gout_odorat": "Présent",
#     "Toux_seche": "Présent"
# }

# {
#     "Temperature": 36.8,
#     "Pulse": 85.0,
#     "BloodPressure": 160.0,
#     "SpO2": 97.0,
#     "RespiratoryRate": 18.0,
#     "BMI": 29.0,
#     "FastingGlucose": 210.0,
#     "Cholesterol": 350.0,
#     "StressLevel": 8.0,
#     "Fatigue_intense": "Présent",
#     "Frissons": "Absent",
#     "Perte_gout_odorat": "Absent",
#     "Toux_seche": "Absent"
# }