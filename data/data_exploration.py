import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Parametri
TICKERS = ["AAPL", "MSFT", "SPY"]
DAYS_BACK = 30

# Intervallo temporale
end_date = datetime.today()
start_date = end_date - timedelta(days=DAYS_BACK)

# Scarico e analizzo dati
for ticker in TICKERS:
    print(f"\n=== Analisi dati per {ticker} ===")
    df = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"), auto_adjust=False)

    if df.empty:
        print(f"Nessun dato disponibile per {ticker}")
        continue

    df.reset_index(inplace=True)

    # Gestione MultiIndex (appiattimento colonne)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] if col[1] == '' else col[0] for col in df.columns.values]

    print("Colonne disponibili dopo correzione:", df.columns)

    if 'Close' not in df.columns or 'Volume' not in df.columns:
        raise KeyError(f"Colonne 'Close' o 'Volume' non trovate in {df.columns}")

    df['Date'] = pd.to_datetime(df['Date'])
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    print(df.head())
    print(df.describe())

    # Controllo dati mancanti
    missing = df.isnull().sum()
    print(f"\nDati mancanti per {ticker}:")
    print(missing[missing > 0])

    # Plot andamento prezzo di chiusura
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Close'], marker='o')
    plt.title(f'{ticker} - Prezzo di chiusura ultimi {DAYS_BACK} giorni')
    plt.xlabel('Data')
    plt.ylabel('Prezzo di Chiusura ($)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plot volume
    plt.figure(figsize=(10, 5))
    plt.bar(df['Date'], df['Volume'])
    plt.title(f'{ticker} - Volume ultimi {DAYS_BACK} giorni')
    plt.xlabel('Data')
    plt.ylabel('Volume')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()