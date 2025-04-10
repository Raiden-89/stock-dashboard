
# 📈 Stock Dashboard ETL with Airflow, Docker and PostgreSQL

This project implements an automated ETL pipeline that downloads historical stock data (AAPL, MSFT, SPY) using `yfinance`, processes it with Python, and stores it in a PostgreSQL database. The workflow is orchestrated using **Apache Airflow**, all running in a **Dockerized environment**.

---

## 🧱 Project Structure

```
stock-dashboard/
│
├── dags/                   # Airflow DAGs (etl_stock_data.py)
├── scripts/                # Initialization scripts (e.g. create_user.sh)
├── .env                    # Environment variables for stock database
├── requirements.txt        # Python dependencies (yfinance, pandas, sqlalchemy, etc.)
├── docker-compose.yml      # Docker Compose configuration
└── README.md               # Project documentation
```

---

## 🚀 Tech Stack

- [Apache Airflow](https://airflow.apache.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker & Docker Compose](https://www.docker.com/)
- [yfinance](https://github.com/ranaroussi/yfinance)
- Python (pandas, sqlalchemy, etc.)

---

## ⚙️ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/stock-dashboard.git
cd stock-dashboard
```

### 2. Create the `.env` file

```env
# .env
STOCK_DB_HOST=stock_pg
STOCK_DB_PORT=5432
STOCK_DB_USER=stockuser
STOCK_DB_PASSWORD=stockpass
STOCK_DB_NAME=stockdb
```

### 3. Start the system

```bash
docker-compose up -d
```

This will launch:
- A PostgreSQL instance for Airflow (`postgres_airflow`)
- A PostgreSQL instance for stock data (`stock_pg`)
- The Airflow webserver (`http://localhost:8080`)
- The Airflow scheduler

---

## 🔁 DAG Overview

The DAG `etl_stock_data`:

- Runs **daily** (`@daily`)
- Downloads stock data from the past 30 days for AAPL, MSFT, and SPY
- Validates required columns
- Appends data into the `stock_prices` table in the `stockdb` database

---

## 🔐 Airflow Access

- **URL:** [http://localhost:8080](http://localhost:8080)
- **Username:** `admin`
- **Password:** `admin` *(can be changed in `create_user.sh` script)*

---

## 🐘 Connect to PostgreSQL via DBeaver (optional)

- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `stockdb`
- **User:** `stockuser`
- **Password:** `stockpass`

Make sure the port is properly exposed in `docker-compose.yml` if needed.

---

## ☁️ Deployment on GCP (optional)

To deploy this stack on **Google Cloud Platform**, you can use:
- **Compute Engine** with Docker
- Or **Cloud Composer** (managed Airflow) + **Cloud SQL**

See the deployment section for more details (coming soon).

---

## 📝 TODO

- [ ] Add an interactive dashboard (Streamlit or Dash)
- [ ] Write unit/integration tests for data validation
- [ ] Perform technical analysis on stock data

---

## 📄 License

MIT © 2025 - [Your Name or Team]
