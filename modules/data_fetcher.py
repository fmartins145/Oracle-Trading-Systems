import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz

class DataFetcher:
    """Coleta dados de mercado usando APIs gratuitas"""
    
    def __init__(self):
        self.timezone = pytz.UTC
    
    def fetch_ohlcv(self, symbol, interval='15m', period='5d'):
        """
        Busca dados OHLCV do Yahoo Finance
        
        Args:
            symbol: Par forex ou crypto (ex: 'EURUSD=X', 'BTC-USD')
            interval: Timeframe ('15m', '1h', '4h', '1d')
            period: Período histórico ('1d', '5d', '1mo')
        
        Returns:
            DataFrame com OHLCV
        """
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                return None
            
            df.index = df.index.tz_localize(None)  # Remove timezone
            return df
        
        except Exception as e:
            print(f"❌ Erro ao buscar {symbol}: {str(e)}")
            return None
    
    def fetch_multiple_timeframes(self, symbol):
        """Busca dados em múltiplos timeframes para análise VTI"""
        data = {}
        
        # M15 (primário)
        data['15m'] = self.fetch_ohlcv(symbol, interval='15m', period='5d')
        
        # H1 (secundário)
        data['1h'] = self.fetch_ohlcv(symbol, interval='1h', period='1mo')
        
        # H4 (terciário)
        data['4h'] = self.fetch_ohlcv(symbol, interval='1d', period='3mo')
        
        return data
    
    def get_current_price(self, symbol):
        """Obtém preço atual"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1m')
            
            if data.empty:
                return None
            
            return data['Close'].iloc[-1]
        
        except Exception as e:
            print(f"❌ Erro ao buscar preço de {symbol}: {str(e)}")
            return None
    
    def get_economic_calendar(self):
        """
        Simula calendário econômico (sem API paga)
        Em produção real, usar: tradingeconomics, investing.com scraper
        """
        # Retorna eventos fictícios para demonstração
        events = {
            'next_24h': [],
            'next_48h': ['FOMC Minutes', 'ECB Speech'],
            'high_impact': False
        }
        return events
