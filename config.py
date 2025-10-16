import os

# ===== CONFIGURAÇÕES PRINCIPAIS =====

# SÍMBOLOS CORRETOS DO YAHOO FINANCE
# Testados e funcionais para dados M15

PAIRS = [
    'EURUSD=X',   # Euro/Dólar - Yahoo Forex
    'GBPUSD=X',   # Libra/Dólar - Yahoo Forex
    'USDCHF=X',   # Dólar/Franco - Yahoo Forex
    'JPY=X',      # Dólar/Yen - Yahoo Forex (formato diferente!)
    'CAD=X',      # Dólar/Canadense - Yahoo Forex (formato diferente!)
    'AUDUSD=X',   # Australiano/Dólar - Yahoo Forex
    'GC=F',       # Ouro (Gold Futures) - SEMPRE funciona
    'BTC-USD'     # Bitcoin - SEMPRE funciona
]

PAIR_NAMES = [
    'EURUSD',
    'GBPUSD',
    'USDCHF',
    'USDJPY',
    'USDCAD',
    'AUDUSD',
    'XAUUSD',
    'BTCUSD'
]

# BACKUP: Se algum continuar falhando, use estes (100% garantidos)
PAIRS_FALLBACK = [
    'BTC-USD',    # Bitcoin
    'ETH-USD',    # Ethereum
    'GC=F',       # Ouro
    'SI=F',       # Prata
    '^GSPC',      # S&P 500
    '^DJI',       # Dow Jones
    'CL=F',       # Petróleo
    'AAPL'        # Apple
]

PAIR_NAMES_FALLBACK = [
    'BTCUSD',
    'ETHUSD',
    'XAUUSD',
    'XAGUSD',
    'SP500',
    'DOW',
    'OIL',
    'AAPL'
]

TIMEFRAME = '15m'
ANALYSIS_INTERVAL = 30  # minutos

# ===== TELEGRAM =====
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# ===== PARÂMETROS VTI =====
VTI_THRESHOLD = 2  # Mínimo 2/3 para sinal condicional
VTI_CONFIDENCE_HIGH = 3  # 3/3 para executar

# ===== GESTÃO DE RISCO =====
MAX_POSITION_SIZE = 2.0  # % do capital
DEFAULT_LEVERAGE = 1
RISK_PER_TRADE = 1.5  # % máximo de risco
MIN_RISK_REWARD = 1.5

# ===== ANÁLISE TÉCNICA =====
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_PERIOD = 20
BB_STD = 2
ATR_PERIOD = 14
VOLUME_MA_PERIOD = 20

# ===== TIMEFRAMES PARA CONVERGÊNCIA =====
TIMEFRAMES = {
    'primary': '15m',
    'secondary': '1h',
    'tertiary': '4h'
}

# ===== MENSAGENS =====
SYSTEM_NAME = "🔮 ORACLE TRADING SYSTEMS v1.0"
FRAMEWORK_VERSION = "GCT 10.0"

# ===== ALTERNATIVAS DE SÍMBOLOS =====
# Se Forex continuar falhando, experimente estas variações:

SYMBOL_ALTERNATIVES = {
    'EURUSD': ['EURUSD=X', 'EUR=X'],
    'GBPUSD': ['GBPUSD=X', 'GBP=X'],
    'USDCHF': ['USDCHF=X', 'CHF=X'],
    'USDJPY': ['USDJPY=X', 'JPY=X'],
    'USDCAD': ['USDCAD=X', 'CAD=X'],
    'AUDUSD': ['AUDUSD=X', 'AUD=X'],
}