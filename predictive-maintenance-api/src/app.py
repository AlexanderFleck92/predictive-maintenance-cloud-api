# src/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os

app = FastAPI(title="KI Predictive Maintenance API", version="1.0")

MODEL_PATH = "models/rf_maintenance_model.pkl"

# 
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None
    print("ℹAPI läuft im Entwicklungsmodus")

# Datenstruktur für die Cloud-Anfrage (API-Payload)
class MachineMetrics(BaseModel):
    air_temp: float
    process_temp: float
    rotational_speed: float
    torque: float

@app.post("/predict")
def predict_maintenance(data: MachineMetrics):
    if model is None:
        return {
            "status": "API im Entwicklungsmodus",
            "message": "Modell-Inferenz wird nach Abschluss des Pipeline-Deployments aktiviert."
        }
    
    try:
        # Feature Engineering & Vorhersage
        input_data = {
            'Air temperature [K]': [data.air_temp],
            'Process temperature [K]': [data.process_temp],
            'Rotational speed [rpm]': [data.rotational_speed],
            'Torque [Nm]': [data.torque],
            'temp_diff': [data.process_temp - data.air_temp]
        }
        df_input = pd.DataFrame(input_data)
        prediction = model.predict(df_input)
        
        return {
            "machine_failure_predicted": bool(prediction),
            "status": "Wartung erforderlich!" if prediction == 1 else "Betrieb normal"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
