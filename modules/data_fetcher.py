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
        
        # ===== TWELVE DATA API =====
        self.twelve_data_key = os.environ.get('TWELVE_DATA_KEY', 'demo')
        
        # ===== TRADING ECONOMICS API =====
        self.te_api_key = os.environ.get('TE_API_KEY', '')
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Mapeamento de símbolos Forex/Crypto para Twelve Data
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
        
        # Países relevantes para calendário econômico
        self.macro_countries = [
            'United States',
            'Euro Area', 
            'United Kingdom',
            'Japan',
            'Switzerland',
            'Canada',
            'Australia'
        ]
    
    # =========================================================
    # TWELVE DATA - COTAÇÕES M15
    # =========================================================
    
    def fetch_ohlcv(self, symbol, interval='15m', period='5d'):
        """
        Busca cotações do Twelve Data
        
        Args:
            symbol: Par (EURUSD, GBPUSD, etc)
            interval: Timeframe ('15m', '1h', '4h', '1d')
        
        Returns:
            DataFrame com OHLCV
        """
        
        print(f"\n📊 Buscando {symbol} ({interval}):")
        
        try:
            # Converte símbolo
            td_symbol = self.symbol_map.get(symbol, symbol)
            td_interval = self.interval_map.get(interval, '15min')
            
            # Calcula outputsize
            outputsize_map = {
                '15m': 480,  # ~5 dias
                '1h': 720,   # ~1 mês
                '4h': 180,   # ~1 mês
                '1d': 90     # ~3 meses
            }
            outputsize = outputsize_map.get(interval, 480)
            
            print(f"  🔄 Twelve Data: {td_symbol} | {td_interval} | {outputsize} velas")
            
            # Request
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
                msg = data.get('message', 'Unknown')
                print(f"  ❌ API Error: {msg}")
                
                if 'limit' in msg.lower():
                    print(f"  ⚠️ Limite de API atingido! Aguarde alguns minutos.")
                
                return None
            
            if 'values' not in data:
                print(f"  ❌ Sem dados. Response keys: {list(data.keys())}")
                return None
            
            # Converte para DataFrame
            df = pd.DataFrame(data['values'])
            
            if df.empty:
                print(f"  ❌ DataFrame vazio")
                return None
            
            # Renomeia e converte colunas
            df = df.rename(columns={
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume'
            })
            
            for col in ['Open', 'High', 'Low', 'Close']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(1000)
            
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
        """Busca dados em múltiplos timeframes"""
        
        print(f"\n{'='*60}")
        print(f"📈 ANALISANDO: {symbol}")
        print(f"{'='*60}")
        
        data = {}
        
        # M15 (primário)
        print("\n⏰ Timeframe M15 (primário):")
        df_15m = self.fetch_ohlcv(symbol, interval='15m')
        data['15m'] = df_15m
        
        if df_15m is None:
            print(f"\n❌ FALHA CRÍTICA: {symbol} sem dados M15")
            return {'15m': None, '1h': None, '4h': None}
        
        time.sleep(0.5)  # Rate limit
        
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
    
    # =========================================================
    # TRADING ECONOMICS - CALENDÁRIO MACRO
    # =========================================================
    
    def get_economic_calendar(self):
        """
        Busca eventos econômicos do Trading Economics
        
        Retorna eventos HIGH/MEDIUM das próximas 24-48h
        para validação VTI-3 (Temporal-Fundamental Harmony)
        """
        
        # Cache de 4 horas (atualiza 2x por ciclo de 8h)
        if self.calendar_cache and self.calendar_cache_time:
            cache_age = (datetime.utcnow() - self.calendar_cache_time).total_seconds()
            if cache_age < 14400:  # 4 horas
                print("📅 Usando cache do calendário econômico")
                return self.calendar_cache
        
        print("\n" + "="*60)
        print("📅 BUSCANDO CALENDÁRIO ECONÔMICO - TRADING ECONOMICS")
        print("="*60)
        
        if not self.te_api_key:
            print("⚠️ TE_API_KEY não configurada, usando fallback")
            return self._fallback_calendar()
        
        try:
            # Janela de 48 horas à frente
            now = datetime.utcnow()
            from_date = now.strftime('%Y-%m-%d')
            to_date = (now + timedelta(hours=48)).strftime('%Y-%m-%d')
            
            print(f"\n🔍 Período: {from_date} até {to_date}")
            print(f"🌍 Países: {', '.join(self.macro_countries[:3])}...")
            
            # Request para Trading Economics
            url = 'https://api.tradingeconomics.com/calendar'
            
            params = {
                'c': self.te_api_key,
                'd1': from_date,
                'd2': to_date,
                'importance': '2,3'  # Apenas Medium (2) e High (3)
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ Trading Economics API retornou {response.status_code}")
                return self._fallback_calendar()
            
            events_raw = response.json()
            
            if not events_raw or not isinstance(events_raw, list):
                print(f"⚠️ Resposta vazia ou inválida")
                return self._fallback_calendar()
            
            print(f"\n📊 Total de eventos retornados: {len(events_raw)}")
            
            # Filtrar por países relevantes e processar
            next_24h = []
            next_48h = []
            high_impact = False
            
            for event in events_raw:
                try:
                    # Campos principais
                    country = event.get('Country', '')
                    event_name = event.get('Event', '')
                    importance = event.get('Importance', 1)
                    event_date_str = event.get('Date', '')
                    
                    # Filtro por país
                    if country not in self.macro_countries:
                        continue
                    
                    # Parse da data
                    if not event_date_str:
                        continue
                    
                    # Formato: "2025-10-16T08:30:00"
                    event_time = datetime.strptime(event_date_str, '%Y-%m-%dT%H:%M:%S')
                    
                    # Diferença em horas
                    hours_diff = (event_time - now).total_seconds() / 3600
                    
                    # Apenas eventos futuros
                    if hours_diff < 0:
                        continue
                    
                    # Montar item
                    item = {
                        'title': event_name,
                        'country': country,
                        'time': event_time.strftime('%H:%M UTC'),
                        'date': event_time.strftime('%Y-%m-%d'),
                        'hours_until': round(hours_diff, 1),
                        'importance': importance,
                        'actual': event.get('Actual', ''),
                        'forecast': event.get('Forecast', ''),
                        'previous': event.get('Previous', '')
                    }
                    
                    # Classificar por janela
                    if 0 <= hours_diff <= 24:
                        next_24h.append(item)
                        if importance == 3:  # HIGH
                            high_impact = True
                    elif 24 < hours_diff <= 48:
                        next_48h.append(item)
                
                except Exception as e:
                    continue
            
            # Ordenar por proximidade
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
            
            # Atualiza cache
            self.calendar_cache = result
            self.calendar_cache_time = datetime.utcnow()
            
            # Log resumo
            print(f"\n{'='*60}")
            print(f"📊 RESUMO CALENDÁRIO:")
            print(f"  Próximas 24h: {len(next_24h)} eventos")
            print(f"  Próximas 48h: {len(next_48h)} eventos")
            print(f"  High Impact: {'SIM' if high_impact else 'NÃO'}")
            print(f"{'='*60}")
            
            if high_impact:
                print(f"\n🚨 EVENTOS HIGH IMPACT DETECTADOS:")
                for evt in next_24h[:3]:
                    if evt['importance'] == 3:
                        print(f"  • {evt['time']} - {evt['title']} ({evt['country']})")
            
            return result
        
        except Exception as e:
            print(f"\n❌ Erro ao buscar calendário: {str(e)}")
            return self._fallback_calendar()
    
    def _fallback_calendar(self):
        """Fallback quando Trading Economics falha"""
        print("⚠️ Usando calendário fallback (sem eventos)")
        return {
            'next_24h': [],
            'next_48h': [],
            'high_impact': False,
            'total_events': 0,
            'last_update': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
            'source': 'Fallback',
            'error': 'API indisponível'
        }
    
    # =========================================================
    # TESTES E VALIDAÇÃO
    # =========================================================
    
    def test_connections(self):
        """Testa ambas as APIs"""
        print("\n" + "="*60)
        print("🧪 TESTANDO CONEXÕES")
        print("="*60)
        
        # Teste Twelve Data
        print("\n1️⃣ TWELVE DATA (Cotações):")
        df = self.fetch_ohlcv('EURUSD', interval='15m')
        
        if df is not None and not df.empty:
            print(f"✅ Twelve Data OK - {len(df)} velas | Último preço: {df['Close'].iloc[-1]:.5f}")
            td_ok = True
        else:
            print(f"❌ Twelve Data FALHOU")
            td_ok = False
        
        # Teste Trading Economics
        print("\n2️⃣ TRADING ECONOMICS (Calendário Macro):")
        calendar = self.get_economic_calendar()
        
        if calendar['total_events'] > 0:
            print(f"✅ Trading Economics OK - {calendar['total_events']} eventos")
            te_ok = True
        elif 'error' in calendar:
            print(f"⚠️ Trading Economics com erro: {calendar.get('error')}")
            te_ok = False
        else:
            print(f"✅ Trading Economics OK - Sem eventos nas próximas 48h")
            te_ok = True
        
        # Resumo
        print("\n" + "="*60)
        if td_ok and te_ok:
            print("✅ SISTEMA 100% OPERACIONAL!")
        elif td_ok:
            print("⚠️ Sistema parcial: Cotações OK, Calendário com problemas")
        elif te_ok:
            print("⚠️ Sistema parcial: Calendário OK, Cotações com problemas")
        else:
            print("❌ SISTEMA COM FALHAS CRÍTICAS")
        print("="*60)
        
        return td_ok and te_ok


# TESTE
if __name__ == "__main__":
    fetcher = DataFetcher()
    fetcher.test_connections()