import joblib

try:
    model = joblib.load("ml_model.pkl")
except:
    model = None

def ml_filter_signal(df, signal):
    if model is None:
        return True, 50.0
    try:
        features = df[['EMA9','EMA21','RSI','MACD','ATR']].iloc[-1:].values
        prob = model.predict_proba(features)[0][1]
        if signal == "BUY":
            return prob > 0.6, round(prob*100, 1)
        elif signal == "SELL":
            return (1 - prob) > 0.6, round((1-prob)*100, 1)
        else:
            return False, round(prob*100, 1)
    except:
        return True, 50.0
