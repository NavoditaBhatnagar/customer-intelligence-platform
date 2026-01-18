import pandas as pd

# -------------------------
# Load datasets
# -------------------------
customers = pd.read_csv("data/customers.csv")
transactions = pd.read_csv("data/transactions.csv")

print("Customers Data:")
print(customers.head(), "\n")

print("Transactions Data:")
print(transactions.head(), "\n")

# -------------------------
# Merge datasets
# -------------------------
customer_data = pd.merge(transactions, customers, on="customer_id")

print("Merged Dataset:")
print(customer_data.head(), "\n")

# -------------------------
# Business Analytics
# -------------------------

# Total revenue per customer
revenue_per_customer = (
    customer_data
    .groupby(["customer_id", "name"])["amount"]
    .sum()
    .reset_index()
    .sort_values(by="amount", ascending=False)
)

print("Total Revenue per Customer:")
print(revenue_per_customer, "\n")

# Average order value
aov = (
    customer_data
    .groupby(["customer_id", "name"])["amount"]
    .mean()
    .reset_index()
    .rename(columns={"amount": "avg_order_value"})
)

print("Average Order Value per Customer:")
print(aov, "\n")

# Payment method distribution
payment_analysis = (
    customer_data
    .groupby("payment_method")["amount"]
    .sum()
    .reset_index()
    .sort_values(by="amount", ascending=False)
)

print("Revenue by Payment Method:")
print(payment_analysis, "\n")

# -------------------------
# Feature Engineering (RFM)
# -------------------------

# Convert date columns
customer_data["transaction_date"] = pd.to_datetime(customer_data["transaction_date"])
customer_data["signup_date"] = pd.to_datetime(customer_data["signup_date"])

# Reference date (simulated "today")
reference_date = pd.to_datetime("2024-04-01")

# Create RFM features
rfm = (
    customer_data
    .groupby("customer_id")
    .agg({
        "transaction_date": lambda x: (reference_date - x.max()).days,  # Recency
        "transaction_id": "count",                                       # Frequency
        "amount": "sum"                                                   # Monetary
    })
    .reset_index()
)

rfm.columns = ["customer_id", "recency_days", "frequency", "monetary"]

print("RFM Features:")
print(rfm, "\n")

# Create churn label
# Business rule: recency > 60 days → churned
rfm["churn"] = rfm["recency_days"].apply(lambda x: 1 if x > 60 else 0)

print("RFM with Churn Label:")
print(rfm, "\n")

# -------------------------
# Machine Learning: Churn Prediction
# -------------------------

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Features and target
X = rfm[["recency_days", "frequency", "monetary"]]
y = rfm["churn"]

print("Feature Matrix (X):")
print(X, "\n")

print("Target Variable (y):")
print(y, "\n")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Initialize model
model = LogisticRegression()

# Train model
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("Model Accuracy:")
print(accuracy_score(y_test, y_pred), "\n")

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred), "\n")

print("Classification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    "feature": X.columns,
    "coefficient": model.coef_[0]
}).sort_values(by="coefficient", ascending=False)

print("Feature Importance:")
print(feature_importance)
