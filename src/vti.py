from dataclasses import dataclass
from .macro import MacroSnapshot
from .tech import TechSnapshot
from .flow import FlowSnapshot

@dataclass
class VTIResult:
    vti1_valid: bool
    vti2_valid: bool
    vti3_valid: bool
    score: int
    direction: str
    confidence_pct: int
    risk_level: str
    validity_window_h: int

def decide_direction(tech: TechSnapshot, flow: FlowSnapshot) -> str:
    if tech.trend_m15 == "Alta" and flow.inst_side == "Long":
        return "BUY"
    if tech.trend_m15 == "Baixa" and flow.inst_side == "Short":
        return "SELL"
    return "OUT"

def vti_validate(macro: MacroSnapshot, tech: TechSnapshot, flow: FlowSnapshot) -> VTIResult:
    # VTI-1: Macro Bias Alignment
    vti1 = (macro.risk_env == "Risk-On" and flow.inst_side == "Long") or (macro.risk_env == "Risk-Off" and flow.inst_side == "Short")
    # VTI-2: Structural-Flow Convergence
    vti2 = (tech.trend_m15 == tech.trend_h1 == tech.trend_h4) and ((tech.trend_m15 == "Alta" and flow.inst_side == "Long") or (tech.trend_m15 == "Baixa" and flow.inst_side == "Short"))
    # VTI-3: Temporal-Fundamental Harmony
    vti3 = (macro.expected_impact in ["Neutro","Positivo"]) and (macro.expected_vol in ["Baixa","Média"])

    score = int(vti1) + int(vti2) + int(vti3)
    direction = decide_direction(tech, flow)
    confidence = 30 + score*20
    risk = "Baixo" if score == 3 else ("Médio" if score == 2 else "Alto")
    validity = 3 if score == 3 else (2 if score == 2 else 1)

    return VTIResult(vti1, vti2, vti3, score, direction, confidence, risk, validity)
