"""
Configurações gerais do Oracle Trading System
"""

# Pares de moedas para análise
PAIRS = [
    'EURUSD=X',
    'GBPUSD=X', 
    'USDCHF=X',
    'USDJPY=X',
    'USDCAD=X',
    'AUDUSD=X',
    'GC=F',      # Ouro (XAUUSD)
    'BTC-USD'    # Bitcoin
]

# Nomes amigáveis para exibição
PAIR_NAMES = {
    'EURUSD=X': 'EUR/USD',
    'GBPUSD=X': 'GBP/USD',
    'USDCHF=X': 'USD/CHF',
    'USDJPY=X': 'USD/JPY',
    'USDCAD=X': 'USD/CAD',
    'AUDUSD=X': 'AUD/USD',
    'GC=F': 'XAU/USD',
    'BTC-USD': 'BTC/USD'
}

# Timeframes para análise
PRIMARY_TIMEFRAME = '15m'
ANALYSIS_TIMEFRAMES = ['15m', '1h', '4h']

# Período de dados históricos (em dias)
HISTORICAL_DAYS = 30

# Parâmetros de indicadores técnicos
BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Thresholds de confiança
HIGH_CONFIDENCE = 75
MEDIUM_CONFIDENCE = 60
LOW_CONFIDENCE = 50

# Configuração de risco
MAX_RISK_PER_TRADE = 2.0  # % do capital

# ===== CALENDÁRIO ECONÔMICO =====

# Janela de verificação de eventos (horas)
EVENT_CHECK_WINDOW = 6

# Penalidade por evento high-impact próximo
EVENT_PENALTY = 20

# Bônus por janela limpa
CLEAN_WINDOW_BONUS = 10

# URLs das APIs de calendário econômico
JBLANKED_API_URL = "https://www.jblanked.com/news/api"
FINNHUB_API_URL = "https://finnhub.io/api/v1"
