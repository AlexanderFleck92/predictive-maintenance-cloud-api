# 1. Nutzen Sie ein offizielles Python-Image als Basis
FROM python:3.11-slim

# 2. Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# 3. Kopieren Sie die Liste der Abhängigkeiten in den Container
COPY requirements.txt .

# 4. Installieren Sie die Python-Bibliotheken
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kopieren Sie den Programmcode und Ihre Daten in den Container
COPY src/ ./src/
COPY data/ ./data/

# 6. Öffnen Sie den Port, auf dem FastAPI laufen wird
EXPOSE 8000

# 7. Befehl, um die API beim Start des Containers auszuführen
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
