# KI-gestützte Predictive Maintenance API

Eine cloud-bereite Python-API zur **KI-gestützten Vorhersage von Maschinenausfällen** auf Basis von Sensordaten.

Das Projekt simuliert einen Anwendungsfall aus dem Bereich **Industrie 4.0 / Predictive Maintenance**: Sensordaten einer Maschine werden an eine REST-API übertragen, durch ein trainiertes Machine-Learning-Modell analysiert und anschließend hinsichtlich eines möglichen Maschinenausfalls bewertet.

Ziel des Projekts ist es, die einzelnen Bausteine von **Datenaufbereitung über Machine Learning bis hin zur containerisierten Bereitstellung einer API** in einer zusammenhängenden Anwendung abzubilden.

---

## 🎯 Projektziel

Ungeplante Maschinenausfälle können in industriellen Produktionsumgebungen zu Produktionsstillständen und hohen Kosten führen.

Predictive Maintenance verfolgt deshalb den Ansatz, mögliche Ausfälle **frühzeitig anhand von Sensordaten zu erkennen**.

In diesem Projekt werden beispielsweise:

* Temperaturdaten
* Drehzahlen
* weitere Maschinenkennzahlen

verarbeitet und für eine KI-basierte Vorhersage verwendet.

Der grundlegende Ablauf sieht dabei so aus:

```text
Sensordaten
     │
     ▼
FastAPI
     │
     ▼
Datenvalidierung
     │
     ▼
Machine-Learning-Modell
     │
     ▼
Ausfallprognose
     │
     ▼
JSON-Antwort
```

Die Anwendung ist dabei so aufgebaut, dass das trainierte Modell anschließend innerhalb eines **Docker-Containers** zusammen mit der API bereitgestellt werden kann.

---

## 🏗️ Architektur

Das Projekt besteht aus drei wesentlichen Bereichen:

### 1. Datenaufbereitung & Machine Learning

Zunächst werden historische Sensordaten aus einem Kaggle-Datensatz verarbeitet und für das Training des Machine-Learning-Modells vorbereitet.

Dabei werden unter anderem:

* Daten geladen und bereinigt
* relevante Merkmale ausgewählt
* zusätzliche Features erstellt
* Trainings- und Testdaten aufgeteilt
* ein Machine-Learning-Modell trainiert
* die Modellleistung ausgewertet

Als Machine-Learning-Modell kommt ein **Random Forest Classifier** zum Einsatz.

Das trainierte Modell wird anschließend mit **Joblib** serialisiert und als `.pkl`-Datei gespeichert.

---

### 2. REST-API

Das trainierte Modell wird anschließend über eine Python-API bereitgestellt.

Dafür wird **FastAPI** verwendet.

Die API stellt einen `/predict`-Endpunkt bereit, an den Maschinenkennzahlen übertragen werden können.

Beispiel:

```http
POST /predict
```

Eine Anfrage kann beispielsweise Maschinenwerte enthalten:

```json
{
  "temperature": 80.5,
  "rotational_speed": 1450
}
```

Die API validiert die eingehenden Daten und übergibt sie anschließend an das Machine-Learning-Modell.

Das Ergebnis wird als JSON zurückgegeben.

---

## 🧠 Datenvalidierung

Für die Validierung der eingehenden Sensordaten wird **Pydantic** verwendet.

Das Datenmodell `MachineMetrics` definiert dabei, welche Daten die API erwartet.

Dadurch können beispielsweise:

* fehlende Werte
* falsche Datentypen
* ungültige Eingaben

bereits beim Eingang der Anfrage erkannt werden.

Die API liefert in solchen Fällen eine entsprechende Fehlermeldung zurück, anstatt fehlerhafte Daten an das Machine-Learning-Modell weiterzugeben.

---

## 🐳 Containerisierung

Die Anwendung wird mit **Docker** containerisiert.

Das Docker-Image enthält:

* die Python-Anwendung
* das trainierte Machine-Learning-Modell
* die benötigten Python-Abhängigkeiten
* die FastAPI-Anwendung

Dadurch kann die Anwendung unabhängig von der lokalen Python-Umgebung ausgeführt werden.

Der Aufbau ermöglicht beispielsweise eine spätere Bereitstellung auf einer Cloud-Plattform.

```text
Docker Container
├── FastAPI
├── Machine-Learning-Modell
├── Python-Code
└── Dependencies
```

---

## 🧪 Testing

Für automatisierte Tests wird **Pytest** verwendet.

