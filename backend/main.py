from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Initialize app
app = FastAPI(title="Customer Churn Prediction API")

# Load trained model
model = joblib.load("backend/model/churn_model.pkl")

# Input schema
class CustomerData(BaseModel):
    recency_days: int
    frequency: int
    monetary: float

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Churn Prediction API is running"}

# Prediction endpoint
@app.post("/predict")
def predict_churn(data: CustomerData):
    # Prepare input for model
    input_data = np.array([[data.recency_days, data.frequency, data.monetary]])

    # Prediction
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    return {
        "churn_prediction": int(prediction),
        "churn_probability": round(float(probability), 3)
    }
