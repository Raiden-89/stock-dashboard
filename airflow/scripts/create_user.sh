#!/bin/bash
# Aspetto che il DB sia pronto
airflow db upgrade
# Crea l'utente leggendo le variabili dall'ambiente
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin