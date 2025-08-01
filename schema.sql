CREATE TABLE IF NOT EXISTS coins (
    id INTEGER PRIMARY KEY,
    symbol TEXT UNIQUE,
    name TEXT
);

CREATE TABLE IF NOT EXISTS ohlcv (
    id INTEGER PRIMARY KEY,
    coin_symbol TEXT,
    date DATE,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL
);

CREATE TABLE IF NOT EXISTS mean_reversion_signals (
    id INTEGER PRIMARY KEY,
    coin_symbol TEXT,
    date DATE,
    drop_from_high_pct REAL,
    volume_spike BOOLEAN,
    price_rebound BOOLEAN,
    signal_triggered BOOLEAN
);
