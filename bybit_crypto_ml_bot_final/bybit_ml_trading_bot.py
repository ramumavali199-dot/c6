import time
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from technical_analysis import calculate_indicators, generate_signal
from alerts.telegram_bot import send_alert
from ml_models import ml_filter_signal
from data_fetch.bybit_data import fetch_ohlc_bybit

SYMBOLS = ["BTCUSDT", "ETHUSDT"]

def run_bot():
    send_alert("🚀 Bybit ML Bot Started Successfully!")
    while True:
        try:
            for sym in SYMBOLS:
                df = fetch_ohlc_bybit(sym, interval="60", limit=200)
                if df.empty:
                    continue
                df = calculate_indicators(df)

                signal, reason = generate_signal(df)
                passed, conf = ml_filter_signal(df, signal)

                if signal != "HOLD" and passed:
                    price = df["close"].iloc[-1]
                    msg = f"""
📊 <b>{sym}</b>
Signal: {signal} ✅ ({conf}% confidence)
Price: {price}
Reason: {reason}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                    """.strip()
                    send_alert(msg)

            time.sleep(300)
        except Exception as e:
            send_alert(f"⚠️ Bot Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_bot()
