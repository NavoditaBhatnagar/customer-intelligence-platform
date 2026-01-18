
-- Advanced SQL Analytics Queries
-- Author: Navodita Bhatnagar

-- 1. Customer Revenue
SELECT 
    c.customer_id,
    c.city,
    SUM(p.price * t.quantity) AS total_revenue
FROM dbo.transactions t
JOIN dbo.customers c ON t.customer_id = c.customer_id
JOIN dbo.products p ON t.product_id = p.product_id
GROUP BY c.customer_id, c.city
ORDER BY total_revenue DESC;

-- 2. Rank Customers by Revenue
SELECT
    c.customer_id,
    SUM(p.price * t.quantity) AS total_revenue,
    RANK() OVER (ORDER BY SUM(p.price * t.quantity) DESC) AS revenue_rank
FROM dbo.transactions t
JOIN dbo.customers c ON t.customer_id = c.customer_id
JOIN dbo.products p ON t.product_id = p.product_id
GROUP BY c.customer_id;

-- 3. Monthly Revenue Trend
SELECT
    FORMAT(transaction_date, 'yyyy-MM') AS month,
    SUM(p.price * t.quantity) AS revenue
FROM dbo.transactions t
JOIN dbo.products p ON t.product_id = p.product_id
GROUP BY FORMAT(transaction_date, 'yyyy-MM')
ORDER BY month;

-- 4. Churn-Prone Customers
SELECT
    c.customer_id,
    COUNT(t.transaction_id) AS txn_count
FROM dbo.customers c
LEFT JOIN dbo.transactions t 
    ON c.customer_id = t.customer_id
GROUP BY c.customer_id
HAVING COUNT(t.transaction_id) < 2;




-- Total revenue and number of transactions per customer
SELECT 
    c.customer_id,
    c.name,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_revenue
FROM customers c
JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_revenue DESC;


-- Identify high-value customers
SELECT 
    c.customer_id,
    c.name,
    SUM(t.amount) AS total_revenue
FROM customers c
JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY c.customer_id, c.name
HAVING SUM(t.amount) > 2000;


-- Customer recency (days since last transaction)
SELECT
    c.customer_id,
    c.name,
    MAX(t.transaction_date) AS last_purchase_date
FROM customers c
JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY c.customer_id, c.name;


-- Average order value per customer
SELECT
    c.customer_id,
    c.name,
    AVG(t.amount) AS avg_order_value
FROM customers c
JOIN transactions t
    ON c.customer_id = t.customer_id
GROUP BY c.customer_id, c.name;


-- Revenue by payment method
SELECT
    payment_method,
    SUM(amount) AS total_revenue
FROM transactions
GROUP BY payment_method
ORDER BY total_revenue DESC;

