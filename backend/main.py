from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# Initialize app
app = FastAPI(title="Customer Churn Prediction API")

# -------------------------
# CORS Configuration
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow POST, OPTIONS, etc.
    allow_headers=["*"],
)

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
    input_data = np.array([[data.recency_days, data.frequency, data.monetary]])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    return {
        "churn_prediction": int(prediction),
        "churn_probability": round(float(probability), 3)
    }
