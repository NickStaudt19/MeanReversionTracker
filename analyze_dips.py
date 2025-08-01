import sqlite3
import pandas as pd
from datetime import date
import smtplib
from email.mime.text import MIMEText
import os

def send_email(subject, body):
    from_email = os.getenv("ALERT_EMAIL")
    to_email = os.getenv("ALERT_TO") or from_email
    app_password = os.getenv("ALERT_PASS")

    if not from_email or not app_password:
        print("❌ ALERT_EMAIL or ALERT_PASS environment variable is not set.")
        return

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, app_password)
            server.send_message(msg)
        print(f"📧 Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def analyze_mean_reversion(conn):
    cursor = conn.cursor()

    coins = [row[0] for row in cursor.execute("SELECT DISTINCT token FROM price_history")]
    today = date.today().isoformat()

    for coin in coins:
        df = pd.read_sql("""
            SELECT timestamp as date, price
            FROM price_history
            WHERE token = ?
            ORDER BY timestamp
        """, conn, params=(coin,))

        if len(df) < 10:
            continue

        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)

        current_price = df.iloc[-1]['price']
        high_30d = df['price'].rolling(window=30, min_periods=1).max().iloc[-1]
        drop_pct = (high_30d - current_price) / high_30d * 100

        price_rebound = df.iloc[-1]['price'] > df.iloc[-2]['price']
        volume_spike = False  # No volume data for now

        signal = drop_pct >= 10 and price_rebound

        # Insert into signals table
        cursor.execute("""
            INSERT OR REPLACE INTO mean_reversion_signals
            (token, timestamp, price, high_30d, drop_from_high_pct, signal_triggered)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            coin,
            df.iloc[-1]['date'].strftime('%Y-%m-%d %H:%M:%S'),
            current_price,
            high_30d,
            drop_pct,
            int(signal)
        ))

        message = f"{coin} | Drop: {drop_pct:.2f}% | Signal: {'✅' if signal else '—'}"
        print(message)

        if signal:
            email_subject = f"📉 Mean Reversion Signal: {coin}"
            email_body = (
                f"Token: {coin}\n"
                f"Date: {df.iloc[-1]['date'].strftime('%Y-%m-%d')}\n"
                f"Drop from 30d High: {drop_pct:.2f}%\n"
                f"Price: ${current_price:.2f}\n"
                f"Rebound: {'Yes' if price_rebound else 'No'}"
            )
            send_email(email_subject, email_body)

    conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect("crypto.db")
    analyze_mean_reversion(conn)
    conn.close()
