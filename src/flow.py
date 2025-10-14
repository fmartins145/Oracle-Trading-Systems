from dataclasses import dataclass
import pandas as pd
from .data_sources import estimate_delta, volume_vs_avg

@dataclass
class FlowSnapshot:
    inst_pos_pct: int
    inst_side: str
    retail_pos_pct: int
    retail_side: str
    vol_vs_avg_pct: float
    cvd_sign: str
    cvd_value: float
    liquidity_zones: dict
    absorption: str

def flow_snapshot(df_m15: pd.DataFrame) -> FlowSnapshot:
    # Heurísticas baseadas em delta e variação para simular posicionamentos
    delta = estimate_delta(df_m15)
    cvd_sign = "Positivo" if delta > 0 else ("Negativo" if delta < 0 else "Neutro")
    vol_vs = volume_vs_avg(df_m15)
    # Institutional vs retail proxy (simples): se delta positivo e tendência alta -> inst long
    inst_bias_long = (cvd_sign == "Positivo")
    inst_pos_pct = 65 if inst_bias_long else 35
    retail_pos_pct = 100 - inst_pos_pct
    inst_side = "Long" if inst_bias_long else "Short"
    retail_side = "Short" if inst_bias_long else "Long"
    # Liquidity zones: última faixa de consolidação
    recent = df_m15.tail(40)
    acc_low, acc_high = recent["Low"].min(), recent["High"].max()
    liq_shorts = acc_high * 1.002
    protect_zone = acc_low * 0.998
    absorption = "Compras absorvendo acima do pivô" if inst_bias_long else "Vendas absorvendo abaixo do pivô"

    return FlowSnapshot(inst_pos_pct, inst_side, retail_pos_pct, retail_side, vol_vs, cvd_sign, float(delta),
                        {"accumulation": (acc_low, acc_high), "shorts_liquidity": liq_shorts, "protect": protect_zone},
                        absorption)
