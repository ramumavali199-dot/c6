import requests
import pandas as pd

def fetch_ohlc_bybit(symbol="BTCUSDT", interval="60", limit=100):
    try:
        url = "https://api.bybit.com/v5/market/kline"
        params = {"category": "spot", "symbol": symbol, "interval": interval, "limit": limit}
        resp = requests.get(url, params=params, timeout=10).json()
        if resp.get("retCode") == 0:
            candles = resp.get("result", {}).get("list", [])
            if candles:
                df = pd.DataFrame(candles, columns=['timestamp','open','high','low','close','volume','turnover'])
                df[['open','high','low','close','volume']] = df[['open','high','low','close','volume']].astype(float)
                df = df.sort_values('timestamp').reset_index(drop=True)
                return df
    except Exception as e:
        print("Bybit fetch error:", e)
    return pd.DataFrame()
