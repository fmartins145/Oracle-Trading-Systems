import config

class RiskManager:
    """Gestão de risco e cálculo de posições"""
    
    def __init__(self, current_price, atr):
        self.current_price = current_price
        self.atr = atr
    
    def calculate_stop_loss(self, direction, support_resistance):
        """
        Calcula stop loss baseado em estrutura
        
        Args:
            direction: 'BUY' ou 'SELL'
            support_resistance: dict com supports/resistances
        """
        if direction == 'BUY':
            # Stop abaixo do suporte mais próximo
            supports = support_resistance.get('supports', [])
            if supports:
                stop_loss = supports[0] * 0.998  # 0.2% abaixo do suporte
            else:
                # Fallback: 1.5 ATR abaixo
                stop_loss = self.current_price - (1.5 * self.atr)
        
        elif direction == 'SELL':
            # Stop acima da resistência mais próxima
            resistances = support_resistance.get('resistances', [])
            if resistances:
                stop_loss = resistances[0] * 1.002  # 0.2% acima da resistência
            else:
                # Fallback: 1.5 ATR acima
                stop_loss = self.current_price + (1.5 * self.atr)
        
        else:
            stop_loss = self.current_price
        
        return round(stop_loss, 5)
    
    def calculate_take_profits(self, direction, stop_loss):
        """
        Calcula 3 níveis de take profit
        
        Args:
            direction: 'BUY' ou 'SELL'
            stop_loss: nível do stop loss
        """
        risk = abs(self.current_price - stop_loss)
        
        if direction == 'BUY':
            tp1 = self.current_price + (risk * 1.5)  # R:R 1.5:1
            tp2 = self.current_price + (risk * 2.5)  # R:R 2.5:1
            tp3 = self.current_price + (risk * 4.0)  # R:R 4:1
        
        elif direction == 'SELL':
            tp1 = self.current_price - (risk * 1.5)
            tp2 = self.current_price - (risk * 2.5)
            tp3 = self.current_price - (risk * 4.0)
        
        else:
            tp1 = tp2 = tp3 = self.current_price
        
        return {
            'tp1': round(tp1, 5),
            'tp2': round(tp2, 5),
            'tp3': round(tp3, 5),
            'rr1': 1.5,
            'rr2': 2.5,
            'rr3': 4.0
        }
    
    def calculate_position_size(self, stop_loss, account_size=10000):
        """
        Calcula tamanho de posição baseado em risco
        
        Args:
            stop_loss: nível do SL
            account_size: tamanho da conta (default: $10k)
        """
        risk_amount = account_size * (config.RISK_PER_TRADE / 100)
        
        risk_per_unit = abs(self.current_price - stop_loss)
        
        if risk_per_unit == 0:
            position_size = 0
        else:
            position_size = risk_amount / risk_per_unit
        
        # Limita ao máximo configurado
        max_position = account_size * (config.MAX_POSITION_SIZE / 100)
        position_value = position_size * self.current_price
        
        if position_value > max_position:
            position_size = max_position / self.current_price
        
        return {
            'position_size': round(position_size, 4),
            'position_value': round(position_size * self.current_price, 2),
            'risk_amount': round(risk_amount, 2),
            'risk_percentage': config.RISK_PER_TRADE
        }
    
    def validate_risk_reward(self, stop_loss, take_profit):
        """Valida se R:R mínimo foi atingido"""
        risk = abs(self.current_price - stop_loss)
        reward = abs(take_profit - self.current_price)
        
        if risk == 0:
            return False
        
        rr_ratio = reward / risk
        
        return rr_ratio >= config.MIN_RISK_REWARD
