import requests
import sqlite3
import time
from datetime import datetime, timedelta

conn = sqlite3.connect("crypto.db")
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS price_history (
        token TEXT,
        timestamp TEXT,
        price REAL,
        PRIMARY KEY (token, timestamp)
    )
''')

# Add more tokens if needed
tokens = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'SOL': 'solana',
    'AVAX': 'avalanche-2',
    'XRP': 'ripple'
}

to_timestamp = int(time.time())
from_timestamp = to_timestamp - 60 * 60 * 24 * 90  # Last 90 days

for symbol, coingecko_id in tokens.items():
    print(f"Fetching data for {symbol}...")
    url = f"https://api.coingecko.com/api/v3/coins/{coingecko_id}/market_chart/range"
    params = {
        'vs_currency': 'usd',
        'from': from_timestamp,
        'to': to_timestamp
    }
    try:
        r = requests.get(url, params=params)
        data = r.json()
        if "prices" not in data:
            print(f"Error: Response for {symbol} missing 'prices': {data}")
            continue
        prices = []
        for timestamp_ms, price in data["prices"]:
            ts = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
            prices.append((symbol, ts, price))
        c.executemany("INSERT OR REPLACE INTO price_history (token, timestamp, price) VALUES (?, ?, ?)", prices)
        conn.commit()
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

conn.close()
print("Finished updating price history.")
