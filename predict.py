import os
import sys
import json
import joblib
import requests
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "Model")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "crop_yield_model.joblib")
ENCODER_PATH = os.path.join(MODEL_DIR, "encoders.joblib")
COLUMNS_PATH = os.path.join(MODEL_DIR, "columns.joblib")

MODEL_URL = os.environ.get("MODEL_URL")
ENCODER_URL = os.environ.get("ENCODER_URL")
COLUMNS_URL = os.environ.get("COLUMNS_URL")

_model = None
_encoders = None
_columns = None

def download(path, url):
    if os.path.exists(path):
        return
    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()
    with open(path, "wb") as f:
        for c in r.iter_content(8192):
            f.write(c)

def load_model():
    global _model, _encoders, _columns

    if _model is not None:
        return

    download(MODEL_PATH, MODEL_URL)
    download(ENCODER_PATH, ENCODER_URL)
    download(COLUMNS_PATH, COLUMNS_URL)

    _model = joblib.load(MODEL_PATH)
    _encoders = joblib.load(ENCODER_PATH)
    _columns = joblib.load(COLUMNS_PATH)

def predict(data):
    load_model()
    df = pd.DataFrame([data])
    for col, enc in _encoders.items():
        if col in df:
            df[col] = enc.transform(df[col].astype(str))
        else:
            df[col] = 0
    df = df.reindex(columns=_columns, fill_value=0)
    return float(_model.predict(df)[0])

if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    result = predict(data)
    print(json.dumps({"prediction": result}))
