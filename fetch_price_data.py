import sqlite3
import requests
from datetime import datetime

# Fetch historical price data from CoinGecko (30 days)
def fetch_price_data(coin_id="bitcoin"):
    url = "https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=30"
    response = requests.get(url)
    return response.json()

# Insert data into SQLite
def store_price_data(data, coin_id="bitcoin"):
    conn = sqlite3.connect("crypto.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_history (
        timestamp TEXT,
        token TEXT,
        price REAL
    )
    """)

    # Insert data into the table
    for i in range(len(data['prices'])):
        from datetime import timezone
        timestamp = datetime.fromtimestamp(data['prices'][i][0] / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        price = data['prices'][i][1]
        cursor.execute("""
            INSERT INTO price_history (timestamp, token, price)
            VALUES (?, ?, ?)
        """, (timestamp, coin_id, price))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    data = fetch_price_data("bitcoin")  # Replace with any coin ID like "ethereum"
    store_price_data(data, "bitcoin")
    print("Data fetched and stored successfully.")
