from flask import Flask, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = jotlib.load('yield_model.pk1')
feature_columns = joblib.load('feature_columns.pk1')

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data])
    df = pd.get_dummies(df, columns=['Area', 'Item'], drop_first = True)
    df = df.reindex(columns=feature_columns, fill_value=0)
    prediction = model.predict(df)[0]
    return jsonify({"predicted_yield": prediction})
if __name__ == "__main__":
    app.run(debug=True)