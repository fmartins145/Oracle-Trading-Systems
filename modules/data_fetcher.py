import pandas as pd
from datetime import datetime, timedelta
import pytz
import requests
import time
import os

class DataFetcher:
    """
    Coleta dados usando Twelve Data API (GRATUITA)
    800 requests/dia = suficiente para 8 pares, 3 timeframes, 3x/dia
    """
    
    def __init__(self):
        self.timezone = pytz.UTC
        self.calendar_cache = None
        self.calendar_cache_time = None
        
        # Twelve Data API Key
        self.twelve_data_key = os.environ.get('TWELVE_DATA_KEY', 'demo')
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Mapeamento de símbolos
        self.symbol_map = {
            'EURUSD': 'EUR/USD',
            'GBPUSD': 'GBP/USD',
            'USDCHF': 'USD/CHF',
            'USDJPY': 'USD/JPY',
            'USDCAD': 'USD/CAD',
            'AUDUSD': 'AUD/USD',
            'XAUUSD': 'XAU/USD',  # Ouro
            'BTCUSD': 'BTC/USD'
        }
        
        # Mapeamento de intervalos
        self.interval_map = {
            '15m': '15min',
            '1h': '1h',
            '4h': '4h',
            '1d': '1day'
        }
    
    def fetch_ohlcv(self, symbol, interval='15m', period='5d'):
        """
        Busca dados do Twelve Data
        
        Args:
            symbol: Par (EURUSD, GBPUSD, etc)
            interval: Timeframe ('15m', '1h', '4h', '1d')
            period: Período (não usado, Twelve Data retorna últimas velas)
        
        Returns:
            DataFrame com OHLCV
        """
        
        print(f"\n📊 Buscando {symbol} ({interval}):")
        
        try:
            # Converte símbolo
            td_symbol = self.symbol_map.get(symbol, symbol)
            td_interval = self.interval_map.get(interval, '15min')
            
            # Calcula outputsize baseado no período
            outputsize_map = {
                '15m': 480,  # ~5 dias de M15 (24h * 4 * 5)
                '1h': 720,   # ~1 mês de H1
                '4h': 180,   # ~1 mês de H4
                '1d': 90     # ~3 meses de D1
            }
            outputsize = outputsize_map.get(interval, 480)
            
            print(f"  🔄 API: {td_symbol} | {td_interval} | {outputsize} velas")
            
            # Request para Twelve Data
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
            
            # Verifica erros
            if 'status' in data and data['status'] == 'error':
                print(f"  ❌ API Error: {data.get('message', 'Unknown')}")
                
                # Se erro de limite, aguarda
                if 'limit' in data.get('message', '').lower():
                    print(f"  ⚠️ Limite de API atingido!")
                
                return None
            
            if 'values' not in data:
                print(f"  ❌ Sem dados. Keys: {list(data.keys())}")
                return None
            
            # Converte para DataFrame
            df = pd.DataFrame(data['values'])
            
            if df.empty:
                print(f"  ❌ DataFrame vazio")
                return None
            
            # Renomeia colunas
            df = df.rename(columns={
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume'
            })
            
            # Converte tipos
            for col in ['Open', 'High', 'Low', 'Close']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(1000)
            
            # Converte datetime
            df['datetime'] = pd.to_datetime(df['datetime'])
            df = df.set_index('datetime')
            
            # Ordena (mais antigo → mais recente)
            df = df.sort_index()
            
            # Remove timezone se houver
            if df.index.tz is not None:
                df.index = df.index.tz_localize(None)
            
            print(f"  ✅ {len(df)} velas obtidas")
            
            return df
        
        except Exception as e:
            print(f"  ❌ Exceção: {str(e)}")
            return None
    
    def fetch_multiple_timeframes(self, symbol):
        """Busca dados em múltiplos timeframes"""
        
        print(f"\n{'='*60}")
        print(f"📈 ANALISANDO: {symbol}")
        print(f"{'='*60}")
        
        data = {}
        
        # M15 (primário) - MAIS IMPORTANTE
        print("\n⏰ Timeframe M15 (primário):")
        df_15m = self.fetch_ohlcv(symbol, interval='15m')
        data['15m'] = df_15m
        
        if df_15m is None:
            print(f"\n❌ FALHA CRÍTICA: Não foi possível obter dados M15 para {symbol}")
            return {'15m': None, '1h': None, '4h': None}
        
        # Pequeno delay para não sobrecarregar API
        time.sleep(0.5)
        
        # H1 (secundário)
        print("\n⏰ Timeframe H1 (secundário):")
        df_1h = self.fetch_ohlcv(symbol, interval='1h')
        data['1h'] = df_1h
        
        time.sleep(0.5)
        
        # H4 (terciário)
        print("\n⏰ Timeframe H4 (terciário):")
        df_4h = self.fetch_ohlcv(symbol, interval='4h')
        data['4h'] = df_4h
        
        # Resumo
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
        """Busca eventos econômicos do Forex Factory"""
        
        # Cache de 30 minutos
        if self.calendar_cache and self.calendar_cache_time:
            cache_age = (datetime.utcnow() - self.calendar_cache_time).total_seconds()
            if cache_age < 1800:
                print("📅 Usando cache do calendário econômico")
                return self.calendar_cache
        
        try:
            print("📅 Buscando calendário econômico...")
            
            url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
            
            response = requests.get(url, timeout=15, headers=self.headers)
            
            if response.status_code != 200:
                print(f"⚠️ API calendário retornou {response.status_code}")
                return self._fallback_calendar()
            
            events = response.json()
            now = datetime.utcnow()
            
            next_24h = []
            next_48h = []
            high_impact = False
            
            for event in events:
                try:
                    event_date = event.get('date', '')
                    if not event_date:
                        continue
                    
                    event_time = datetime.strptime(event_date, '%Y-%m-%dT%H:%M:%S%z')
                    event_time = event_time.replace(tzinfo=None)
                    
                    hours_diff = (event_time - now).total_seconds() / 3600
                    
                    if event.get('impact') == 'High':
                        event_title = event.get('title', 'Unknown')
                        
                        if 0 <= hours_diff <= 24:
                            next_24h.append({
                                'title': event_title,
                                'time': event_time.strftime('%H:%M UTC'),
                                'hours_until': round(hours_diff, 1)
                            })
                            high_impact = True
                        elif 24 < hours_diff <= 48:
                            next_48h.append({
                                'title': event_title,
                                'time': event_time.strftime('%H:%M UTC'),
                                'hours_until': round(hours_diff, 1)
                            })
                except:
                    continue
            
            result = {
                'next_24h': next_24h[:5],
                'next_48h': next_48h[:5],
                'high_impact': high_impact,
                'total_events': len(events),
                'last_update': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
            }
            
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
        """Fallback quando API de calendário falha"""
        return {
            'next_24h': [],
            'next_48h': [],
            'high_impact': False,
            'total_events': 0,
            'last_update': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
            'error': 'API indisponível'
        }
    
    def test_api_connection(self):
        """Testa conexão com Twelve Data"""
        print("\n" + "="*60)
        print("🧪 TESTANDO CONEXÃO TWELVE DATA")
        print("="*60)
        
        test_symbol = 'EURUSD'
        
        print(f"\nTestando {test_symbol}...")
        df = self.fetch_ohlcv(test_symbol, interval='15m')
        
        if df is not None and not df.empty:
            print(f"\n✅ SUCESSO! API funcionando corretamente!")
            print(f"📊 Obtidas {len(df)} velas")
            print(f"💰 Último preço: {df['Close'].iloc[-1]:.5f}")
            return True
        else:
            print(f"\n❌ FALHA! Verifique sua API key")
            return False


# TESTE
if __name__ == "__main__":
    fetcher = DataFetcher()
    fetcher.test_api_connection()