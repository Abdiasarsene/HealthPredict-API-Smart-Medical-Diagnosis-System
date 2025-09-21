# app/schemas/schema.py
import json
from app.config import settings
from pydantic import BaseModel, Field, root_validator

# ==== LOAD CATEGORIES + NUMERICALS CONSTRAINTS ====
with open(settings.all_cols, "r") as f:
    schema_constraints = json.load(f)

# Enter in each part of the json file
categoricals = schema_constraints.get("categoricals", {})
numericals = schema_constraints.get("numericals", {})

# ====== SCHEMA D'ENTREE ======
class PatientsData(BaseModel):
    fievre: str = Field(..., alias="Fievre")
    temperature: float = Field(..., alias="Temperature")
    pulse: float = Field(..., alias="Pulse")
    blood_pressure: float = Field(..., alias="BloodPressure")
    spo2: float = Field(..., alias="SpO2")
    respiratoryrate: float = Field(..., alias="RespiratoryRate")
    bmi: float = Field(..., alias="BMI" )
    fastingglucose: float = Field(..., alias="FastingGlucose")
    cholesterol: float = Field(..., alias="Cholesterol")
    stress_level: float = Field(..., alias="StressLevel")
    
    # Pydantic v2
    model_config ={
        "populate_by_name": True
    }

# ====== VALIDATION =======
@root_validator(pre=True)
def validate_input(cls, values):
    
    # ✅ Validation des catégorielles
    for col, allowed in categoricals.items():
        if col in values and values[col] not in allowed:
            raise ValueError(
                f"❌ Invalid value '{values[col]}' for '{col}'."
                f"Allowed examples: {allowed[:10]}..."
            )
    
    # ✅ Validation des numériques
    for col, bounds in numericals.items():
        if col in values:
            val = values[col]
            min_val, max_val = bounds["min"], bounds["max"]
            if not (min_val <= val <= max_val):
                raise ValueError(
                    f"❌ Value {val} for '{col}' is out of range."
                    f"Expected between [{min_val}, {max_val}]"
                )
    
    return values