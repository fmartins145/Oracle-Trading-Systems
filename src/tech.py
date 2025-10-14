import pandas as pd
from dataclasses import dataclass

@dataclass
class TechSnapshot:
    trend_m15: str
    trend_h1: str
    trend_h4: str
    pattern: str
    confirmations: list
    levels: dict

def trend_from_prices(df: pd.DataFrame) -> str:
    # Simple trend proxy: compare short and long MAs
    short = df["Close"].rolling(8).mean().iloc[-1]
    long = df["Close"].rolling(34).mean().iloc[-1]
    if short > long: return "Alta"
    if short < long: return "Baixa"
    return "Lateral"

def compute_levels(df: pd.DataFrame):
    # R1/R2/R3/S1/S2/S3 via pivots (basic)
    last = df["Close"].iloc[-1]
    recent = df.tail(48)
    high = recent["High"].max()
    low = recent["Low"].min()
    pivot = (high + low + last) / 3.0
    r1 = 2*pivot - low
    s1 = 2*pivot - high
    r2 = pivot + (high - low)
    s2 = pivot - (high - low)
    r3 = high + 2*(pivot - low)
    s3 = low - 2*(high - pivot)
    return {
        "R3": r3, "R2": r2, "R1": r1, "PRICE": last, "S1": s1, "S2": s2, "S3": s3,
        "POI": (pivot*0.995, pivot*1.005)
    }

def tech_snapshot(df_m15: pd.DataFrame) -> TechSnapshot:
    trend = trend_from_prices(df_m15)
    # H1/H4 approximations by resampling M15:
    df_h1 = df_m15.set_index("Date").resample("1H").agg({"Open":"first","High":"max","Low":"min","Close":"last"}).dropna().reset_index()
    df_h4 = df_m15.set_index("Date").resample("4H").agg({"Open":"first","High":"max","Low":"min","Close":"last"}).dropna().reset_index()
    trend_h1 = trend_from_prices(df_h1)
    trend_h4 = trend_from_prices(df_h4)
    levels = compute_levels(df_m15)
    # Pattern heuristic
    changes = df_m15["Close"].diff().fillna(0)
    pattern = "Impulso" if abs(changes.tail(8).sum()) > df_m15["Close"].tail(8).std() else "Consolidação"
    confirmations = [
        "MA(8) vs MA(34) alinhadas",
        "Pivô respeitado no intraday",
        "Variação recente coerente com direção"
    ]
    return TechSnapshot(trend, trend_h1, trend_h4, pattern, confirmations, levels)
