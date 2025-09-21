# app/routes/test_schema.py
from app.schemas.schema import PatientsData

exemple = {
    "Fievre": "Présent",
    "Temperature": 37.5,
    "Pulse": 75.0,
    "BloodPressure": 120.0,
    "SpO2": 96.5,
    "RespiratoryRate": 18.0,
    "BMI": 23.5,
    "FastingGlucose": 95.0,
    "Cholesterol": 200.0,
    "StressLevel": 5.0
}

try:
    data = PatientsData(**exemple)
    print(f"✅ Validate :\n {data}")
except Exception as e:
    print(f"❌ Error : {str(e)}")
