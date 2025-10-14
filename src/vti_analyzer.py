"""
Sistema Trinity Validation (VTI) - Análise completa de trading
Agora com integração de calendário econômico
"""
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import MACD, EMAIndicator, SMAIndicator
from ta.volatility import BollingerBands
from config.settings import *
from src.economic_calendar import EconomicCalendar

class VTIAnalyzer:
    """Analisador VTI completo seguindo o framework Oracle GCT 10.0"""
    
    def __init__(self, market_data):
        self.data = market_data
        self.calendar = EconomicCalendar()
        
    def calculate_indicators(self, df):
        """Calcula todos os indicadores técnicos"""
        if df is None or df.empty:
            return None
            
        try:
            # RSI
            rsi = RSIIndicator(close=df['Close'], window=RSI_PERIOD)
            df['RSI'] = rsi.rsi()
            
            # MACD
            macd = MACD(
                close=df['Close'],
                window_fast=MACD_FAST,
                window_slow=MACD_SLOW,
                window_sign=MACD_SIGNAL
            )
            df['MACD'] = macd.macd()
            df['MACD_signal'] = macd.macd_signal()
            df['MACD_hist'] = macd.macd_diff()
            
            # Bollinger Bands
            bb = BollingerBands(
                close=df['Close'],
                window=BOLLINGER_PERIOD,
                window_dev=BOLLINGER_STD
            )
            df['BB_upper'] = bb.bollinger_hband()
            df['BB_middle'] = bb.bollinger_mavg()
            df['BB_lower'] = bb.bollinger_lband()
            
            # EMAs
            df['EMA_20'] = EMAIndicator(close=df['Close'], window=20).ema_indicator()
            df['EMA_50'] = EMAIndicator(close=df['Close'], window=50).ema_indicator()
            
            # SMA 200
            if len(df) >= 200:
                df['SMA_200'] = SMAIndicator(close=df['Close'], window=200).sma_indicator()
            else:
                df['SMA_200'] = df['Close'].rolling(window=min(len(df), 50)).mean()
            
            # Stochastic
            stoch = StochasticOscillator(
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                window=14
            )
            df['Stoch_K'] = stoch.stoch()
            df['Stoch_D'] = stoch.stoch_signal()
            
            return df
            
        except Exception as e:
            print(f"❌ Erro ao calcular indicadores: {str(e)}")
            return None
    
    def detect_trend(self, df):
        """Detecta tendência atual"""
        if df is None or len(df) < 50:
            return 'INDEFINIDA'
            
        last_price = df['Close'].iloc[-1]
        ema_20 = df['EMA_20'].iloc[-1]
        ema_50 = df['EMA_50'].iloc[-1]
        
        if pd.isna(ema_20) or pd.isna(ema_50):
            return 'INDEFINIDA'
        
        if last_price > ema_20 > ema_50:
            return 'ALTA'
        elif last_price < ema_20 < ema_50:
            return 'BAIXA'
        else:
            return 'LATERAL'
    
    def vti_1_macro_bias(self, pair_data):
        """VTI-1: Macro Bias Alignment"""
        try:
            df_4h = pair_data['4h']
            if df_4h is None:
                return {'status': False, 'score': 0, 'reason': 'Dados insuficientes'}
            
            df_4h = self.calculate_indicators(df_4h)
            if df_4h is None:
                return {'status': False, 'score': 0, 'reason': 'Erro nos indicadores'}
            
            trend_4h = self.detect_trend(df_4h)
            
            # Análise de tendência macro
            score = 0
            reasons = []
            
            if trend_4h == 'ALTA':
                score += 40
                reasons.append("Tendência macro de ALTA confirmada")
            elif trend_4h == 'BAIXA':
                score += 40
                reasons.append("Tendência macro de BAIXA confirmada")
            else:
                score += 20
                reasons.append("Mercado em consolidação")
            
            # Volume analysis
            if 'Volume' in df_4h.columns:
                volume_avg = df_4h['Volume'].rolling(20).mean().iloc[-1]
                current_volume = df_4h['Volume'].iloc[-1]
                
                if not pd.isna(volume_avg) and not pd.isna(current_volume):
                    if current_volume > volume_avg * 1.2:
                        score += 30
                        reasons.append("Volume acima da média (+20%)")
                    elif current_volume > volume_avg:
                        score += 15
                        reasons.append("Volume saudável")
            
            validated = score >= 50
            
            return {
                'status': validated,
                'score': score,
                'trend': trend_4h,
                'reasons': reasons
            }
            
        except Exception as e:
            return {'status': False, 'score': 0, 'reason': f'Erro: {str(e)}'}
    
    def vti_2_structural_flow(self, pair_data):
        """VTI-2: Structural-Flow Convergence"""
        try:
            df_15m = pair_data['15m']
            df_1h = pair_data['1h']
            
            if df_15m is None or df_1h is None:
                return {'status': False, 'score': 0, 'reason': 'Dados insuficientes'}
            
            df_15m = self.calculate_indicators(df_15m)
            df_1h = self.calculate_indicators(df_1h)
            
            if df_15m is None or df_1h is None:
                return {'status': False, 'score': 0, 'reason': 'Erro nos indicadores'}
            
            trend_15m = self.detect_trend(df_15m)
            trend_1h = self.detect_trend(df_1h)
            
            score = 0
            reasons = []
            
            # Convergência de tendências
            if trend_15m == trend_1h and trend_15m != 'LATERAL':
                score += 50
                reasons.append(f"Convergência temporal: {trend_15m}")
            elif trend_15m != 'INDEFINIDA':
                score += 25
                reasons.append(f"Tendência M15: {trend_15m}")
            
            # RSI confirmation
            rsi_15m = df_15m['RSI'].iloc[-1]
            if not pd.isna(rsi_15m):
                if trend_15m == 'ALTA' and 40 < rsi_15m < 70:
                    score += 25
                    reasons.append(f"RSI saudável: {rsi_15m:.1f}")
                elif trend_15m == 'BAIXA' and 30 < rsi_15m < 60:
                    score += 25
                    reasons.append(f"RSI saudável: {rsi_15m:.1f}")
            
            # MACD confirmation
            macd_hist = df_15m['MACD_hist'].iloc[-1]
            if not pd.isna(macd_hist):
                if trend_15m == 'ALTA' and macd_hist > 0:
                    score += 25
                    reasons.append("MACD confirma alta")
                elif trend_15m == 'BAIXA' and macd_hist < 0:
                    score += 25
                    reasons.append("MACD confirma baixa")
            
            validated = score >= 60
            
            return {
                'status': validated,
                'score': score,
                'trend_15m': trend_15m,
                'trend_1h': trend_1h,
                'rsi': rsi_15m if not pd.isna(rsi_15m) else 0,
                'reasons': reasons
            }
            
        except Exception as e:
            return {'status': False, 'score': 0, 'reason': f'Erro: {str(e)}'}
    
    def vti_3_temporal_fundamental(self, pair_data):
        """VTI-3: Temporal-Fundamental Harmony (COM CALENDÁRIO ECONÔMICO)"""
        try:
            df_15m = pair_data['15m']
            df_1h = pair_data['1h']
            df_4h = pair_data['4h']
            
            if any(d is None for d in [df_15m, df_1h, df_4h]):
                return {'status': False, 'score': 0, 'reason': 'Dados insuficientes'}
            
            df_15m = self.calculate_indicators(df_15m)
            df_1h = self.calculate_indicators(df_1h)
            df_4h = self.calculate_indicators(df_4h)
            
            if any(d is None for d in [df_15m, df_1h, df_4h]):
                return {'status': False, 'score': 0, 'reason': 'Erro nos indicadores'}
            
            trend_15m = self.detect_trend(df_15m)
            trend_1h = self.detect_trend(df_1h)
            trend_4h = self.detect_trend(df_4h)
            
            score = 0
            reasons = []
            
            # Alinhamento de todos os timeframes
            if trend_15m == trend_1h == trend_4h and trend_15m != 'LATERAL':
                score += 50
                reasons.append(f"Alinhamento total: {trend_15m}")
            elif trend_15m == trend_1h:
                score += 30
                reasons.append(f"Alinhamento parcial: M15/H1")
            
            # Stochastic confirmation
            stoch_k = df_15m['Stoch_K'].iloc[-1]
            if not pd.isna(stoch_k):
                if trend_15m == 'ALTA' and stoch_k < 80:
                    score += 20
                    reasons.append("Stochastic permite entrada")
                elif trend_15m == 'BAIXA' and stoch_k > 20:
                    score += 20
                    reasons.append("Stochastic permite entrada")
            
            # ===== CALENDÁRIO ECONÔMICO =====
            try:
                pair_symbol = pair_data.get('symbol', '')
                
                # Verifica eventos nas próximas 6 horas
                has_event, events = self.calendar.has_major_event_soon(
                    pair_symbol, 
                    hours=EVENT_CHECK_WINDOW
                )
                
                if has_event:
                    score -= EVENT_PENALTY
                    event_names = [e['name'][:30] for e in events[:2]]
                    reasons.append(f"⚠️  {len(events)} evento(s) high-impact: {', '.join(event_names)}")
                else:
                    score += CLEAN_WINDOW_BONUS
                    reasons.append("✅ Janela limpa (sem eventos major)")
                
                # Analisa sentimento macro
                sentiment = self.calendar.get_market_sentiment()
                if sentiment == 'HIGH_VOLATILITY':
                    score -= 10
                    reasons.append("⚠️  Volatilidade elevada esperada")
                elif sentiment == 'ELEVATED_RISK':
                    score -= 5
                    reasons.append("⚠️  Risco elevado no mercado")
                
            except Exception as e:
                print(f"⚠️  Calendário econômico indisponível: {str(e)}")
                reasons.append("⚪ Calendário econômico não disponível")
            
            # ===== FIM CALENDÁRIO =====
            
            validated = score >= 60
            
            return {
                'status': validated,
                'score': score,
                'alignment': f"{trend_15m}/{trend_1h}/{trend_4h}",
                'reasons': reasons
            }
            
        except Exception as e:
            return {'status': False, 'score': 0, 'reason': f'Erro: {str(e)}'}
    
    def calculate_levels(self, df):
        """Calcula níveis de suporte e resistência"""
        if df is None or len(df) < 50:
            return {}
        
        high = df['High'].iloc[-50:].max()
        low = df['Low'].iloc[-50:].min()
        current = df['Close'].iloc[-1]
        
        # Níveis de Fibonacci
        diff = high - low
        fib_levels = {
            'R3': high,
            'R2': current + (diff * 0.618),
            'R1': current + (diff * 0.382),
            'S1': current - (diff * 0.382),
            'S2': current - (diff * 0.618),
            'S3': low
        }
        
        return fib_levels
    
    def generate_signal(self, pair, pair_data):
        """Gera sinal completo para um par"""
        print(f"
🔍 Analisando {pair}...")
        
        # Executa os 3 pilares VTI
        vti1 = self.vti_1_macro_bias(pair_data)
        vti2 = self.vti_2_structural_flow(pair_data)
        vti3 = self.vti_3_temporal_fundamental(pair_data)
        
        # Calcula VTI Score
        vti_score = sum([vti1['status'], vti2['status'], vti3['status']])
        
        # Determina direção
        if vti_score >= 2:
            df_15m = self.calculate_indicators(pair_data['15m'])
            if df_15m is not None:
                trend = self.detect_trend(df_15m)
                
                if trend == 'ALTA':
                    direction = 'BUY'
                elif trend == 'BAIXA':
                    direction = 'SELL'
                else:
                    direction = 'OUT'
            else:
                direction = 'OUT'
        else:
            direction = 'OUT'
        
        # Calcula confiança
        avg_score = (vti1['score'] + vti2['score'] + vti3['score']) / 3
        
        if avg_score >= HIGH_CONFIDENCE:
            confidence = avg_score
            risk = 'BAIXO'
        elif avg_score >= MEDIUM_CONFIDENCE:
            confidence = avg_score
            risk = 'MÉDIO'
        else:
            confidence = avg_score
            risk = 'ALTO'
        
        # Calcula níveis
        levels = self.calculate_levels(pair_data['15m'])
        
        signal = {
            'pair': pair,
            'direction': direction,
            'confidence': confidence,
            'risk': risk,
            'vti_score': vti_score,
            'vti1': vti1,
            'vti2': vti2,
            'vti3': vti3,
            'current_price': pair_data['current_price'],
            'levels': levels,
            'timestamp': pd.Timestamp.now(tz='UTC')
        }
        
        return signal
    
    def analyze_all_pairs(self):
        """Analisa todos os pares e gera sinais"""
        signals = []
        
        for pair, pair_data in self.data.items():
            try:
                signal = self.generate_signal(pair, pair_data)
                signals.append(signal)
            except Exception as e:
                print(f"❌ Erro ao analisar {pair}: {str(e)}")
                continue
        
        return signals