Dabei wird unter anderem überprüft, ob die API auf gültige Anfragen korrekt reagiert und die erwartete JSON-Struktur zurückliefert.

Für die Simulation von HTTP-Anfragen innerhalb der Testumgebung wird **HTTPX bzw. FastAPI TestClient** eingesetzt.

Dadurch können die API-Endpunkte getestet werden, ohne dass die Anwendung tatsächlich öffentlich im Internet erreichbar sein muss.

---

## 🛠️ Technologien

| Technologie            | Verwendung                                |
| ---------------------- | ----------------------------------------- |
| **Python**             | Programmiersprache                        |
| **Pandas**             | Datenaufbereitung und Feature Engineering |
| **NumPy**              | Numerische Berechnungen                   |
| **Scikit-Learn**       | Machine Learning                          |
| **Joblib**             | Speicherung des trainierten Modells       |
| **FastAPI**            | REST-API                                  |
| **Pydantic**           | Datenvalidierung                          |
| **Uvicorn**            | ASGI-Webserver                            |
| **Pytest**             | Automatisierte Tests                      |
| **HTTPX / TestClient** | API-Tests                                 |
| **Docker**             | Containerisierung                         |

---

## 📁 Projektstruktur

```text
predictive-maintenance-api/
│
├── app/
│   ├── main.py
│   ├── model.py
│   └── schemas.py
│
├── model/
│   └── predictive_maintenance_model.pkl
│
├── data/
│   └── dataset.csv
│
├── tests/
│   └── test_api.py
│
├── train.py
├── requirements.txt
├── Dockerfile
└── README.md
```

Die konkrete Struktur kann je nach Umsetzung des Projekts angepasst werden.

---

## 🚀 Installation

Repository klonen:

```bash
git clone <repository-url>
cd predictive-maintenance-api
```

Virtuelle Umgebung erstellen:

```bash
python -m venv venv
```

Virtuelle Umgebung aktivieren:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

---

## ▶️ API starten

Die API kann mit Uvicorn gestartet werden:

```bash
uvicorn app.main:app --reload
```

Anschließend ist die API lokal erreichbar.

FastAPI stellt außerdem automatisch eine interaktive API-Dokumentation bereit.

---

## 🐳 Start mit Docker

Docker-Image erstellen:

```bash
docker build -t predictive-maintenance-api .
```

Container starten:

```bash
docker run -p 8000:8000 predictive-maintenance-api
```

Die Anwendung läuft anschließend innerhalb des Containers und kann über den veröffentlichten Port angesprochen werden.

---

## 🧪 Tests ausführen

Die automatisierten Tests können mit folgendem Befehl ausgeführt werden:

```bash
pytest
```

---

## ☁️ Cloud-Perspektive

Das Projekt ist bewusst so aufgebaut, dass die Anwendung **containerisiert und damit grundsätzlich cloud-bereit** ist.

Der Docker-Container könnte beispielsweise auf einer Cloud-Infrastruktur betrieben werden.

Eine mögliche Weiterentwicklung wäre eine Architektur mit:

```text
IoT-Sensoren
     │
     ▼
Message Broker
     │
     ▼
Cloud-Infrastruktur
     │
     ▼
Predictive Maintenance API
     │
     ▼
Machine-Learning-Modell
     │
     ▼
Ausfallprognose
```

Mögliche nächste Schritte wären unter anderem:

* Bereitstellung in einer Public Cloud
* Kubernetes-basierter Betrieb
* automatisierte CI/CD-Pipeline
* Monitoring und Logging
* Anbindung eines Message Brokers
* Speicherung historischer Sensordaten
* regelmäßiges Retraining des Machine-Learning-Modells

Diese Punkte sind **mögliche Erweiterungen des Projekts** und nicht Bestandteil der aktuellen Implementierung.

---

## 🎓 Ziel des Projekts

Mit diesem Projekt soll eine durchgängige Verbindung zwischen **Machine Learning, Python-Entwicklung und Cloud-/DevOps-Konzepten** geschaffen werden.

Dabei steht nicht nur das Trainieren eines Machine-Learning-Modells im Vordergrund, sondern insbesondere dessen **Bereitstellung als reproduzierbare, getestete und containerisierte Anwendung**.

Das Projekt dient damit als praktische Auseinandersetzung mit typischen Aufgabenstellungen an der Schnittstelle von **Cloud Engineering, DevOps und Künstlicher Intelligenz**.
