import pandas as pd
from datetime import datetime, timedelta
import pytz
import requests
import time
import os

class DataFetcher:
    """
    Coleta dados de múltiplas fontes:
    - Twelve Data: Cotações M15 Forex/Crypto
    - Trading Economics: Calendário Econômico Macro
    """
    
    def __init__(self):
        self.timezone = pytz.UTC
        self.calendar_cache = None
        self.calendar_cache_time = None
        
        self.twelve_data_key = os.environ.get('TWELVE_DATA_KEY', 'demo')
        self.te_api_key = os.environ.get('TE_API_KEY', '')
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        self.symbol_map = {
            'EURUSD': 'EUR/USD',
            'GBPUSD': 'GBP/USD',
            'USDCHF': 'USD/CHF',
            'USDJPY': 'USD/JPY',
            'USDCAD': 'USD/CAD',
            'AUDUSD': 'AUD/USD',
            'XAUUSD': 'XAU/USD',
            'BTCUSD': 'BTC/USD'
        }
        
        self.interval_map = {
            '15m': '15min',
            '1h': '1h',
            '4h': '4h',
            '1d': '1day'
        }
        
        self.macro_countries = [
            'United States',
            'Euro Area', 
            'United Kingdom',
            'Japan',
            'Switzerland',
            'Canada',
            'Australia'
        ]
    
    def fetch_ohlcv(self, symbol, interval='15m', period='5d'):
        """Busca cotações do Twelve Data"""
        
        print(f"\n📊 Buscando {symbol} ({interval}):")
        
        try:
            td_symbol = self.symbol_map.get(symbol, symbol)
            td_interval = self.interval_map.get(interval, '15min')
            
            outputsize_map = {
                '15m': 480,
                '1h': 720,
                '4h': 180,
                '1d': 90
            }
            outputsize = outputsize_map.get(interval, 480)
            
            print(f"  🔄 Twelve Data: {td_symbol} | {td_interval} | {outputsize} velas")
            
            url = 'https://api.twelvedata.com/time_series'
            
            params = {
                'symbol': td_symbol,
                'interval': td_interval,
                'apikey': self.twelve_data_key,
                'outputsize': outputsize,
                'format': 'JSON'
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code != 200:
                print(f"  ❌ HTTP {response.status_code}")
                return None
            
            data = response.json()
            
            if 'status' in data and data['status'] == 'error':
                msg = data.get('message', 'Unknown')
                print(f"  ❌ API Error: {msg}")
                return None
            
            if 'values' not in data:
                print(f"  ❌ Sem dados. Keys: {list(data.keys())}")
                return None
            
            df = pd.DataFrame(data['values'])
            
            if df.empty:
                print(f"  ❌ DataFrame vazio")
                return None
            
            # Renomeia colunas base (Volume pode não existir)
            column_mapping = {
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close'
            }
            
            if 'volume' in df.columns:
                column_mapping['volume'] = 'Volume'
            
            df = df.rename(columns=column_mapping)
            
            # Converte OHLC
            for col in ['Open', 'High', 'Low', 'Close']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Volume: real ou fake
            if 'Volume' in df.columns:
                df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(1000)
            else:
                df['Volume'] = 1000
            
            # Datetime
            df['datetime'] = pd.to_datetime(df['datetime'])
            df = df.set_index('datetime')
            df = df.sort_index()
            
            if df.index.tz is not None:
                df.index = df.index.tz_localize(None)
            
            print(f"  ✅ {len(df)} velas obtidas")
            
            return df
        
        except Exception as e:
            print(f"  ❌ Exceção: {str(e)}")
            return None
    
    def fetch_multiple_timeframes(self, symbol):
        """Busca dados em múltiplos timeframes COM DELAYS para respeitar rate limit"""
        
        print(f"\n{'='*60}")
        print(f"📈 ANALISANDO: {symbol}")
        print(f"{'='*60}")
        
        data = {}
        
        # M15
        print("\n⏰ Timeframe M15 (primário):")
        df_15m = self.fetch_ohlcv(symbol, interval='15m')
        data['15m'] = df_15m
        
        if df_15m is None:
            print(f"\n❌ FALHA CRÍTICA: {symbol} sem dados M15")
            return {'15m': None, '1h': None, '4h': None}
        
        # DELAY para respeitar rate limit (8 requests/min)
        print("  ⏳ Aguardando 2s (rate limit)...")
        time.sleep(2)
        
        # H1
        print("\n⏰ Timeframe H1 (secundário):")
        df_1h = self.fetch_ohlcv(symbol, interval='1h')
        data['1h'] = df_1h
        
        print("  ⏳ Aguardando 2s (rate limit)...")
        time.sleep(2)
        
        # H4
        print("\n⏰ Timeframe H4 (terciário):")
        df_4h = self.fetch_ohlcv(symbol, interval='4h')
        data['4h'] = df_4h
        
        # DELAY entre pares
        print("  ⏳ Aguardando 5s antes do próximo par...")
        time.sleep(5)
        
        print(f"\n{'='*60}")
        print(f"📊 RESUMO {symbol}:")
        print(f"  M15: {'✅ ' + str(len(df_15m)) + ' velas' if df_15m is not None else '❌ Sem dados'}")
        print(f"  H1:  {'✅ ' + str(len(df_1h)) + ' velas' if df_1h is not None else '⚠️  Sem dados'}")
        print(f"  H4:  {'✅ ' + str(len(df_4h)) + ' velas' if df_4h is not None else '⚠️  Sem dados'}")
        print(f"{'='*60}\n")
        
        return data
    
    def get_current_price(self, symbol):
        """Obtém preço atual"""
        df = self.fetch_ohlcv(symbol, interval='15m')
        
        if df is not None and not df.empty:
            return df['Close'].iloc[-1]
        
        return None
    
    def get_economic_calendar(self):
        """Busca eventos econômicos do Trading Economics"""
        
        if self.calendar_cache and self.calendar_cache_time:
            cache_age = (datetime.utcnow() - self.calendar_cache_time).total_seconds()
            if cache_age < 14400:
                print("📅 Usando cache do calendário econômico")
                return self.calendar_cache
        
        print("\n" + "="*60)
        print("📅 BUSCANDO CALENDÁRIO ECONÔMICO - TRADING ECONOMICS")
        print("="*60)
        
        if not self.te_api_key:
            print("⚠️ TE_API_KEY não configurada, usando fallback")
            return self._fallback_calendar()
        
        try:
            now = datetime.utcnow()
            from_date = now.strftime('%Y-%m-%d')
            to_date = (now + timedelta(hours=48)).strftime('%Y-%m-%d')
            
            print(f"\n🔍 Período: {from_date} até {to_date}")
            
            url = 'https://api.tradingeconomics.com/calendar'
            
            params = {
                'c': self.te_api_key,
                'd1': from_date,
                'd2': to_date,
                'importance': '2,3'
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ Trading Economics retornou {response.status_code}")
                return self._fallback_calendar()
            
            events_raw = response.json()
            
            if not events_raw or not isinstance(events_raw, list):
                print(f"⚠️ Resposta vazia")
                return self._fallback_calendar()
            
            print(f"\n📊 Total de eventos: {len(events_raw)}")
            
            next_24h = []
            next_48h = []
            high_impact = False
            
            for event in events_raw:
                try:
                    country = event.get('Country', '')
                    event_name = event.get('Event', '')
                    importance = event.get('Importance', 1)
                    event_date_str = event.get('Date', '')
                    
                    if country not in self.macro_countries:
                        continue
                    
                    if not event_date_str:
                        continue
                    
                    event_time = datetime.strptime(event_date_str, '%Y-%m-%dT%H:%M:%S')
                    hours_diff = (event_time - now).total_seconds() / 3600
                    
                    if hours_diff < 0:
                        continue
                    
                    item = {
                        'title': event_name,
                        'country': country,
                        'time': event_time.strftime('%H:%M UTC'),
                        'date': event_time.strftime('%Y-%m-%d'),
                        'hours_until': round(hours_diff, 1),
                        'importance': importance
                    }
                    
                    if 0 <= hours_diff <= 24:
                        next_24h.append(item)
                        if importance == 3:
                            high_impact = True
                    elif 24 < hours_diff <= 48:
                        next_48h.append(item)
                
                except:
                    continue
            
            next_24h = sorted(next_24h, key=lambda x: x['hours_until'])[:10]
            next_48h = sorted(next_48h, key=lambda x: x['hours_until'])[:10]
            
            result = {
                'next_24h': next_24h,
                'next_48h': next_48h,
                'high_impact': high_impact,
                'total_events': len(next_24h) + len(next_48h),
                'last_update': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
                'source': 'Trading Economics'
            }
            
            self.calendar_cache = result
            self.calendar_cache_time = datetime.utcnow()
            
            print(f"\n📊 Próximas 24h: {len(next_24h)} eventos")
            print(f"📊 Próximas 48h: {len(next_48h)} eventos")
            print(f"🚨 High Impact: {'SIM' if high_impact else 'NÃO'}")
            
            return result
        
        except Exception as e:
            print(f"\n❌ Erro: {str(e)}")
            return self._fallback_calendar()
    
    def _fallback_calendar(self):
        """Fallback"""
        return {
            'next_24h': [],
            'next_48h': [],
            'high_impact': False,
            'total_events': 0,
            'last_update': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
            'source': 'Fallback'
        }