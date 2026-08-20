import pandas as pd

# Load data
users = pd.read_csv("users.csv")
orders = pd.read_csv("orders.csv")

orders["order_date"] = pd.to_datetime(orders["order_date"])

# Revenue by Month
monthly_revenue = (
    orders.groupby(
        orders["order_date"].dt.to_period("M")
    )["revenue"]
    .sum()
    .reset_index()
)

monthly_revenue.to_csv(
    "monthly_revenue.csv",
    index=False
)

# Revenue by Channel
channel_revenue = (
    orders.merge(users, on="user_id")
    .groupby("acquisition_channel")["revenue"]
    .sum()
    .reset_index()
)

channel_revenue.to_csv(
    "channel_revenue.csv",
    index=False
)

# Revenue by Country
country_revenue = (
    orders.merge(users, on="user_id")
    .groupby("country")["revenue"]
    .sum()
    .reset_index()
)

country_revenue.to_csv(
    "country_revenue.csv",
    index=False
)

# Top Customers
top_customers = (
    orders.groupby("user_id")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_customers.to_csv(
    "top_customers.csv",
    index=False
)

# KPI Summary
total_users = users["user_id"].nunique()
total_revenue = orders["revenue"].sum()
total_orders = len(orders)
purchasers = orders["user_id"].nunique()

conversion_rate = (
    purchasers / total_users * 100
)

arpu = (
    total_revenue / total_users
)

kpi_summary = pd.DataFrame({
    "Metric": [
        "Total Users",
        "Total Revenue",
        "Total Orders",
        "Conversion Rate",
        "ARPU"
    ],
    "Value": [
        total_users,
        total_revenue,
        total_orders,
        conversion_rate,
        arpu
    ]
})

kpi_summary.to_csv(
    "kpi_summary.csv",
    index=False
)

print("Revenue analysis complete.")
