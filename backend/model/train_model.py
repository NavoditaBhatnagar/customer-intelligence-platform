import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load data
customers = pd.read_csv("data/customers.csv")
transactions = pd.read_csv("data/transactions.csv")

# Merge
customer_data = pd.merge(transactions, customers, on="customer_id")

# Feature engineering
customer_data["transaction_date"] = pd.to_datetime(customer_data["transaction_date"])
reference_date = pd.to_datetime("2024-04-01")

rfm = (
    customer_data
    .groupby("customer_id")
    .agg({
        "transaction_date": lambda x: (reference_date - x.max()).days,
        "transaction_id": "count",
        "amount": "sum"
    })
    .reset_index()
)

rfm.columns = ["customer_id", "recency_days", "frequency", "monetary"]

rfm["churn"] = rfm["recency_days"].apply(lambda x: 1 if x > 60 else 0)

# Features / target
X = rfm[["recency_days", "frequency", "monetary"]]
y = rfm["churn"]

# Train-test split
X_train, _, y_train, _ = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(class_weight="balanced", random_state=42))
])

# Train
pipeline.fit(X_train, y_train)

# Save model
joblib.dump(pipeline, "backend/model/churn_model.pkl")

print("✅ Model trained and saved as churn_model.pkl")
