from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)  # allow frontend to call this API

# Load model and feature columns saved from Colab
model = joblib.load("yield_random_forest.pkl")
feature_columns = joblib.load("feature_columns.pkl")  # NOTE: .pkl, not .pk1

@app.route("/predict", methods=["POST"])
def predict():
    # Get JSON from frontend
    data = request.get_json()

    # Put JSON into a DataFrame (one row)
    df = pd.DataFrame([data])

    # Handle avg_temp missing
    if "avg_temp" in df.columns:
        df["avg_temp"] = df["avg_temp"].fillna(df["avg_temp"].mean())

    # One-hot encode Area and Item exactly like training
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