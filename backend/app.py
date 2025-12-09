from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import zipfile
import os

MODEL_ZIP = "yield_random_forest.pkl.zip"
MODEL_FILE = "yield_random_forest.pkl"
FEATURES_FILE = "feature_columns.pkl"

# Unzip model if not extracted
if not os.path.exists(MODEL_FILE) and os.path.exists(MODEL_ZIP):
    with zipfile.ZipFile(MODEL_ZIP, "r") as zip_ref:
        zip_ref.extractall("./")

app = Flask(__name__)
CORS(app)

# Load model and feature columns
model = joblib.load(MODEL_FILE)
feature_columns = joblib.load(FEATURES_FILE)

# Discretization helper
def discretize(df):
    # Yield category
    if df['hg/ha_yield'].nunique() > 1:
        df['yield_category'] = pd.qcut(
            df['hg/ha_yield'], q=4,
            labels=['Low', 'Medium', 'High', 'Very High'],
            duplicates='drop'
        )
    else:
        df['yield_category'] = 'Medium'

    # Temperature category
    temp_bins = [0, 10, 20, 25, 50]
    temp_labels = ['Cold', 'Moderate', 'Warm', 'Hot']
    df['temp_category'] = pd.cut(
        df['avg_temp'],
        bins=temp_bins,
        labels=temp_labels,
        include_lowest=True
    )

    # Rainfall category
    rainfall_bins = [0, 500, 1000, 1500, 5000]
    rainfall_labels = ['Low', 'Moderate', 'High', 'Very High']
    df['rainfall_category'] = pd.cut(
        df['average_rain_fall_mm_per_year'],
        bins=rainfall_bins,
        labels=rainfall_labels,
        include_lowest=True
    )

    # Pesticides category
    if df['pesticides_tonnes'].nunique() > 1:
        df['pesticides_category'] = pd.qcut(
            df['pesticides_tonnes'], q=3,
            labels=['Low', 'Medium', 'High'],
            duplicates='drop'
        )
    else:
        df['pesticides_category'] = 'Medium'

    return df

@app.route("/predict", methods=["POST"])
def predict():
    # Parse JSON input
    data = request.get_json()
    df = pd.DataFrame([data])

    # Fill missing numeric values
    for col in ['avg_temp', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'hg/ha_yield']:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean() if not df[col].isna().all() else 0)
        else:
            df[col] = 0  # if missing entirely

    # Apply discretization
    df = discretize(df)

    # One-hot encode without dropping first
    df = pd.get_dummies(
        df,
        columns=['Area', 'Item', 'yield_category', 'temp_category', 'rainfall_category', 'pesticides_category'],
        drop_first=False
    )

    # Reindex to match training features (missing columns filled with 0)
    df = df.reindex(columns=feature_columns, fill_value=0)

    # Debug
    # Print the one-hot encoded row before prediction
    print(df[feature_columns].iloc[0])

    # Predict
    prediction = model.predict(df)[0]

    return jsonify({"predicted_yield": float(prediction)})

@app.route("/", methods=["GET"])
def home():
    return {"message": "Crop Yield Random Forest API is running 👋"}

if __name__ == "__main__":
    app.run(debug=True)
