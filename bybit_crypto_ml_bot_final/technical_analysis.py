import pandas as pd
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df['EMA9'] = EMAIndicator(df['close'], window=9).ema_indicator()
    df['EMA21'] = EMAIndicator(df['close'], window=21).ema_indicator()
    df['RSI'] = RSIIndicator(df['close'], window=14).rsi()
    macd = MACD(df['close'])
    df['MACD'] = macd.macd()
    df['MACD_SIGNAL'] = macd.macd_signal()
    atr = AverageTrueRange(df['high'], df['low'], df['close'], window=14)
    df['ATR'] = atr.average_true_range()
    return df

def generate_signal(df: pd.DataFrame):
    signal, reason = "HOLD", "No clear setup"
    if df['EMA9'].iloc[-1] > df['EMA21'].iloc[-1] and df['RSI'].iloc[-1] > 50:
        signal, reason = "BUY", "EMA9 > EMA21 and RSI > 50"
    elif df['EMA9'].iloc[-1] < df['EMA21'].iloc[-1] and df['RSI'].iloc[-1] < 50:
        signal, reason = "SELL", "EMA9 < EMA21 and RSI < 50"
    return signal, reason
