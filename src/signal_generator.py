"""
Módulo principal que coordena todo o sistema
"""
from src.data_fetcher import DataFetcher
from src.vti_analyzer import VTIAnalyzer
from src.telegram_bot import TelegramBot
from datetime import datetime

def main():
    """Função principal do sistema"""

    print("=" * 60)
    print("ORACLE TRADING SYSTEM v1.0")
    print("=" * 60)
    print(f"Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} UTC")
    print("[INFO] Com calendário econômico integrado")

    try:
        # 1. Coleta dados de mercado
        print("Coletando dados de mercado...")
        fetcher = DataFetcher()
        market_data = fetcher.fetch_all_pairs()

        if not market_data:
            print("Nenhum dado coletado. Notificando erro...")
            try:
                bot = TelegramBot()
                bot.send_signals([])  # Envia mensagem de erro
            except:
                pass
            return

        print(f"{len(market_data)} pares coletados com sucesso.")

        # 2. Analisa com sistema VTI
        print("Executando análise VTI completa...")
        analyzer = VTIAnalyzer(market_data)
        signals = analyzer.analyze_all_pairs()

        print(f"{len(signals)} sinais gerados.")

        # 3. Envia para Telegram
        print("Enviando sinais para Telegram...")
        bot = TelegramBot()
        bot.send_signals(signals)

        print("=" * 60)
        print("ANÁLISE CONCLUÍDA COM SUCESSO")
        print("=" * 60)

    except Exception as e:
        print(f"ERRO CRÍTICO: {str(e)}")
        print(f"Tipo: {type(e).__name__}")

        import traceback
        traceback.print_exc()

        # Tenta notificar erro no Telegram
        try:
            bot = TelegramBot()
            error_msg = f"""
ERRO NO SISTEMA ORACLE

{type(e).__name__}
{str(e)[:200]}

{datetime.now().strftime('%d/%m/%Y %H:%M')} UTC

O sistema tentará novamente na próxima execução.
"""
            bot.send_message(error_msg)
        except:
            print("Não foi possível notificar erro via Telegram")

if __name__ == "__main__":
    main()
