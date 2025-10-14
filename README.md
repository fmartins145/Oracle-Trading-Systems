# 🤖 Oracle Trading System v1.0

Sistema automatizado de análise de trading com framework **VTI (Trinity Validation Index)** e **calendário econômico integrado**.

## 📊 Características

- ✅ Análise de **8 pares**: EURUSD, GBPUSD, USDCHF, USDJPY, USDCAD, AUDUSD, XAUUSD, BTCUSD
- ✅ Timeframe **M15** com análise multi-temporal (M15/H1/H4)
- ✅ Sistema **VTI** com 3 pilares de validação institucional
- ✅ **Calendário econômico** integrado (JBlanked + Finnhub)
- ✅ Execução automática a cada **30 minutos**
- ✅ Notificações via **Telegram Bot**
- ✅ **100% gratuito** (GitHub Actions + APIs públicas)

---

## 🎯 Sistema VTI (Trinity Validation Index)

### Três Pilares de Validação:

**1. VTI-1: Macro Bias Alignment**
   - Analisa tendência H4 (macro)
   - Verifica volume institucional
   - Validado: Score ≥ 50/100

**2. VTI-2: Structural-Flow Convergence**
   - Convergência M15/H1
   - Confirmação RSI e MACD
   - Validado: Score ≥ 60/100

**3. VTI-3: Temporal-Fundamental Harmony** ⭐ **COM CALENDÁRIO ECONÔMICO**
   - Alinhamento M15/H1/H4
   - **Calendário econômico** (eventos high-impact)
   - Sentimento de mercado
   - Validado: Score ≥ 60/100

### Decisão Final:

| VTI Score | Status | Ação |
|-----------|--------|------|
| **3/3** | ✅ **VALIDADO** | Executar operação |
| **2/3** | ⚠️ **CONDICIONAL** | Aguardar confirmação |
| **≤1/3** | ❌ **INVÁLIDO** | Não operar |

---

## 🚀 Como Usar

### 1. Teste Manual

1. Vá em **Actions** → **Oracle Trading Bot**
2. Clique em **Run workflow** → **Run workflow**
3. Aguarde 2-3 minutos
4. Verifique seu Telegram! 🎉

### 2. Execução Automática

O sistema executa **automaticamente a cada 30 minutos** (24/7).

---

## 🔧 Tecnologias

- Python 3.11
- GitHub Actions (scheduler)
- yfinance (dados de mercado)
- JBlanked + Finnhub (calendário econômico)
- Telegram Bot API (notificações)

---

## ⚠️ Disclaimer

**AVISO:** Este sistema é para fins educacionais. Trading envolve riscos. Sempre faça sua própria análise. Não me responsabilizo por perdas financeiras.

---

## 📜 Licença

MIT License - Uso livre para fins educacionais

---

🤖 **Sistema 100% automatizado e operacional!**
