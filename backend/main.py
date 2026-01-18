from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------------------------
# Initialize FastAPI app
# -------------------------------------------------
app = FastAPI(
    title="Customer Churn Prediction API",
    description="API for predicting customer churn using a trained ML model",
    version="1.0.0"
)

# -------------------------------------------------
# CORS Configuration (Production-safe for demo apps)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Vercel + local)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS
    allow_headers=["*"],
)

# -------------------------------------------------
# Load trained ML model
# -------------------------------------------------
model = joblib.load("backend/model/churn_model.pkl")

# -------------------------------------------------
# Request schema
# -------------------------------------------------
class CustomerData(BaseModel):
    recency_days: int
    frequency: int
    monetary: float

# -------------------------------------------------
# Health check / root endpoint
# -------------------------------------------------
@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "Customer Churn Prediction API is live"
    }

# -------------------------------------------------
# Prediction endpoint
# -------------------------------------------------
@app.post("/predict")
def predict_churn(data: CustomerData):
    input_data = np.array([
        [data.recency_days, data.frequency, data.monetary]
    ])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    return {
        "churn_prediction": int(prediction),
        "churn_probability": round(float(probability), 3),
        "risk_level": (
            "High" if probability > 0.7
            else "Medium" if probability > 0.4
            else "Low"
        )
    }
