"""
Telegram Bot para envio de sinais de trading
"""
import os
import requests
from datetime import datetime
from config.settings import PAIR_NAMES

class TelegramBot:
    """Bot para enviar sinais via Telegram"""
    
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not self.token or not self.chat_id:
            raise ValueError("❌ TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID devem estar configurados!")
        
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        
    def send_message(self, text, parse_mode='Markdown'):
        """Envia mensagem para o Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                print("✅ Mensagem enviada com sucesso")
                return True
            else:
                print(f"❌ Erro ao enviar: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {str(e)}")
            return False
    
    def format_signal(self, signal):
        """Formata sinal no padrão Oracle GCT 10.0"""
        
        pair_name = PAIR_NAMES.get(signal['pair'], signal['pair'])
        
        # Emojis baseados na direção
        if signal['direction'] == 'BUY':
            emoji = '🟢'
            action = '📈 COMPRA'
        elif signal['direction'] == 'SELL':
            emoji = '🔴'
            action = '📉 VENDA'
        else:
            emoji = '⚪'
            action = '⏸️ AGUARDAR'
        
        # Emoji de risco
        risk_emoji = {
            'BAIXO': '🟢',
            'MÉDIO': '🟡',
            'ALTO': '🔴'
        }.get(signal['risk'], '⚪')
        
        # Formata preço com número correto de decimais
        current_price = signal.get('current_price', 0)
        if current_price:
            if 'JPY' in pair_name:
                price_str = f"{current_price:.3f}"
            elif 'BTC' in pair_name:
                price_str = f"{current_price:.2f}"
            else:
                price_str = f"{current_price:.5f}"
        else:
            price_str = "N/A"
        
        message = f"""
{emoji} *ORACLE GCT 10.0 - SINAL DETECTADO*

━━━━━━━━━━━━━━━━━━━━━━
📊 *PAR:* `{pair_name}`
⏰ *TIMEFRAME:* M15
🕐 *HORÁRIO:* {signal['timestamp'].strftime('%d/%m/%Y %H:%M')} UTC

━━━━━━━━━━━━━━━━━━━━━━
🎯 *EXECUTIVE DASHBOARD*

*Direção:* {action}
*Confiança:* {signal['confidence']:.1f}%
*Risco:* {risk_emoji} {signal['risk']}
*VTI Score:* {signal['vti_score']}/3
*Preço Atual:* ${price_str}

━━━━━━━━━━━━━━━━━━━━━━
🔍 *TRINITY VALIDATION SYSTEM*

*VTI-1: Macro Bias*
{'✅ VALIDADO' if signal['vti1']['status'] else '❌ FALHOU'} - Score: {signal['vti1']['score']}/100
Tendência: {signal['vti1'].get('trend', 'N/A')}
{chr(10).join(['  • ' + r for r in signal['vti1'].get('reasons', [])[:2]])}

*VTI-2: Structural-Flow*
{'✅ VALIDADO' if signal['vti2']['status'] else '❌ FALHOU'} - Score: {signal['vti2']['score']}/100
M15: {signal['vti2'].get('trend_15m', 'N/A')} | H1: {signal['vti2'].get('trend_1h', 'N/A')}
{chr(10).join(['  • ' + r for r in signal['vti2'].get('reasons', [])[:2]])}

*VTI-3: Temporal-Fundamental*
{'✅ VALIDADO' if signal['vti3']['status'] else '❌ FALHOU'} - Score: {signal['vti3']['score']}/100
Alinhamento: {signal['vti3'].get('alignment', 'N/A')}
{chr(10).join(['  • ' + r for r in signal['vti3'].get('reasons', [])[:3]])}

━━━━━━━━━━━━━━━━━━━━━━
📍 *NÍVEIS CRÍTICOS*

R3: ${signal['levels'].get('R3', 0):.5f}
R2: ${signal['levels'].get('R2', 0):.5f}
R1: ${signal['levels'].get('R1', 0):.5f}
───────────────
*PREÇO:* ${price_str}
───────────────
S1: ${signal['levels'].get('S1', 0):.5f}
S2: ${signal['levels'].get('S2', 0):.5f}
S3: ${signal['levels'].get('S3', 0):.5f}

━━━━━━━━━━━━━━━━━━━━━━
⚠️ *DECISÃO FINAL*

"""
        
        if signal['vti_score'] == 3:
            message += "✅ *SINAL VALIDADO* - Executar operação
"
            message += "Todos os 3 pilares VTI confirmados.
"
        elif signal['vti_score'] == 2:
            message += "⚠️ *SINAL CONDICIONAL* - Aguardar confirmação
"
            message += "2 de 3 pilares VTI validados.
"
        else:
            message += "❌ *SINAL INVÁLIDO* - Não operar
"
            message += "Critérios VTI insuficientes.
"
        
        message += "
🤖 _Oracle Trading System v1.0_"
        
        return message
    
    def send_signals(self, signals):
        """Envia todos os sinais relevantes"""
        
        if not signals:
            error_msg = f"""
🤖 *ORACLE TRADING SYSTEM*

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')} UTC

❌ Nenhum dado coletado nesta execução.
Verifique a conexão com yfinance.

_Próxima análise em 30 minutos._
"""
            self.send_message(error_msg)
            return
        
        # Filtra apenas sinais com VTI >= 2
        relevant_signals = [s for s in signals if s['vti_score'] >= 2]
        
        if not relevant_signals:
            summary = f"""
🤖 *ORACLE TRADING SYSTEM*

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')} UTC

ℹ️ Nenhum sinal validado neste momento.

📊 Análise completa:
• Pares analisados: {len(signals)}
• Sinais validados: 0
• Status: Aguardando configuração ideal

_Todos os pares estão fora dos critérios VTI._
_Próxima análise em 30 minutos._
"""
            self.send_message(summary)
            return
        
        # Envia cabeçalho
        header = f"""
🚀 *ORACLE TRADING SYSTEM*
⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')} UTC

📊 *{len(relevant_signals)} SINAL(IS) DETECTADO(S)*
━━━━━━━━━━━━━━━━━━━━━━
"""
        self.send_message(header)
        
        # Envia sinal individual para cada par relevante
        for signal in relevant_signals:
            formatted = self.format_signal(signal)
            self.send_message(formatted)
        
        # Envia resumo final
        vti_3 = sum(1 for s in relevant_signals if s['vti_score'] == 3)
        vti_2 = sum(1 for s in relevant_signals if s['vti_score'] == 2)
        
        summary = f"""
━━━━━━━━━━━━━━━━━━━━━━
📊 *RESUMO DA ANÁLISE*

✅ Total analisado: {len(signals)} pares
✅ Sinais validados (3/3): {vti_3}
⚠️ Sinais condicionais (2/3): {vti_2}

⏰ Próxima análise: 30 minutos

_Sistema Oracle GCT 10.0 operacional_ ✅
_Com calendário econômico integrado_ 📅
"""
        self.send_message(summary)
