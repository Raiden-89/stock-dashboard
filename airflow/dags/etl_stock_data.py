from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# 🔌 Parametri di connessione al database
POSTGRES_CONN = {
    "host": os.getenv("STOCK_DB_HOST"),
    "port": int(os.getenv("STOCK_DB_PORT", 5432)),
    "user": os.getenv("STOCK_DB_USER"),
    "password": os.getenv("STOCK_DB_PASSWORD"),
    "database": os.getenv("STOCK_DB_NAME")
}

TICKERS = ["AAPL", "MSFT", "SPY"]
TABLE_NAME = "stock_prices"
DAYS_BACK = 30

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

dag = DAG(
    dag_id="etl_stock_data",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["finance", "stock", "etl"]
)

def fetch_save_stock_data(**kwargs):
    db_url = (
        f"postgresql://{POSTGRES_CONN['user']}:{POSTGRES_CONN['password']}"
        f"@{POSTGRES_CONN['host']}:{POSTGRES_CONN['port']}/{POSTGRES_CONN['database']}"
    )
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:

            conn.execute(f"""
CREATE TABLE IF NOT EXISTS  {TABLE_NAME} (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10),
    date DATE,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    adj_close NUMERIC,
    volume BIGINT,
    UNIQUE (ticker, date)
);""")
        print("✅ Connessione al database riuscita.")
    except OperationalError as e:
        print(f"❌ Errore di connessione al DB: {e}")
        raise

    end_date = datetime.today()
    start_date = end_date - timedelta(days=DAYS_BACK)

    for ticker in TICKERS:
        print(f"⬇️ Scarico dati per {ticker}...")
        df = yf.download(
            ticker,
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d"),
            auto_adjust=False  # ✅ Mantiene tutte le colonne originali
        )

        if df.empty:
            print(f"⚠️ Nessun dato trovato per {ticker}")
            continue

        df = df.reset_index()

        # 🛡️ Fallback se 'Adj Close' è assente
        if 'Adj Close' not in df.columns and 'Close' in df.columns:
            print(f"⚠️ 'Adj Close' mancante per {ticker}, uso 'Close'")
            df['Adj Close'] = df['Close']

        required_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"❌ Colonne mancanti per {ticker}: {missing}")

        df['ticker'] = ticker
        df.rename(columns={
            'Date': 'date',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Adj Close': 'adj_close',
            'Volume': 'volume'
        }, inplace=True)

        df = df[['ticker', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']]

        # 🔧 Fix colonne con MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        print(f"📊 Primo snapshot dati {ticker}:\n{df.head()}")

        try:
            df.to_sql(TABLE_NAME, engine, if_exists='append', index=False)
            print(f"✅ Dati salvati per {ticker}")
        except Exception as e:
            print(f"❌ Errore salvataggio per {ticker}: {e}")
            raise


fetch_and_save = PythonOperator(
    task_id="fetch_and_save_stock_data",
    python_callable=fetch_save_stock_data,
    dag=dag
)
