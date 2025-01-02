import os
import pickle
import numpy as np


# Load the trained model from the pickle file
model_path = os.path.join("models", "cancer_diagnosis_model.pkl")
with open(model_path, 'rb') as f:
    model = pickle.load(f)


def predict_cancerous(input_data):
    # Convert input data to a NumPy array and reshape if necessary
    input_data = np.array(input_data).reshape(1, -1)

    # Make predictions using the loaded model
    prediction = model.predict(input_data)

    # Return the prediction (0 = non-cancerous, 1 = cancerous)
    return prediction
