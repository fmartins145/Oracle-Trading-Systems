from datetime import datetime
import config
from modules.technical_analysis import TechnicalAnalyzer
from modules.vti_analyzer import VTIAnalyzer
from modules.risk_manager import RiskManager

class SignalGenerator:
    """Gera sinais de trading completos com framework GCT"""
    
    def __init__(self, pair_name, pair_symbol, data_multi_tf):
        self.pair_name = pair_name
        self.pair_symbol = pair_symbol
        self.data = data_multi_tf
        self.df_primary = data_multi_tf.get('15m')
        
        # FIX: Validação correta de DataFrame
        if self.df_primary is None:
            self.valid = False
            return
        
        # Verifica se está vazio DEPOIS de confirmar que não é None
        if self.df_primary.empty:
            self.valid = False
            return
        
        self.valid = True
        self.tech = TechnicalAnalyzer(self.df_primary)
        self.vti = VTIAnalyzer(pair_name, data_multi_tf, self.tech)
        
        self.current_price = self.df_primary['Close'].iloc[-1]
        self.atr = self.df_primary['ATR'].iloc[-1] if 'ATR' in self.df_primary.columns else 0.001
    
    def generate_signal(self):
        """Gera sinal completo de trading"""
        if not self.valid:
            return None
        
        # 1. Calcula VTI Score
        vti_score = self.vti.calculate_vti_score()
        vti_report = self.vti.get_vti_report()
        
        # 2. Se VTI < 2, não gera sinal
        if vti_score < config.VTI_THRESHOLD:
            return None
        
        # 3. Determina direção
        direction = self._determine_direction()
        
        if direction == 'OUT':
            return None
        
        # 4. Análise técnica
        trend = self.tech.detect_trend()
        pattern = self.tech.detect_pattern()
        sr_levels = self.tech.get_support_resistance()
        confirmations = self.tech.get_signal_confirmations()
        volatility = self.tech.calculate_volatility()
        
        # 5. Gestão de risco
        risk_mgr = RiskManager(self.current_price, self.atr)
        
        stop_loss = risk_mgr.calculate_stop_loss(direction, sr_levels)
        take_profits = risk_mgr.calculate_take_profits(direction, stop_loss)
        position = risk_mgr.calculate_position_size(stop_loss)
        
        # 6. Valida R:R
        if not risk_mgr.validate_risk_reward(stop_loss, take_profits['tp2']):
            return None
        
        # 7. Monta sinal completo
        signal = {
            'pair': self.pair_name,
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
            'current_price': round(self.current_price, 5),
            'direction': direction,
            'vti_score': vti_report['score'],
            'vti_status': vti_report['status'],
            'confidence': vti_report['confidence'],
            'trend': trend,
            'pattern': pattern,
            'volatility': volatility,
            'stop_loss': stop_loss,
            'take_profits': take_profits,
            'position': position,
            'support_resistance': sr_levels,
            'confirmations': confirmations[:3],
            'vti_details': vti_report,
            'risk_level': self._assess_risk_level(volatility, vti_score)
        }
        
        return signal
    
    def _determine_direction(self):
        """Determina direção do sinal (BUY/SELL/OUT)"""
        if self.df_primary is None or len(self.df_primary) < 50:
            return 'OUT'
        
        last = self.df_primary.iloc[-1]
        
        # Critérios combinados
        trend = self.tech.detect_trend()
        rsi = last.get('RSI', 50)
        macd_diff = last.get('MACD_diff', 0)
        
        # BUY: Tendência alta + RSI < 70 + MACD positivo
        if trend == 'ALTA' and rsi < 70 and macd_diff > 0:
            return 'BUY'
        
        # SELL: Tendência baixa + RSI > 30 + MACD negativo
        elif trend == 'BAIXA' and rsi > 30 and macd_diff < 0:
            return 'SELL'
        
        # Fora do mercado
        else:
            return 'OUT'
    
    def _assess_risk_level(self, volatility, vti_score):
        """Avalia nível de risco da operação"""
        if vti_score == 3 and volatility == 'BAIXA':
            return 'BAIXO'
        elif vti_score == 3 and volatility == 'MÉDIA':
            return 'BAIXO'
        elif vti_score == 2 and volatility in ['BAIXA', 'MÉDIA']:
            return 'MÉDIO'
        else:
            return 'ALTO'