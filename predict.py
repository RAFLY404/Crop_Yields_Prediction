import sys
import json
import pandas as pd
import joblib

# Load model components
model = joblib.load("Model/crop_yield_model.joblib")
encoders = joblib.load("Model/encoders.joblib")
model_columns = joblib.load("Model/columns.joblib")

def predict_yield(data_dict):
    df = pd.DataFrame([data_dict])

    # Encode categorical columns
    for col, encoder in encoders.items():
        df[col] = encoder.transform(df[col].astype(str))

    # Align column order
    df = df.reindex(columns=model_columns, fill_value=0)

    # Predict
    pred = model.predict(df)[0]
    return float(pred)

if __name__ == "__main__":
    # Receive JSON input from Node.js
    input_json = sys.stdin.read()
    data = json.loads(input_json)

    result = predict_yield(data)

    print(json.dumps({"prediction": result}))
