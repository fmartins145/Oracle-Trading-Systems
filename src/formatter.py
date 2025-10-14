from .templates import ORACLE_TEMPLATE

def fmt_pct(v: float, prec: int = 2):
    try:
        return f"{v:.{prec}f}"
    except Exception:
        return str(v)

def fmt_price(v: float, prec: int = 5):
    try:
        return f"{v:.{prec}f}"
    except Exception:
        return str(v)

def render_report(pair: str, utc: str, price: float, macro, tech, flow, vti, cfg):
    levels = tech.levels
    confirmations = tech.confirmations
    align_tf = "SIM" if (tech.trend_m15 == tech.trend_h1 == tech.trend_h4) else "NÃO"

    text = ORACLE_TEMPLATE.format(
        pair=pair,
        utc=utc,
        price=fmt_price(price, cfg.get("format", {}).get("price_precision", 5)),
        direction=vti.direction,
        confidence=vti.confidence_pct,
        risk=vti.risk_level,
        score=vti.score,
        validity=vti.validity_window_h,
        vti1_status="✅ VALIDADO" if vti.vti1_valid else "❌ FALHOU",
        macro_policy=macro.policy,
        macro_rates=macro.rates,
        macro_risk=macro.risk_env,
        macro_flow=macro.capital_flow,
        macro_narrative=macro.narrative,
        vti1_conclusion=("Macro alinhada ao fluxo" if vti.vti1_valid else "Macro em desacordo com fluxo"),
        vti2_status="✅ VALIDADO" if vti.vti2_valid else "❌ FALHOU",
        trend_m15=tech.trend_m15,
        trend_h1=tech.trend_h1,
        trend_h4=tech.trend_h4,
        pattern=tech.pattern,
        confirmations=", ".join(confirmations),
        inst_pos=flow.inst_pos_pct,
        inst_side=flow.inst_side,
        retail_pos=flow.retail_pos_pct,
        retail_side=flow.retail_side,
        vol_vs=fmt_pct(flow.vol_vs_avg_pct),
        cvd_sign=flow.cvd_sign,
        cvd_value=fmt_pct(flow.cvd_value, prec=0),
        vti2_conclusion=("Estrutura e fluxo convergentes" if vti.vti2_valid else "Divergência entre estrutura e fluxo"),
        vti3_status="✅ VALIDADO" if vti.vti3_valid else "❌ FALHOU",
        align_tf=align_tf,
        divergences=("Nenhuma" if align_tf == "SIM" else "Alinhamento parcial"),
        events=", ".join(macro.upcoming_events),
        impact=macro.expected_impact,
        vol=macro.expected_vol,
        vti3_conclusion=("Convergência temporal-fundamental presente" if vti.vti3_valid else "Fundamentos/tempo desalinhados"),
        R3=fmt_price(levels["R3"]), R2=fmt_price(levels["R2"]), R1=fmt_price(levels["R1"]),
        PRICE=fmt_price(levels["PRICE"]),
        S1=fmt_price(levels["S1"]), S2=fmt_price(levels["S2"]), S3=fmt_price(levels["S3"]),
        POI_LOW=fmt_price(levels["POI"][0]), POI_HIGH=fmt_price(levels["POI"][1]),
        conf1=confirmations[0], conf2=confirmations[1], conf3=confirmations[2],
        divergence=abs(flow.inst_pos_pct - flow.retail_pos_pct),
        vol_24h=fmt_price(levels["PRICE"]),  # proxy
        absorption=flow.absorption,
        acc_low=fmt_price(flow.liquidity_zones["accumulation"][0]),
        acc_high=fmt_price(flow.liquidity_zones["accumulation"][1]),
        liq_shorts=fmt_price(flow.liquidity_zones["shorts_liquidity"]),
        protect_zone=fmt_price(flow.liquidity_zones["protect"]),
        entry_low=fmt_price(levels["POI"][0]),
        entry_high=fmt_price(levels["POI"][1]),
        pos_pct=cfg.get("risk_rules", {}).get("max_position_pct", 2),
        leverage=cfg.get("risk_rules", {}).get("max_leverage", 3),
        risk_perc=cfg.get("risk_rules", {}).get("max_position_pct", 2),
        stop=fmt_price(levels["S1"]),
        t1=fmt_price(levels["R1"]), t2=fmt_price(levels["R2"]), t3=fmt_price(levels["R3"]),
        rr_t1=cfg.get("risk_rules", {}).get("rr_targets", {}).get("T1", 1.0),
        rr_t2=cfg.get("risk_rules", {}).get("rr_targets", {}).get("T2", 1.5),
        rr_t3=cfg.get("risk_rules", {}).get("rr_targets", {}).get("T3", 2.5),
        invalid_h1=fmt_price(levels["S2"]),
        position_value=fmt_price(levels["PRICE"])
    )
    return text
