import pytest
from httpx import AsyncClient
from unittest.mock import patch
from main import app 
from src.api.schemas import PresenceStatus


@pytest.mark.asyncio
@patch("src.api.routes.make_prediction")
async def test_predict_disease_success(mock_make_prediction):
    # On simule une réponse du modèle
    mock_make_prediction.return_value = ("Le patient souffre de l'Asthme", 0)

    payload = {
        "Temperature": 37.0,
        "Pulse": 85,
        "BloodPressure": 120,
        "SpO2": 98,
        "RespiratoryRate": 18,
        "BMI": 23.5,
        "FastingGlucose": 95,
        "Cholesterol": 180,
        "StressLevel": 4,
        "Fatigue_intense": PresenceStatus.present.value,
        "Frissons": PresenceStatus.absent.value,
        "Perte_gout_odorat": PresenceStatus.absent.value,
        "Toux_seche": PresenceStatus.present.value
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/disease", json=payload)

    assert response.status_code == 200
    response_data = response.json()

    assert "Diagnostique" in response_data
    assert "Code" in response_data
    assert "Statut" in response_data
    assert response_data["Statut"] == "Success"
    assert isinstance(response_data["Code"], int)
    assert response_data["Diagnostique"].startswith("Le patient souffre de")


@pytest.mark.asyncio
async def test_predict_disease_invalid_input():
    invalid_payload = {
        "Temperature": 37.0,
        "Pulse": 85,
        "BloodPressure": 120,
        "SpO2": 98,
        "RespiratoryRate": 18,
        "BMI": 23.5,
        "FastingGlucose": 95,
        "Cholesterol": 999,  # invalide (>400)
        "StressLevel": 4,
        "Fatigue_intense": PresenceStatus.present.value,
        "Frissons": PresenceStatus.absent.value,
        "Perte_gout_odorat": PresenceStatus.absent.value,
        "Toux_seche": PresenceStatus.present.value
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/disease", json=invalid_payload)

    assert response.status_code == 422
    error = response.json()
    assert "detail" in error
