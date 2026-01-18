import pandas as pd

# Load datasets
customers = pd.read_csv("data/customers.csv")
transactions = pd.read_csv("data/transactions.csv")

print("Customers Data:")
print(customers.head(), "\n")

print("Transactions Data:")
print(transactions.head(), "\n")

# Merge datasets
customer_data = pd.merge(transactions, customers, on="customer_id")

print("Merged Dataset:")
print(customer_data.head(), "\n")

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
print(payment_analysis)
