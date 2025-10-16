import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz
import requests
import time

class DataFetcher:
    """
    Coleta dados APENAS do Yahoo Finance
    Com múltiplas estratégias de retry e símbolos alternativos
    """
    
    def __init__(self):
        self.timezone = pytz.UTC
        self.calendar_cache = None
        self.calendar_cache_time = None
        
        # Headers para evitar bloqueio
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        # Símbolos alternativos para cada par
        self.symbol_alternatives = {
            'EURUSD': ['EURUSD=X', 'EUR=X'],
            'GBPUSD': ['GBPUSD=X', 'GBP=X'],
            'USDCHF': ['USDCHF=X', 'CHF=X'],
            'USDJPY': ['USDJPY=X', 'JPY=X'],
            'USDCAD': ['USDCAD=X', 'CAD=X'],
            'AUDUSD': ['AUDUSD=X', 'AUD=X'],
            'XAUUSD': ['GC=F', 'XAUUSD=X'],
            'BTCUSD': ['BTC-USD', 'BTCUSD'],
        }
    
    def fetch_ohlcv(self, symbol, interval='15m', period='5d', max_retries=3):
        """
        Busca dados com múltiplas estratégias:
        1. Tenta símbolo original
        2. Tenta símbolos alternativos
        3. Usa método download() como fallback
        4. Exponential backoff entre tentativas
        """
        
        # Determina símbolos a testar
        symbols_to_try = self._get_symbols_to_try(symbol)
        
        print(f"\n📊 Buscando {symbol}:")
        
        for sym in symbols_to_try:
            print(f"  🔄 Tentando: {sym}")
            
            # Estratégia 1: yfinance Ticker
            df = self._fetch_with_ticker(sym, interval, period, max_retries)
            
            if df is not None and not df.empty:
                print(f"  ✅ Sucesso com {sym}: {len(df)} velas")
                return df
            
            # Estratégia 2: yfinance download
            df = self._fetch_with_download(sym, interval, period)
            
            if df is not None and not df.empty:
                print(f"  ✅ Sucesso (download) com {sym}: {len(df)} velas")
                return df
            
            print(f"  ❌ {sym} falhou")
        
        print(f"  ❌ TODAS as alternativas falharam para {symbol}")
        return None
    
    def _get_symbols_to_try(self, symbol):
        """Retorna lista de símbolos alternativos para tentar"""
        
        # Remove sufixos comuns
        clean_symbol = symbol.replace('=X', '').replace('-USD', '').replace('USD', '')
        
        # Verifica se há alternativas definidas
        if clean_symbol in self.symbol_alternatives:
            return self.symbol_alternatives[clean_symbol]
        
        # Senão, tenta variações comuns
        variations = [
            symbol,
            f"{symbol}=X",
            f"{symbol}-USD",
            clean_symbol,
        ]
        
        # Remove duplicatas mantendo ordem
        return list(dict.fromkeys(variations))
    
    def _fetch_with_ticker(self, symbol, interval, period, max_retries):
        """Método 1: Usar yf.Ticker()"""
        
        for attempt in range(max_retries):
            try:
                # Cria sessão com headers
                session = requests.Session()
                session.headers.update(self.headers)
                
                # Cria ticker
                ticker = yf.Ticker(symbol, session=session)
                
                # Busca histórico
                df = ticker.history(
                    period=period,
                    interval=interval,
                    timeout=30,
                    raise_errors=False
                )
                
                if df is not None and not df.empty:
                    # Remove timezone
                    if df.index.tz is not None:
                        df.index = df.index.tz_localize(None)
                    return df
                
                # Se vazio, aguarda e tenta novamente
                if attempt < max_retries - 1:
                    wait = 2 ** attempt
                    time.sleep(wait)
            
            except Exception as e:
                if attempt < max_retries - 1:
                    wait = 2 ** attempt
                    time.sleep(wait)
                else:
                    pass
        
        return None
    
    def _fetch_with_download(self, symbol, interval, period):
        """Método 2: Usar yf.download() (mais robusto)"""
        
        try:
            df = yf.download(
                tickers=symbol,
                period=period,
                interval=interval,
                progress=False,
                show_errors=False,
                timeout=30
            )
            
            if df is None or df.empty:
                return None
            
            # Se MultiIndex (quando baixa múltiplos tickers)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
            
            # Remove timezone
            if df.index.tz is not None:
                df.index = df.index.tz_localize(None)
            
            return df
        
        except Exception as e:
            return None
    
    def fetch_multiple_timeframes(self, symbol):
        """Busca dados em múltiplos timeframes"""
        
        print(f"\n{'='*60}")
        print(f"📈 ANALISANDO: {symbol}")
        print(f"{'='*60}")
        
        data = {}
        
        # M15 (primário) - MAIS IMPORTANTE
        print("\n⏰ Timeframe M15 (primário):")
        df_15m = self.fetch_ohlcv(symbol, interval='15m', period='5d')
        data['15m'] = df_15m
        
        if df_15m is None:
            print(f"\n❌ FALHA CRÍTICA: Não foi possível obter dados M15 para {symbol}")
            return {'15m': None, '1h': None, '4h': None}
        
        # H1 (secundário)
        print("\n⏰ Timeframe H1 (secundário):")
        df_1h = self.fetch_ohlcv(symbol, interval='1h', period='1mo', max_retries=2)
        data['1h'] = df_1h
        
        # H4/D1 (terciário)
        print("\n⏰ Timeframe D1 (terciário):")
        df_4h = self.fetch_ohlcv(symbol, interval='1d', period='3mo', max_retries=2)
        data['4h'] = df_4h
        
        # Resumo
        print(f"\n{'='*60}")
        print(f"📊 RESUMO {symbol}:")
        print(f"  M15: {'✅ ' + str(len(df_15m)) + ' velas' if df_15m is not None else '❌ Sem dados'}")
        print(f"  H1:  {'✅ ' + str(len(df_1h)) + ' velas' if df_1h is not None else '⚠️  Sem dados'}")
        print(f"  D1:  {'✅ ' + str(len(df_4h)) + ' velas' if df_4h is not None else '⚠️  Sem dados'}")
        print(f"{'='*60}\n")
        
        return data
    
    def get_current_price(self, symbol):
        """Obtém preço atual"""
        df = self.fetch_ohlcv(symbol, interval='1m', period='1d')
        
        if df is not None and not df.empty:
            return df['Close'].iloc[-1]
        
        # Fallback: último preço do M15
        df = self.fetch_ohlcv(symbol, interval='15m', period='1d')
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
    
    def test_all_symbols(self, symbols):
        """Testa quais símbolos funcionam"""
        
        print("\n" + "="*60)
        print("🧪 TESTANDO TODOS OS SÍMBOLOS")
        print("="*60)
        
        working = []
        failing = []
        
        for symbol in symbols:
            print(f"\n📊 Testando: {symbol}")
            df = self.fetch_ohlcv(symbol, interval='1d', period='5d')
            
            if df is not None and not df.empty:
                working.append(symbol)
                print(f"✅ {symbol} FUNCIONA")
            else:
                failing.append(symbol)
                print(f"❌ {symbol} FALHOU")
        
        print("\n" + "="*60)
        print("📊 RESULTADOS:")
        print("="*60)
        print(f"\n✅ Funcionando ({len(working)}):")
        for s in working:
            print(f"  • {s}")
        
        print(f"\n❌ Falhando ({len(failing)}):")
        for s in failing:
            print(f"  • {s}")
        
        return working, failing


# TESTE
if __name__ == "__main__":
    import config
    
    fetcher = DataFetcher()
    
    # Testa todos os símbolos do config
    working, failing = fetcher.test_all_symbols(config.PAIRS)
    
    print(f"\n\n🎯 RECOMENDAÇÃO:")
    if len(working) >= 6:
        print(f"✅ {len(working)}/8 pares funcionando - SISTEMA VIÁVEL!")
    elif len(working) >= 4:
        print(f"⚠️ {len(working)}/8 pares funcionando - Considere usar apenas os que funcionam")
    else:
        print(f"❌ Apenas {len(working)}/8 pares - Use símbolos alternativos (crypto/commodities)")