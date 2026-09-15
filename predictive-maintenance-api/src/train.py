# src/train.py
import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """Lädt die Kaggle-Daten und führt Feature Engineering mit Pandas durch."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")
        
    df = pd.read_csv(file_path)
    
    # Feature Engineering: Temperaturdifferenz berechnen
    df['temp_diff'] = df['Process temperature [K]'] - df['Air temperature [K]']
    
    return df

def train_model():
    print("Lade Daten und starte Vorbereitung")
    df = load_and_clean_data("data/predictive_maintenance.csv")
    
    # Features und Zielvariable definieren
    feature_cols = ['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'temp_diff']
    X = df[feature_cols]
    y = df['Target']  # 1 = Ausfall, 0 = Normalbetrieb
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Trainiere Random Forest Modell")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Validierung 
    predictions = model.predict(X_test)
    print("\n--- Modell Performance ---")
    print(classification_report(y_test, predictions))
    
    # Modell für die Cloud-API speichern
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/rf_maintenance_model.pkl")
    print("Modell erfolgreich unter 'models/rf_maintenance_model.pkl' gespeichert!")

if __name__ == "__main__":
    train_model()
