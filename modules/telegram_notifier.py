import requests
import config

class TelegramNotifier:
    """Envia notificações formatadas para o Telegram"""
    
    def __init__(self):
        self.bot_token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_signal(self, signal):
        """Envia sinal de trading formatado"""
        if signal is None:
            return False
        
        message = self._format_signal_message(signal)
        return self._send_message(message)
    
    def send_analysis_summary(self, analysis_count, signals_count):
        """Envia resumo da análise"""
        message = f"""
🔮 {config.SYSTEM_NAME}
📊 Análise Concluída

✅ Pares analisados: {analysis_count}
📈 Sinais gerados: {signals_count}
⏰ {self._get_timestamp()}

{config.FRAMEWORK_VERSION}
        """.strip()
        
        return self._send_message(message)
    
    def send_error(self, error_msg):
        """Envia notificação de erro"""
        message = f"⚠️ ERRO: {error_msg}"
        return self._send_message(message)
    
    def _format_signal_message(self, signal):
        """Formata mensagem do sinal"""
        direction_emoji = '🟢' if signal['direction'] == 'BUY' else '🔴'
        
        # Confirmações
        confirmations_text = '\n'.join([f"  • {c}" for c in signal['confirmations']]) if signal['confirmations'] else '  • Análise técnica padrão'
        
        # Suporte/Resistência
        sr = signal['support_resistance']
        sr_text = ''
        if sr.get('resistances'):
            sr_text += f"📈 R: {', '.join([f'${r:.5f}' for r in sr['resistances'][:2]])}\n"
        if sr.get('supports'):
            sr_text += f"📉 S: {', '.join([f'${s:.5f}' for s in sr['supports'][:2]])}\n"
        
        message = f"""
{direction_emoji} **{signal['direction']} {signal['pair']}**

━━━━━━━━━━━━━━━━━━━━
📊 **EXECUTIVE DASHBOARD**
━━━━━━━━━━━━━━━━━━━━

💰 Preço: **${signal['current_price']:.5f}**
🎯 VTI Score: **{signal['vti_score']}**
✅ Confiança: **{signal['confidence']}%**
⚠️ Risco: **{signal['risk_level']}**
📈 Tendência: {signal['trend']}
🔄 Padrão: {signal['pattern']}
💨 Volatilidade: {signal['volatility']}

━━━━━━━━━━━━━━━━━━━━
🎯 **PLANO DE EXECUÇÃO**
━━━━━━━━━━━━━━━━━━━━

🛑 Stop Loss: **${signal['stop_loss']:.5f}**

🎁 Take Profit 1: ${signal['take_profits']['tp1']:.5f} (R:R {signal['take_profits']['rr1']}:1)
🎁 Take Profit 2: ${signal['take_profits']['tp2']:.5f} (R:R {signal['take_profits']['rr2']}:1)
🎁 Take Profit 3: ${signal['take_profits']['tp3']:.5f} (R:R {signal['take_profits']['rr3']}:1)

💼 Tamanho Sugerido: **{signal['position']['position_size']} unidades**
💵 Valor: ${signal['position']['position_value']}
⚠️ Risco: ${signal['position']['risk_amount']} ({signal['position']['risk_percentage']}%)

━━━━━━━━━━━━━━━━━━━━
📍 **NÍVEIS ESTRUTURAIS**
━━━━━━━━━━━━━━━━━━━━

{sr_text}
━━━━━━━━━━━━━━━━━━━━
✅ **CONFIRMAÇÕES TÉCNICAS**
━━━━━━━━━━━━━━━━━━━━

{confirmations_text}

━━━━━━━━━━━━━━━━━━━━
⏰ {signal['timestamp']}
🔮 {config.SYSTEM_NAME}
        """.strip()
        
        return message
    
    def _send_message(self, text):
        """Envia mensagem via Telegram API"""
        if not self.bot_token or not self.chat_id:
            print("⚠️ Credenciais Telegram não configuradas")
            return False
        
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                print("✅ Mensagem enviada ao Telegram")
                return True
            else:
                print(f"❌ Erro Telegram: {response.status_code}")
                return False
        
        except Exception as e:
            print(f"❌ Exceção ao enviar mensagem: {str(e)}")
            return False
    
    def _get_timestamp(self):
        """Retorna timestamp formatado"""
        from datetime import datetime
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
