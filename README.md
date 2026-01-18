📊 Customer Intelligence Platform (AI-Powered)

An end-to-end Machine Learning application that predicts customer churn risk using behavioral analytics, exposed via a production-ready REST API, and deployed with a modern frontend dashboard.

🔗 Live Application

Frontend (Vercel): https://customer-intelligence-platform.vercel.app

Backend API (Render): https://customer-intelligence-platform-1.onrender.com


🚀 Project Overview

Customer churn is a critical business problem in industries like e-commerce, fintech, and SaaS.
This project demonstrates how to:

Analyze customer transaction behavior

Engineer meaningful ML features (RFM)

Train and deploy a churn prediction model

Expose predictions via an API

Consume the API from a modern frontend UI

This is a real-world, production-style ML system, not just a notebook.


🧠 Machine Learning Approach
🔹 Feature Engineering (RFM Model)

Recency: Days since last transaction

Frequency: Number of purchases

Monetary: Total spending

🔹 Model

Logistic Regression (with StandardScaler)

Pipeline-based training

Model persisted using joblib

🔹 Target

Churn = 1 → No activity for more than 60 days

Churn = 0 → Active customer

🔹 Output

Churn prediction (Yes / No)

Churn probability

Risk level (Low / Medium / High)


🏗️ Tech Stack
Backend (ML API)

Python

FastAPI

scikit-learn

pandas / numpy

joblib

Uvicorn

Frontend

Next.js

React

Tailwind CSS

Deployment

Backend: Render

Frontend: Vercel

Version Control: Git & GitHub


📂 Project Structure
customer-intelligence-platform/
│
├── backend/
│   ├── main.py               # FastAPI application
│   ├── model/
│   │   ├── train_model.py    # ML training script
│   │   └── churn_model.pkl   # Trained model
│
├── data/
│   ├── customers.csv
│   └── transactions.csv
│
├── python/
│   └── customer_analysis.py  # Data analysis & feature engineering
│
├── frontend/
│   └── app/
│       └── page.jsx          # UI for churn prediction
│
├── sql/
│   └── advanced_analytics.sql
│
├── requirements.txt
└── README.md


🔌 API Usage
Health Check
GET /

Predict Churn
POST /predict


Request Body

{
  "recency_days": 90,
  "frequency": 1,
  "monetary": 1200
}


Response

{
  "churn_prediction": 1,
  "churn_probability": 0.92,
  "risk_level": "High"
}


🖥️ Frontend Features

Clean, responsive UI

Real-time predictions

Risk-level visualization

API integration with error handling


📈 Key Learnings & Takeaways

Built a complete ML lifecycle: data → model → API → UI → deployment

Applied business-driven feature engineering

Learned production deployment challenges

Integrated ML into a real web application

Designed APIs consumable by frontend systems


🔮 Future Improvements

Add customer segmentation (K-Means)

Store predictions in a database

Add authentication & user roles

Improve model with XGBoost / Random Forest

Add analytics dashboards & charts

Automate retraining pipeline


👤 Author

Navodita Bhatnagar
Aspiring Data Scientist | Machine Learning | Full-Stack ML Projects

🔗 GitHub: https://github.com/NavoditaBhatnagar

🔗 LinkedIn: (add your LinkedIn profile here)