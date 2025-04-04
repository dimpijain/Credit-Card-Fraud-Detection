import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

app = Flask(__name__)

# Load the trained fraud detection model
try:
    model = joblib.load("fraud_detection_model.pkl")
    print("✅ Fraud detection model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading fraud detection model: {e}")

# Load the pre-trained PCA model
try:
    pca = joblib.load("pca_model.pkl")
    print("✅ PCA model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading PCA model: {e}")

# Load the standard scaler (used before PCA)
try:
    scaler = joblib.load("scaler.pkl")
    print("✅ Scaler loaded successfully!")
except Exception as e:
    print(f"❌ Error loading scaler: {e}")

# Mapping for transaction type
transaction_type_mapping = {
    "Online": 0,
    "POS": 1,
    "ATM": 2
}

# Mapping for location (example)
location_mapping = {
    "USA": 0,
    "UK": 1,
    "India": 2,
    "Germany": 3,
    "Australia": 4
}

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        
        # Extract user input
        amount = float(data.get("Amount", 0))
        transaction_type = data.get("TransactionType", "")
        location = data.get("Location", "")
        time_of_day = int(data.get("TimeOfDay", -1))  # 0-23 (hour of transaction)

        # Validate input values
        if amount <= 0:
            return jsonify({"error": "Invalid transaction amount"}), 400
        if time_of_day < 0 or time_of_day > 23:
            return jsonify({"error": "Invalid time of day (should be between 0-23)"}), 400

        # Encode categorical data
        transaction_type_value = transaction_type_mapping.get(transaction_type, -1)
        location_value = location_mapping.get(location, -1)

        if transaction_type_value == -1 or location_value == -1:
            return jsonify({"error": "Invalid transaction type or location"}), 400

        # Create feature array
        features = np.array([[amount, transaction_type_value, location_value, time_of_day]])

        # Apply scaling (same scaling used during training)
        scaled_features = scaler.transform(features)

        # Apply PCA transformation
        pca_features = pca.transform(scaled_features)

        # Predict fraud
        prediction = model.predict(pca_features)

        # Return the result
        result = {"fraud": int(prediction[0])}  # Convert NumPy int to Python int
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
