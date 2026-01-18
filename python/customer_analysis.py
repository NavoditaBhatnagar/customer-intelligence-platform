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

customer_data["transaction_date"] = pd.to_datetime(customer_data["transaction_date"])
customer_data["signup_date"] = pd.to_datetime(customer_data["signup_date"])

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

print("RFM Features:")
print(rfm, "\n")

rfm["churn"] = rfm["recency_days"].apply(lambda x: 1 if x > 60 else 0)

print("RFM with Churn Label:")
print(rfm, "\n")

# =====================================================
# IMPROVED MACHINE LEARNING (STEP 1)
# =====================================================

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

X = rfm[["recency_days", "frequency", "monetary"]]
y = rfm["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(class_weight="balanced", random_state=42))
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

print("Improved Model Accuracy:")
print(accuracy_score(y_test, y_pred), "\n")

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred), "\n")

print("Classification Report:")
print(classification_report(y_test, y_pred))

cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="accuracy")
print("Cross-Validation Scores:", cv_scores)
print("Mean CV Accuracy:", cv_scores.mean(), "\n")

coefficients = pipeline.named_steps["model"].coef_[0]

feature_importance = pd.DataFrame({
    "feature": X.columns,
    "coefficient": coefficients
}).sort_values(by="coefficient", ascending=False)

print("Feature Importance (Improved Model):")
print(feature_importance, "\n")

# =====================================================
# STEP 2: VISUALIZATIONS (EDA + CHURN INSIGHTS)
# =====================================================

import matplotlib.pyplot as plt

# 1. Churn distribution
plt.figure()
rfm["churn"].value_counts().plot(kind="bar")
plt.title("Churn Distribution")
plt.xlabel("Churn (0 = Active, 1 = Churned)")
plt.ylabel("Number of Customers")
plt.show()

# 2. Recency vs Monetary by churn
plt.figure()
for churn_value in [0, 1]:
    subset = rfm[rfm["churn"] == churn_value]
    plt.scatter(subset["recency_days"], subset["monetary"], label=f"Churn = {churn_value}")
plt.xlabel("Recency (Days)")
plt.ylabel("Total Monetary Value")
plt.title("Recency vs Monetary by Churn")
plt.legend()
plt.show()

# 3. Monetary value distribution by churn
plt.figure()
rfm.boxplot(column="monetary", by="churn")
plt.title("Customer Monetary Value by Churn")
plt.suptitle("")
plt.xlabel("Churn (0 = Active, 1 = Churned)")
plt.ylabel("Total Spend")
plt.show()

# 4. Feature importance visualization
plt.figure()
plt.bar(feature_importance["feature"], feature_importance["coefficient"])
plt.title("Feature Importance (Logistic Regression)")
plt.xlabel("Feature")
plt.ylabel("Coefficient Value")
plt.show()
