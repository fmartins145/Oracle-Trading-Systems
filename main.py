#!/usr/bin/env python3
"""
Oracle Trading Systems v1.0
Framework GCT 10.0 - Institutional Execution
Análise automatizada de múltiplos pares forex/crypto
"""

import sys
from datetime import datetime
import config
from modules.data_fetcher import DataFetcher
from modules.signal_generator import SignalGenerator
from modules.telegram_notifier import TelegramNotifier

def print_header():
    """Exibe cabeçalho do sistema"""
    print("=" * 60)
    print(f"{config.SYSTEM_NAME}")
    print(f"Framework: {config.FRAMEWORK_VERSION}")
    print(f"Análise: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 60)
    print()

def analyze_pair(pair_symbol, pair_name, data_fetcher):
    """
    Analisa um par individual
    
    Args:
        pair_symbol: Símbolo para API (ex: 'EURUSD=X')
        pair_name: Nome amigável (ex: 'EURUSD')
        data_fetcher: Instância do DataFetcher
    
    Returns:
        Signal dict ou None
    """
    print(f"📊 Analisando {pair_name}...", end=" ")
    
    try:
        # 1. Buscar dados multi-timeframe
        data_multi_tf = data_fetcher.fetch_multiple_timeframes(pair_symbol)
        
        # 2. Validar dados
        if not data_multi_tf.get('15m') or data_multi_tf['15m'].empty:
            print("❌ Sem dados")
            return None
        
        # 3. Gerar sinal
        signal_gen = SignalGenerator(pair_name, pair_symbol, data_multi_tf)
        
        if not signal_gen.valid:
            print("❌ Dados inválidos")
            return None
        
        signal = signal_gen.generate_signal()
        
        if signal:
            print(f"✅ {signal['direction']} | VTI: {signal['vti_score']} | Confiança: {signal['confidence']}%")
            return signal
        else:
            print("⚪ Sem sinal")
            return None
    
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return None

def main():
    """Função principal do sistema"""
    print_header()
    
    # Validar credenciais Telegram
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("⚠️ AVISO: Credenciais Telegram não configuradas!")
        print("Configure TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID como secrets no GitHub")
        print()
    
    # Inicializar módulos
    data_fetcher = DataFetcher()
    telegram = TelegramNotifier()
    
    # Lista para armazenar sinais
    signals = []
    
    # Analisar cada par
    print("🔍 INICIANDO ANÁLISE DE MÚLTIPLOS PARES\n")
    
    for pair_symbol, pair_name in zip(config.PAIRS, config.PAIR_NAMES):
        signal = analyze_pair(pair_symbol, pair_name, data_fetcher)
        
        if signal:
            signals.append(signal)
    
    print()
    print("=" * 60)
    print(f"✅ ANÁLISE CONCLUÍDA")
    print(f"📊 Pares analisados: {len(config.PAIRS)}")
    print(f"📈 Sinais gerados: {len(signals)}")
    print("=" * 60)
    print()
    
    # Enviar sinais para o Telegram
    if signals:
        print("📱 ENVIANDO SINAIS PARA O TELEGRAM\n")
        
        for signal in signals:
            print(f"📤 Enviando {signal['pair']}...", end=" ")
            success = telegram.send_signal(signal)
            
            if success:
                print("✅")
            else:
                print("❌")
        
        print()
    
    # Enviar resumo
    print("📤 Enviando resumo...", end=" ")
    telegram.send_analysis_summary(len(config.PAIRS), len(signals))
    print("✅")
    
    print()
    print("=" * 60)
    print("🎯 SISTEMA FINALIZADO COM SUCESSO")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n⚠️ Execução interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {str(e)}")
        sys.exit(1)
