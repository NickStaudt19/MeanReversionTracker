import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to your database
conn = sqlite3.connect("crypto.db")

# Get list of available tokens
tokens_df = pd.read_sql_query("SELECT DISTINCT token FROM price_history", conn)
tokens = tokens_df['token'].tolist()

print("\nAvailable tokens:")
for i, token in enumerate(tokens):
    print(f"{i + 1}. {token}")

choice = input("\nEnter the token abbreviation you want to plot (e.g., BTC, ETH): ").strip().upper()
if choice not in tokens:
    print(f"Token '{choice}' not found in database.")
    conn.close()
    exit()

# Read price history and signals into DataFrames
prices = pd.read_sql_query(f"""
    SELECT timestamp, token, price
    FROM price_history
    WHERE token = '{choice}'
    ORDER BY timestamp
""", conn)

signals = pd.read_sql_query(f"""
    SELECT timestamp, token
    FROM mean_reversion_signals
    WHERE token = '{choice}' AND signal_triggered = 1
    ORDER BY timestamp
""", conn)

conn.close()

# Convert timestamps
prices['timestamp'] = pd.to_datetime(prices['timestamp'])
signals['timestamp'] = pd.to_datetime(signals['timestamp'])

# Plot
plt.figure(figsize=(12, 6))
plt.plot(prices['timestamp'], prices['price'], label=f'{choice} Price', color='blue')

# Add signal markers
plt.scatter(signals['timestamp'], 
            prices.set_index('timestamp').loc[signals['timestamp']]['price'],
            color='red', label='Signal Triggered', zorder=5)

plt.title(f"{choice} Price & Mean Reversion Signals")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
