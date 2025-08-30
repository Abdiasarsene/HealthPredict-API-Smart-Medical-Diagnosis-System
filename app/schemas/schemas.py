from pydantic import BaseModel, Field
from enum import Enum

# ==== DEFINITION DES COLONNES CATEGORIELLES ====
class Fievre(str, Enum):
    present = "Présent"
    absent = "Absent"

# ====== SCHEMA D'ENTREE ======
class PatientsData(BaseModel):
    temperature: float = Field(..., lt=45.0, description="Température corporelle en °C, valeur maximale réaliste", alias="Temperature")
    pulse: float = Field(..., lt=250.0, description="Fréquence cardiaque, évite des valeurs extrêmes", alias="Pulse")
    blood_pressure: float = Field(..., lt=300.0, description="Pression artérielle systolique, seuil réaliste", alias="BloodPressure")
    spo2: float = Field(..., lt=101.0, description="Saturation en oxygène, maximum réaliste de 100%", alias="SpO2")
    respiratoryrate: float = Field(..., lt=60.0, description="Fréquence respiratoire, évite les valeurs anormales",alias="RespiratoryRate")
    bmi: float = Field(..., lt=100.0, description="Indice de masse corporelle, empêche des valeurs extrêmes",alias="BMI" )
    fastingglucose: float = Field(..., lt=300.0, description="Glycémie à jeun, limite supérieure réaliste", alias="FastingGlucose")
    cholesterol: float = Field(..., lt=400.0, description="Cholestérol total, seuil pour éviter les aberrations", alias="Cholesterol")
    stresslevel: float = Field(..., lt=10.0, description="Niveau de stress sur une échelle de 1 à 10", alias="StressLevel")
    fievre : Fievre = Field(..., alias="Fievre")
    

class Config:
    allow_population_by_field_name = True
    from_attributes = True