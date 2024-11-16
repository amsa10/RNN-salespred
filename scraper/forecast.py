import pickle
import pandas as pd

def load_model(model_path="models/sales_model.pkl"):
    """Load the pre-trained sales prediction model."""
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def predict_sales(data):
    """Predict sales using the pre-trained model."""
    model = load_model()
    predictions = model.predict(data[['sales']])  # Assuming 'sales' is a feature used for forecasting
    data['predicted_sales'] = predictions
    return data
