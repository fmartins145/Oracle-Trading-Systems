import datetime as dt
import os

def now_utc_iso():
    return dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M")

def get_env(name: str, default: str = ""):
    return os.environ.get(name, default)

def safe_float(v, default=None):
    try:
        return float(v)
    except Exception:
        return default

def clamp(v, lo, hi):
    return max(lo, min(hi, v))
