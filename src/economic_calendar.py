"""
Módulo para coleta de dados de mercado usando APIs gratuitas
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz
from config.settings import PAIRS, HISTORICAL_DAYS, PAIR_NAMES

class DataFetcher:
    """Coleta dados de mercado em tempo real"""
    
    def __init__(self):
        self.pairs = PAIRS
        
    def fetch_data(self, symbol, interval='15m', days=7):
        """
        Baixa dados históricos do par
        
        Args:
            symbol: Símbolo do par (ex: 'EURUSD=X')
            interval: Intervalo (15m, 1h, 4h, 1d)
            days: Dias de histórico
        """
        try:
            ticker = yf.Ticker(symbol)
            end_date = datetime.now(pytz.UTC)
            start_date = end_date - timedelta(days=days)
            
            # Baixar dados
            df = ticker.history(
                start=start_date,
                end=end_date,
                interval=interval
            )
            
            if df.empty:
                print(f"⚠️  Sem dados para {symbol}")
                return None
                
            return df
            
        except Exception as e:
            print(f"❌ Erro ao buscar {symbol}: {str(e)}")
            return None
    
    def get_current_price(self, symbol):
        """Obtém preço atual do ativo"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1m')
            
            if not data.empty:
                return data['Close'].iloc[-1]
            return None
            
        except Exception as e:
            print(f"❌ Erro ao buscar preço de {symbol}: {str(e)}")
            return None
    
    def fetch_all_pairs(self):
        """Coleta dados de todos os pares configurados"""
        market_data = {}
        
        for pair in self.pairs:
            print(f"📊 Coletando dados: {PAIR_NAMES.get(pair, pair)}")
            
            # Dados em múltiplos timeframes
            data_15m = self.fetch_data(pair, '15m', 7)
            data_1h = self.fetch_data(pair, '1h', 30)
            data_4h = self.fetch_data(pair, '4h', 60)
            
            if data_15m is not None:
                market_data[pair] = {
                    '15m': data_15m,
                    '1h': data_1h,
                    '4h': data_4h,
                    'current_price': self.get_current_price(pair),
                    'symbol': pair  # Adiciona símbolo para calendário econômico
                }
        
        return market_data
