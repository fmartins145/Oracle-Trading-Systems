import pandas as pd
import yfinance as yf
import requests
import time
from typing import Dict, Optional

ALPHA_FX_BASE = "https://www.alphavantage.co/query"

def fetch_yf_history(ticker: str, interval: str = "15m", lookback_days: int = 5) -> Optional[pd.DataFrame]:
    try:
        df = yf.download(tickers=ticker, interval=interval, period=f"{lookback_days}d", auto_adjust=True, progress=False)
        if isinstance(df, pd.DataFrame) and not df.empty:
            df = df.reset_index().rename(columns={"Datetime":"Date"})
            return df
        return None
    except Exception:
        return None

def fetch_alpha_fx(pair: str, api_key: str, interval: str = "15min") -> Optional[pd.DataFrame]:
    from_symbol, to_symbol = pair[:3], pair[3:]
    params = {
        "function": "FX_INTRADAY",
        "from_symbol": from_symbol,
        "to_symbol": to_symbol,
        "interval": interval,
        "outputsize": "compact",
        "apikey": api_key
    }
    try:
        r = requests.get(ALPHA_FX_BASE, params=params, timeout=15)
        if r.status_code == 200:
            j = r.json()
            key = f"Time Series FX ({interval})"
            ts = j.get(key, {})
            if not ts:
                return None
            rows = []
            for k, v in ts.items():
                rows.append({"Date": pd.to_datetime(k), "Open": float(v["1. open"]), "High": float(v["2. high"]),
                             "Low": float(v["3. low"]), "Close": float(v["4. close"]), "Volume": None})
            df = pd.DataFrame(rows).sort_values("Date")
            return df
        return None
    except Exception:
        return None

def last_price(df: pd.DataFrame) -> Optional[float]:
    try:
        return float(df["Close"].iloc[-1])
    except Exception:
        return None

def estimate_delta(df: pd.DataFrame) -> float:
    # Simple proxy for CVD using signed volume approximations (Yahoo lacks true order-flow).
    if "Volume" in df.columns and df["Volume"].notna().sum() > 0:
        changes = df["Close"].diff().fillna(0)
        vol = df["Volume"].fillna(0)
        delta = (changes.apply(lambda x: 1 if x>0 else (-1 if x<0 else 0)) * vol).sum()
        return float(delta)
    # If volume absent, use price change count as proxy
    changes = df["Close"].diff().fillna(0)
    delta = changes.apply(lambda x: 1 if x>0 else (-1 if x<0 else 0)).sum()
    return float(delta)

def volume_vs_avg(df: pd.DataFrame, window: int = 48) -> float:
    if "Volume" in df.columns and df["Volume"].notna().sum() > 0:
        recent = df["Volume"].iloc[-1]
        avg = df["Volume"].tail(window).mean()
        if avg and avg > 0:
            return ((recent - avg) / avg) * 100.0
    return 0.0
