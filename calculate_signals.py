import sqlite3
import pandas as pd

def calculate_signals(db_path="crypto.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS mean_reversion_signals (
            token TEXT,
            timestamp TEXT,
            price REAL,
            high_30d REAL,
            drop_from_high_pct REAL,
            signal_triggered INTEGER,
            PRIMARY KEY (token, timestamp)
        )
    ''')

    df = pd.read_sql("SELECT * FROM price_history", conn, parse_dates=["timestamp"])
    df.sort_values(by=["token", "timestamp"], inplace=True)

    signals = []

    for token in df["token"].unique():
        token_df = df[df["token"] == token].copy()
        token_df["high_30d"] = token_df["price"].rolling(window=30, min_periods=1).max()
        token_df["drop_from_high_pct"] = 100 * (token_df["high_30d"] - token_df["price"]) / token_df["high_30d"]
        token_df["signal_triggered"] = (token_df["drop_from_high_pct"] >= 10).astype(int)

        for _, row in token_df.iterrows():
            signals.append((
                token,
                row["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                row["price"],
                row["high_30d"],
                row["drop_from_high_pct"],
                row["signal_triggered"]
            ))

    c.executemany('''
        INSERT OR REPLACE INTO mean_reversion_signals
        (token, timestamp, price, high_30d, drop_from_high_pct, signal_triggered)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', signals)

    conn.commit()
    conn.close()
    print("Signals calculated and stored.")

if __name__ == "__main__":
    calculate_signals()
