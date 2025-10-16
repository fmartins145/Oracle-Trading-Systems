import os

# ===== SEUS 8 PARES ORIGINAIS =====
PAIRS = [
    'EURUSD',
    'GBPUSD',
    'USDCHF',
    'USDJPY',
    'USDCAD',
    'AUDUSD',
    'XAUUSD',
    'BTCUSD'
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

TIMEFRAME = '15m'
ANALYSIS_INTERVAL = 480  # 8 horas (em minutos)

# ===== TELEGRAM =====
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# ===== TWELVE DATA (Cotações) =====
TWELVE_DATA_KEY = os.environ.get('TWELVE_DATA_KEY', 'demo')

# ===== TRADING ECONOMICS (Calendário Macro) =====
TE_API_KEY = os.environ.get('TE_API_KEY', '')

# ===== VTI =====
VTI_THRESHOLD = 2
VTI_CONFIDENCE_HIGH = 3

# ===== RISCO =====
MAX_POSITION_SIZE = 2.0
RISK_PER_TRADE = 1.5
MIN_RISK_REWARD = 1.5

# ===== TÉCNICA =====
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

# ===== TIMEFRAMES =====
TIMEFRAMES = {
    'primary': '15m',
    'secondary': '1h',
    'tertiary': '4h'
}

# ===== MENSAGENS =====
SYSTEM_NAME = "🔮 ORACLE TRADING SYSTEMS v1.0"
FRAMEWORK_VERSION = "GCT 10.0"