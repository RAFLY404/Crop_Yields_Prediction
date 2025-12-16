import os
import sys
import json
import joblib
import requests
import pandas as pd
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "Model")
os.makedirs(MODEL_DIR, exist_ok=True)

FILES = {
    "model": ("crop_yield_model.joblib", os.environ.get("MODEL_URL")),
    "encoders": ("encoders.joblib", os.environ.get("ENCODER_URL")),
    "columns": ("columns.joblib", os.environ.get("COLUMNS_URL")),
}

def download_file(filename, url):
    path = os.path.join(MODEL_DIR, filename)
    if os.path.exists(path):
        return path
    if not url:
        raise RuntimeError(f"URL not set for {filename}")
    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    return path

try:
    model_path = download_file(*FILES["model"])
    encoders_path = download_file(*FILES["encoders"])
    columns_path = download_file(*FILES["columns"])

    model = joblib.load(model_path)
    encoders = joblib.load(encoders_path)
    model_columns = joblib.load(columns_path)
except Exception as e:
    print(json.dumps({
        "error": "Failed to prepare model",
        "exception": str(e),
        "traceback": traceback.format_exc()
    }))
    sys.exit(1)

def predict_yield(data_dict):
    df = pd.DataFrame([data_dict])
    for col, encoder in encoders.items():
        if col in df.columns:
            df[col] = encoder.transform(df[col].astype(str))
        else:
            df[col] = 0
    df = df.reindex(columns=model_columns, fill_value=0)
    return float(model.predict(df)[0])

if __name__ == "__main__":
    try:
        data = json.loads(sys.stdin.read())
        result = predict_yield(data)
        print(json.dumps({"prediction": result}))
    except Exception as e:
        print(json.dumps({
            "error": "Prediction failed",
            "exception": str(e),
            "traceback": traceback.format_exc()
        }))
        sys.exit(1)
