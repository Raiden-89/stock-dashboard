#!/bin/bash
# Avvia docker-compose in ./airflow
echo "🔧 Avvio Airflow..."
cd airflow || { echo "Directory ./airflow non trovata"; exit 1; }
docker-compose up -d
# Torna indietro e avvia docker-compose in ./docker
cd ../docker || { echo "❌ Directory ./docker non trovata"; exit 1; }
echo "Avvio altri container..."
docker-compose up -d
echo "Tutto Avviato!"