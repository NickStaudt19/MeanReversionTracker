import sqlite3
import pandas as pd

def view_top_signals(db_path="crypto.db", limit=10):
    conn = sqlite3.connect(db_path)

    query = f"""
    SELECT token, timestamp, drop_from_high_pct
    FROM mean_reversion_signals
    WHERE signal_triggered = 1
    ORDER BY timestamp DESC
    LIMIT {limit};
    """

    df = pd.read_sql(query, conn)
    conn.close()

    print("\nRecent Mean Reversion Signals:\n")
    print(df)

if __name__ == "__main__":
    view_top_signals()
