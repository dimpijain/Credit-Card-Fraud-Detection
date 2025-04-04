import joblib
from sklearn.decomposition import PCA
import numpy as np

# Example: Train a PCA model (Assuming you have scaled features)
# Generate some random example data for PCA training (Replace this with actual data)
X_train_scaled = np.random.rand(100, 4)  # 100 samples, 4 features

# Initialize and fit PCA (Assuming 2 principal components)
pca = PCA(n_components=2)
pca.fit(X_train_scaled)

# Save the trained PCA model
joblib.dump(pca, "pca_model.pkl")

print("✅ PCA model saved successfully!")
