# Stock Dashboard with Apache Airflow

This project implements a stock data ETL pipeline using **Apache Airflow** and **Yahoo Finance** data. It allows scheduled extraction and storage of historical stock prices for selected tickers into a PostgreSQL database.

## 🚀 Features

- Download daily stock data using `yfinance`
- Store it in a PostgreSQL database via SQLAlchemy
- Scheduled execution using Airflow DAGs
- Docker-based local development setup

## 🗂 Project Structure

```
stock-dashboard/
│
├── .venv/                     # Python virtual environment (excluded from version control)
│
├── airflow/
│   ├── dags/                  # Airflow DAGs
│   │   ├── __init__.py
│   │   ├── dag_prova.py
│   │   └── etl_stock_data.py
│   │
│   ├── scripts/               # Utility scripts for Airflow (e.g., user creation)
│   │   └── create_user.sh
│   │
│   ├── .env                   # Environment variables used by docker-compose and DAGs
│   ├── docker-compose.yml     # Docker environment configuration
│   └── requirements.txt       # Python dependencies
│
└── README.md                  # Project documentation
```

## 🧰 Requirements

- Docker
- Docker Compose

## ▶️ How to Run

```bash
cd airflow/
docker-compose up --build
```

Then access the Airflow UI at [http://localhost:8080](http://localhost:8080)

## 📊 Environment Variables

Defined in `.env` (sample values):

```
STOCK_DB_HOST=stock_pg
STOCK_DB_PORT=5432
STOCK_DB_USER=stockuser
STOCK_DB_PASSWORD=stockpass
STOCK_DB_NAME=stockdb
```

## 📅 Airflow DAGs

Main DAG: `etl_stock_data.py`  
Runs daily and processes data for these tickers:

```python
["AAPL", "MSFT", "SPY"]
```

## 📎 License

MIT License
