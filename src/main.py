import json
import yaml
import pandas as pd
from pathlib import Path
from telegram import Bot
from telegram.constants import ParseMode
from .data_sources import fetch_yf_history, fetch_alpha_fx, last_price
from .macro import get_macro_snapshot
from .tech import tech_snapshot
from .flow import flow_snapshot
from .vti import vti_validate
from .formatter import render_report
from .utils import now_utc_iso, get_env

def load_config():
    cfg = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))
    pairs_map = json.loads(Path("pairs.json").read_text(encoding="utf-8"))
    return cfg, pairs_map

def fetch_prices(pair_key: str, ticker: str, cfg):
    df = fetch_yf_history(ticker, interval="15m", lookback_days=5)
    if df is None:
        api_key = get_env("ALPHA_VANTAGE_API_KEY")
        if api_key and pair_key != "BTCUSD" and pair_key != "XAUUSD":
            df = fetch_alpha_fx(pair_key, api_key, interval="15min")
    if df is None or df.empty:
        raise RuntimeError(f"Falha ao obter dados para {pair_key}")
    return df

def send_to_telegram(text: str):
    token = get_env("TELEGRAM_BOT_TOKEN")
    chat_id = get_env("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Telegram desabilitado ou secrets ausentes.")
        return
    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN)

def run_once():
    utc = now_utc_iso()
    cfg, pairs_map = load_config()
    pairs = cfg.get("pairs", [])
    for p in pairs:
        try:
            ticker = pairs_map[p]
            df = fetch_prices(p, ticker, cfg)
            price = last_price(df)
            macro = get_macro_snapshot(utc)
            tech = tech_snapshot(df)
            flow = flow_snapshot(df)
            vti = vti_validate(macro, tech, flow)
            report = render_report(p, utc, price, macro, tech, flow, vti, cfg)
            send_to_telegram(report)
            print(f"Enviado: {p} @ {utc}")
        except Exception as e:
            send_to_telegram(f"*Oracle-Trading-Systems*\nFalha em {p}: {str(e)}")
            print(f"Erro {p}: {e}")

if __name__ == "__main__":
    run_once()
