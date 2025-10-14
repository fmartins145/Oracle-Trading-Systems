# Oracle-Trading-Systems

Automação do framework ORACLE GCT 10.0 (M15) com análises a cada 30 minutos via GitHub Actions, enviando sinais para Telegram.

- Pares: EURUSD, GBPUSD, USDCHF, USDJPY, USDCAD, AUDUSD, XAUUSD, BTCUSD
- Timeframe: M15
- Stack: yfinance, Alpha Vantage (fallback), Telegram Bot

## Como funciona
1. Coleta preços (M15), volume e delta aproximado.
2. Checa macro básico (eventos 24–48h e viés de risco).
3. Valida Trinity (VTI-1, VTI-2, VTI-3).
4. Formata o relatório ORACLE GCT 10.0 e envia ao Telegram.

## Configuração rápida
- Defina secrets no GitHub:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`
  - `ALPHA_VANTAGE_API_KEY` (opcional, fallback)
