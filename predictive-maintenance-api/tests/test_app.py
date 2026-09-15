# tests/test_app.py
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_predict_endpoint_success():
    # Simuliert einen normalen payload der Maschinen
    payload = {
        "air_temp": 300.0,
        "process_temp": 310.0,
        "rotational_speed": 1500.0,
        "torque": 40.0
    }
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 200
    json_data = response.json()
    assert "status" in json_data
