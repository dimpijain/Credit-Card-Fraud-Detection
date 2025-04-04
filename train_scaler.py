import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the dataset
df = pd.read_csv("creditcard.csv")

# Selecting features to scale (excluding label 'Class')
features = df.drop(columns=["Class"])  # Assuming "Class" is the fraud label
scaler = StandardScaler()

# Fit the scaler on the data
scaler.fit(features)

# Save the trained scaler
joblib.dump(scaler, "scaler.pkl")
print("Scaler model saved as scaler.pkl")

