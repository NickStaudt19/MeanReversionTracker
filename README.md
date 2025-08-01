# Crypto Mean Reversion Alert System

A Python-based trading signal tracker that detects mean reversion opportunities in crypto assets like BTC and ETH using historical price data. Sends real-time email alerts and runs hourly via cron.

## Features
- Calculates signals based on % drop from 30-day high and price rebound
- Stores and queries price data using SQLite
- Sends real-time alerts via email using Gmail SMTP
- Hourly automation using cron
- Plots historical signals with Matplotlib

## Tech Stack
Python, SQL (SQLite), Pandas, Matplotlib, Cron

## Setup
1. Clone the repo
2. Set environment variables:
   ```bash
   export ALERT_EMAIL="your.email@gmail.com"
   export ALERT_PASS="your_app_password"
   export ALERT_TO="your.destination@email.com"
