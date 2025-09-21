# app/tests/test_pipeline_ray.py
import asyncio
import ray
from ray import serve

async def main():
    # Init Ray (si cluster déjà actif, il se connecte automatiquement)
    ray.init(address="auto", ignore_reinit_error=True)

    # Récupérer le handle du pipeline déployé
    handle = serve.get_deployment_handle("Pipeline", app_name="HealthcareApp")

    print("\n=== 🔥 TEST 1 : Warmup ===")
    resp = await handle.remote({"warmup": True})
    print(resp)

    print("\n=== 🧪 TEST 2 : Patient valide ===")
    patient_data = {
        "Fievre": "Présent",
        "Temperature": 37.5,
        "Pulse": 75,
        "BloodPressure": 120,
        "SpO2": 96,
        "RespiratoryRate": 18,
        "BMI": 23.5,
        "FastingGlucose": 95,
        "Cholesterol": 200,
        "StressLevel": 5
    }
    resp = await handle.remote(patient_data)
    print(resp)

    print("\n=== ❌ TEST 3 : Patient invalide (temp trop basse) ===")
    bad_data = patient_data.copy()
    bad_data["Temperature"] = 20.0  # hors limites du JSON
    resp = await handle.remote(bad_data)
    print(resp)

if __name__ == "__main__":
    asyncio.run(main())
