from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import zipfile
import os

MODEL_ZIP = "yield_random_forest.pkl.zip"
MODEL_FILE = "yield_random_forest.pkl"

# Unzip model if not extracted yet
if not os.path.exists(MODEL_FILE) and os.path.exists(MODEL_ZIP):
    with zipfile.ZipFile(MODEL_ZIP, "r") as zip_ref:
        zip_ref.extractall("./")

app = Flask(__name__)
CORS(app) #frontend to call backend

# Load model and feature columns from Colab
model = joblib.load(MODEL_FILE)
feature_columns = joblib.load("feature_columns.pkl") 

@app.route("/predict", methods=["POST"])
def predict():
    # Get JSON from frontend
    data = request.get_json()

    # Put JSON into DataFrame
    df = pd.DataFrame([data])

    # Handle avg_temp missing
    if "avg_temp" in df.columns:
        df["avg_temp"] = df["avg_temp"].fillna(df["avg_temp"].mean())

    
    df = pd.get_dummies(df, columns=["Area", "Item"], drop_first=True)

    # Reindex to match training feature columns
    df = df.reindex(columns=feature_columns, fill_value=0)

    # Predict
    prediction = model.predict(df)[0]

    return jsonify({"predicted_yield": float(prediction)})


@app.route("/", methods=["GET"])
def home():
    return {"message": "Crop Yield Random Forest API is running 👋"}


if __name__ == "__main__":
    app.run(debug=True)