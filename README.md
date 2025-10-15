# 🔮 Oracle Trading Systems v1.0

Sistema automatizado de análise forex e crypto baseado no **Framework GCT 10.0 (Institutional Execution)**.

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Visão Geral

**Oracle Trading Systems** é um sistema totalmente automatizado que:

✅ Analisa **8 pares** (EURUSD, GBPUSD, USDCHF, USDJPY, USDCAD, AUDUSD, XAUUSD, BTCUSD)  
✅ Executa análises a cada **30 minutos**  
✅ Usa o **Trinity Validation System (VTI)** com 3 pilares independentes  
✅ Envia sinais prontos direto no **Telegram**  
✅ 100% **GRATUITO** (GitHub Actions + APIs públicas)

---

## 🎯 Trinity Validation System (VTI)

Cada sinal passa por **3 validações obrigatórias**:

### VTI-1: Macro Bias Alignment
Valida se o ambiente macro favorece a direção proposta

### VTI-2: Structural-Flow Convergence  
Confirma convergência entre estrutura técnica e fluxo institucional

### VTI-3: Temporal-Fundamental Harmony
Garante alinhamento de timeframes e ausência de eventos críticos

**Score VTI:**
- **3/3** = ✅ SINAL VALIDADO – Executar
- **2/3** = ⚠️ SINAL CONDICIONAL – Aguardar confirmação  
- **≤1/3** = ❌ SINAL INVÁLIDO – Não operar

---

## 🚀 Como Configurar

### Passo 1: Fork/Clone este repositório

```bash
git clone https://github.com/SEU_USUARIO/oracle-trading-systems.git
