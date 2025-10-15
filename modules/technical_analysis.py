import pandas as pd
import numpy as np
from ta.trend import MACD, EMAIndicator, SMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import VolumeWeightedAveragePrice
import config

class TechnicalAnalyzer:
    """Análise técnica completa"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.calculate_indicators()
    
    def calculate_indicators(self):
        """Calcula todos os indicadores técnicos"""
        if self.df is None or self.df.empty:
            return
        
        close = self.df['Close']
        high = self.df['High']
        low = self.df['Low']
        volume = self.df['Volume']
        
        # RSI
        rsi = RSIIndicator(close, window=config.RSI_PERIOD)
        self.df['RSI'] = rsi.rsi()
        
        # MACD
        macd = MACD(close, 
                    window_slow=config.MACD_SLOW,
                    window_fast=config.MACD_FAST,
                    window_sign=config.MACD_SIGNAL)
        self.df['MACD'] = macd.macd()
        self.df['MACD_signal'] = macd.macd_signal()
        self.df['MACD_diff'] = macd.macd_diff()
        
        # Bollinger Bands
        bb = BollingerBands(close, window=config.BB_PERIOD, window_dev=config.BB_STD)
        self.df['BB_upper'] = bb.bollinger_hband()
        self.df['BB_middle'] = bb.bollinger_mavg()
        self.df['BB_lower'] = bb.bollinger_lband()
        
        # ATR
        atr = AverageTrueRange(high, low, close, window=config.ATR_PERIOD)
        self.df['ATR'] = atr.average_true_range()
        
        # EMAs
        self.df['EMA_20'] = EMAIndicator(close, window=20).ema_indicator()
        self.df['EMA_50'] = EMAIndicator(close, window=50).ema_indicator()
        self.df['EMA_200'] = EMAIndicator(close, window=200).ema_indicator()
        
        # Volume
        self.df['Volume_MA'] = SMAIndicator(volume, window=config.VOLUME_MA_PERIOD).sma_indicator()
    
    def detect_trend(self):
        """Detecta tendência com base em EMAs"""
        if self.df is None or len(self.df) < 200:
            return 'INDEFINIDA'
        
        last = self.df.iloc[-1]
        price = last['Close']
        ema20 = last['EMA_20']
        ema50 = last['EMA_50']
        ema200 = last['EMA_200']
        
        if pd.isna(ema20) or pd.isna(ema50) or pd.isna(ema200):
            return 'INDEFINIDA'
        
        # Tendência de alta
        if price > ema20 > ema50 > ema200:
            return 'ALTA'
        
        # Tendência de baixa
        elif price < ema20 < ema50 < ema200:
            return 'BAIXA'
        
        # Lateral
        else:
            return 'LATERAL'
    
    def detect_pattern(self):
        """Detecta padrões de price action"""
        if self.df is None or len(self.df) < 20:
            return 'INDEFINIDO'
        
        # Simplificado: analisa últimas 10 velas
        recent = self.df.tail(10)
        closes = recent['Close'].values
        
        # Impulso: 6+ velas na mesma direção
        up_candles = sum(closes[i] > closes[i-1] for i in range(1, len(closes)))
        
        if up_candles >= 7:
            return 'IMPULSO_ALTA'
        elif up_candles <= 3:
            return 'IMPULSO_BAIXA'
        else:
            return 'CONSOLIDAÇÃO'
    
    def get_support_resistance(self):
        """Identifica suportes e resistências"""
        if self.df is None or len(self.df) < 50:
            return {}
        
        # Usa máximas/mínimas recentes
        recent = self.df.tail(100)
        
        highs = recent['High'].values
        lows = recent['Low'].values
        
        # Resistências (top 3 máximas)
        resistance_levels = sorted(np.unique(highs), reverse=True)[:3]
        
        # Suportes (top 3 mínimas)
        support_levels = sorted(np.unique(lows))[:3]
        
        return {
            'resistances': resistance_levels.tolist(),
            'supports': support_levels.tolist()
        }
    
    def get_signal_confirmations(self):
        """Lista confirmações técnicas"""
        if self.df is None or len(self.df) < 50:
            return []
        
        confirmations = []
        last = self.df.iloc[-1]
        
        # RSI
        if last['RSI'] < config.RSI_OVERSOLD:
            confirmations.append("RSI sobreven <30 (reversão)")
        elif last['RSI'] > config.RSI_OVERBOUGHT:
            confirmations.append("RSI sobrecompra >70 (reversão)")
        
        # MACD
        if last['MACD'] > last['MACD_signal'] and self.df.iloc[-2]['MACD'] <= self.df.iloc[-2]['MACD_signal']:
            confirmations.append("MACD cruzou acima do sinal (bullish)")
        elif last['MACD'] < last['MACD_signal'] and self.df.iloc[-2]['MACD'] >= self.df.iloc[-2]['MACD_signal']:
            confirmations.append("MACD cruzou abaixo do sinal (bearish)")
        
        # Bollinger
        if last['Close'] < last['BB_lower']:
            confirmations.append("Preço abaixo da BB inferior (oversold)")
        elif last['Close'] > last['BB_upper']:
            confirmations.append("Preço acima da BB superior (overbought)")
        
        # Volume
        if last['Volume'] > last['Volume_MA'] * 1.5:
            confirmations.append("Volume 50%+ acima da média")
        
        return confirmations
    
    def calculate_volatility(self):
        """Calcula volatilidade com ATR"""
        if self.df is None or 'ATR' not in self.df.columns:
            return 'MÉDIA'
        
        last_atr = self.df['ATR'].iloc[-1]
        avg_atr = self.df['ATR'].tail(20).mean()
        
        if pd.isna(last_atr) or pd.isna(avg_atr):
            return 'MÉDIA'
        
        if last_atr > avg_atr * 1.5:
            return 'ALTA'
        elif last_atr < avg_atr * 0.7:
            return 'BAIXA'
        else:
            return 'MÉDIA'
