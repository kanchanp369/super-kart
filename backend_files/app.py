# Flask backend: serves online and batch sales predictions
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

superkart_api = Flask("SuperKart Sales Predictor")

# load the serialized pipeline (preprocessing + model)
model = joblib.load("superkart_model.joblib")

FEATURES = ["Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area", "Product_MRP",
            "Store_Size", "Store_Location_City_Type", "Store_Type", "Product_Id_char",
            "Store_Age_Years", "Product_Type_Category"]


@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart Sales Prediction API!"


@superkart_api.post("/v1/predict")
def predict_sales():
    """Single (online) prediction from a JSON payload."""
    payload = request.get_json()
    sample = pd.DataFrame([{f: payload[f] for f in FEATURES}])
    prediction = float(np.round(model.predict(sample)[0], 2))
    return jsonify({"Predicted_Sales_Total": prediction})


@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    """Batch prediction from an uploaded CSV file."""
    file = request.files["file"]
    batch = pd.read_csv(file)[FEATURES]
    predictions = np.round(model.predict(batch), 2).tolist()
    return jsonify({str(i): p for i, p in zip(batch.index, predictions)})


if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860, debug=False)
