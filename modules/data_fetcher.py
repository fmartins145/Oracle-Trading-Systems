import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz
import requests

class DataFetcher:
    """Coleta dados de mercado e calendário econômico usando APIs gratuitas"""
    
    def __init__(self):
        self.timezone = pytz.UTC
        self.calendar_cache = None
        self.calendar_cache_time = None
    
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
            
            df.index = df.index.tz_localize(None)
            return df
        
        except Exception as e:
            print(f"❌ Erro ao buscar {symbol}: {str(e)}")
            return None
    
    def fetch_multiple_timeframes(self, symbol):
        """Busca dados em múltiplos timeframes para análise VTI"""
        data = {}
        
        data['15m'] = self.fetch_ohlcv(symbol, interval='15m', period='5d')
        data['1h'] = self.fetch_ohlcv(symbol, interval='1h', period='1mo')
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
        Busca eventos econômicos reais do Forex Factory (API GRATUITA)
        
        Returns:
            dict com eventos das próximas 24-48h e flag de alto impacto
        """
        # Cache de 30 minutos para não sobrecarregar API
        if self.calendar_cache and self.calendar_cache_time:
            cache_age = (datetime.utcnow() - self.calendar_cache_time).total_seconds()
            if cache_age < 1800:  # 30 minutos
                print("📅 Usando cache do calendário econômico")
                return self.calendar_cache
        
        try:
            print("📅 Buscando calendário econômico do Forex Factory...")
            
            # API gratuita Forex Factory (JSON público)
            url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
            
            response = requests.get(url, timeout=15)
            
            if response.status_code != 200:
                print(f"⚠️ API retornou status {response.status_code}, usando fallback")
                return self._fallback_calendar()
            
            events = response.json()
            now = datetime.utcnow()
            
            next_24h = []
            next_48h = []
            high_impact = False
            
            print(f"📊 Processando {len(events)} eventos do calendário...")
            
            for event in events:
                try:
                    event_date = event.get('date', '')
                    if not event_date:
                        continue
                    
                    # Parse da data (formato ISO 8601)
                    event_time = datetime.strptime(event_date, '%Y-%m-%dT%H:%M:%S%z')
                    event_time = event_time.replace(tzinfo=None)
                    
                    # Calcula diferença em horas
                    hours_diff = (event_time - now).total_seconds() / 3600
                    
                    # Apenas eventos HIGH IMPACT
                    if event.get('impact') == 'High':
                        event_title = event.get('title', 'Unknown Event')
                        event_country = event.get('country', '')
                        
                        # Eventos nas próximas 24h
                        if 0 <= hours_diff <= 24:
                            next_24h.append({
                                'title': event_title,
                                'country': event_country,
                                'time': event_time.strftime('%H:%M UTC'),
                                'hours_until': round(hours_diff, 1)
                            })
                            high_impact = True
                            print(f"  ⚠️ HIGH IMPACT em {hours_diff:.1f}h: {event_title}")
                        
                        # Eventos entre 24-48h
                        elif 24 < hours_diff <= 48:
                            next_48h.append({
                                'title': event_title,
                                'country': event_country,
                                'time': event_time.strftime('%H:%M UTC'),
                                'hours_until': round(hours_diff, 1)
                            })
                
                except Exception as e:
                    continue
            
            result = {
                'next_24h': next_24h[:5],
                'next_48h': next_48h[:5],
                'high_impact': high_impact,
                'total_events': len(events),
                'last_update': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
            }
            
            # Atualiza cache
            self.calendar_cache = result
            self.calendar_cache_time = datetime.utcnow()
            
            if high_impact:
                print(f"🚨 {len(next_24h)} eventos HIGH IMPACT nas próximas 24h!")
            else:
                print("✅ Nenhum evento HIGH IMPACT nas próximas 24h")
            
            return result
        
        except Exception as e:
            print(f"❌ Erro ao buscar calendário: {str(e)}")
            return self._fallback_calendar()
    
    def _fallback_calendar(self):
        """Fallback quando API falha (assume mercado normal)"""
        print("⚠️ Usando calendário fallback (sem eventos críticos)")
        return {
            'next_24h': [],
            'next_48h': [],
            'high_impact': False,
            'total_events': 0,
            'last_update': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
            'error': 'API indisponível'
        }
