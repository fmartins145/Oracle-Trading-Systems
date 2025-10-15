import pandas as pd
from datetime import datetime
import config

class VTIAnalyzer:
    """
    Trinity Validation System (VTI)
    Valida sinais através de 3 pilares independentes
    """
    
    def __init__(self, pair_name, data_multi_tf, technical_analysis):
        self.pair_name = pair_name
        self.data = data_multi_tf
        self.tech = technical_analysis
        self.vti_results = {}
    
    def validate_vti1_macro(self):
        """
        VTI-1: Macro Bias Alignment
        Valida se ambiente macro favorece a direção
        """
        # Simulação simplificada (em produção real: APIs de sentimento, notícias, etc)
        
        # Para forex: detecta risk-on/risk-off baseado em tendência
        trend = self.tech.detect_trend()
        
        # Heurística básica
        if 'USD' in self.pair_name:
            # USD geralmente fortalece em risk-off
            if trend == 'ALTA':
                macro_bias = 'RISK_OFF'
                alignment = True
            elif trend == 'BAIXA':
                macro_bias = 'RISK_ON'
                alignment = True
            else:
                macro_bias = 'NEUTRO'
                alignment = False
        
        elif self.pair_name in ['XAUUSD', 'BTCUSD']:
            # Ouro e BTC favorecem risk-on em alta
            if trend == 'ALTA':
                macro_bias = 'RISK_ON'
                alignment = True
            elif trend == 'BAIXA':
                macro_bias = 'RISK_OFF'
                alignment = True
            else:
                macro_bias = 'NEUTRO'
                alignment = False
        
        else:
            macro_bias = 'NEUTRO'
            alignment = trend != 'LATERAL'
        
        self.vti_results['vti1'] = {
            'status': alignment,
            'macro_bias': macro_bias,
            'trend': trend,
            'analysis': f"Ambiente macro {'FAVORÁVEL' if alignment else 'DESFAVORÁVEL'} para {trend}"
        }
        
        return alignment
    
    def validate_vti2_structure_flow(self):
        """
        VTI-2: Structural-Flow Convergence
        Valida convergência entre estrutura técnica e fluxo
        """
        # Estrutura técnica
        trend_15m = self._get_trend_for_tf('15m')
        trend_1h = self._get_trend_for_tf('1h')
        trend_4h = self._get_trend_for_tf('4h')
        
        pattern = self.tech.detect_pattern()
        
        # Fluxo institucional (simulado via volume)
        df_15m = self.data.get('15m')
        if df_15m is not None and len(df_15m) > 0:
            last_volume = df_15m['Volume'].iloc[-1]
            avg_volume = df_15m['Volume'].tail(20).mean()
            
            volume_ratio = last_volume / avg_volume if avg_volume > 0 else 1.0
            
            if volume_ratio > 1.3:
                flow_sentiment = 'FORTE'
            elif volume_ratio > 1.0:
                flow_sentiment = 'MODERADO'
            else:
                flow_sentiment = 'FRACO'
        else:
            flow_sentiment = 'INDEFINIDO'
            volume_ratio = 1.0
        
        # Convergência: trends alinhados + volume confirmando
        trends_aligned = (trend_15m == trend_1h) or (trend_15m == trend_4h)
        flow_confirms = volume_ratio > 1.0
        
        convergence = trends_aligned and flow_confirms
        
        self.vti_results['vti2'] = {
            'status': convergence,
            'trend_15m': trend_15m,
            'trend_1h': trend_1h,
            'trend_4h': trend_4h,
            'pattern': pattern,
            'flow_sentiment': flow_sentiment,
            'volume_ratio': round(volume_ratio, 2),
            'analysis': f"{'Convergência detectada' if convergence else 'Divergência entre timeframes'}"
        }
        
        return convergence
    
    def validate_vti3_temporal_fundamental(self):
        """
        VTI-3: Temporal-Fundamental Harmony
        Valida alinhamento temporal e ausência de eventos críticos
        """
        # Convergência temporal
        trend_15m = self._get_trend_for_tf('15m')
        trend_1h = self._get_trend_for_tf('1h')
        
        temporal_alignment = (trend_15m == trend_1h) and (trend_15m != 'LATERAL')
        
        # Fundamentos imediatos (calendário econômico simulado)
        # Em produção: integrar API real
        has_high_impact_event = False  # Assumindo sem eventos críticos
        
        # Volatilidade aceitável
        volatility = self.tech.calculate_volatility()
        acceptable_volatility = volatility in ['BAIXA', 'MÉDIA']
        
        harmony = temporal_alignment and not has_high_impact_event and acceptable_volatility
        
        self.vti_results['vti3'] = {
            'status': harmony,
            'temporal_alignment': temporal_alignment,
            'high_impact_events': has_high_impact_event,
            'volatility': volatility,
            'analysis': f"{'Harmonia temporal confirmada' if harmony else 'Desalinhamento temporal ou alta volatilidade'}"
        }
        
        return harmony
    
    def calculate_vti_score(self):
        """Calcula score VTI (0-3)"""
        vti1 = self.validate_vti1_macro()
        vti2 = self.validate_vti2_structure_flow()
        vti3 = self.validate_vti3_temporal_fundamental()
        
        score = sum([vti1, vti2, vti3])
        
        self.vti_results['score'] = score
        self.vti_results['validated'] = score >= config.VTI_THRESHOLD
        
        return score
    
    def get_vti_report(self):
        """Retorna relatório VTI completo"""
        score = self.vti_results.get('score', 0)
        
        if score == 3:
            status = '✅ SINAL VALIDADO – Executar'
            confidence = 85
        elif score == 2:
            status = '⚠️ SINAL CONDICIONAL – Aguardar confirmação'
            confidence = 65
        else:
            status = '❌ SINAL INVÁLIDO – Não operar'
            confidence = 30
        
        return {
            'score': f"{score}/3",
            'status': status,
            'confidence': confidence,
            'vti1': self.vti_results.get('vti1', {}),
            'vti2': self.vti_results.get('vti2', {}),
            'vti3': self.vti_results.get('vti3', {})
        }
    
    def _get_trend_for_tf(self, timeframe):
        """Helper: detecta trend em timeframe específico"""
        df = self.data.get(timeframe)
        if df is None or len(df) < 50:
            return 'INDEFINIDO'
        
        # Usa EMAs para detectar trend
        close = df['Close'].values
        
        # EMA 20 vs 50
        if len(close) >= 50:
            ema20 = pd.Series(close).ewm(span=20, adjust=False).mean().iloc[-1]
            ema50 = pd.Series(close).ewm(span=50, adjust=False).mean().iloc[-1]
            
            if ema20 > ema50 * 1.001:  # 0.1% acima
                return 'ALTA'
            elif ema20 < ema50 * 0.999:  # 0.1% abaixo
                return 'BAIXA'
        
        return 'LATERAL'
