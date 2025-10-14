from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime, timedelta

@dataclass
class MacroSnapshot:
    policy: str
    rates: str
    risk_env: str
    capital_flow: str
    narrative: str
    upcoming_events: List[str]
    expected_impact: str
    expected_vol: str

def get_macro_snapshot(now_utc: str) -> MacroSnapshot:
    # Lightweight macro model (extend later with real calendar fetching).
    now = datetime.strptime(now_utc, "%Y-%m-%d %H:%M")
    events = []

    # Static rolling events (placeholders for 24–48h). You can expand with real API parsing later.
    # Example schedule logic:
    for label, day_mod in [("US CPI", 1), ("FOMC Minutes", 2), ("ECB Rate Decision", 2), ("NFP", 3)]:
        event_time = now + timedelta(days=day_mod)
        events.append(f"{label} ~ {event_time.strftime('%Y-%m-%d')}")

    # Heuristics
    risk_env = "Risk-On"  # simplify; can be refined with VIX/DXY later
    capital_flow = "Rotação para USD e ativos de risco moderada"
    narrative = "Mercado atento a inflação e trajetória de juros; apetite seletivo por risco"
    expected_impact = "Neutro"
    expected_vol = "Média"

    return MacroSnapshot(
        policy="Políticas mistas entre FED/ECB; postura data-dependent",
        rates="Estáveis a levemente restritivas",
        risk_env=risk_env,
        capital_flow=capital_flow,
        narrative=narrative,
        upcoming_events=events,
        expected_impact=expected_impact,
        expected_vol=expected_vol
    )
