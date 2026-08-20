import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
users = pd.read_csv("users.csv")
events = pd.read_csv("events.csv")

# Convert dates
users["signup_date"] = pd.to_datetime(users["signup_date"])
events["event_time"] = pd.to_datetime(events["event_time"])

# Create cohort and activity months
users["cohort_month"] = users["signup_date"].dt.to_period("M")
events["activity_month"] = events["event_time"].dt.to_period("M")

# Merge
df = events.merge(
    users[["user_id", "cohort_month"]],
    on="user_id"
)

# Month number
df["month_number"] = (
    df["activity_month"] -
    df["cohort_month"]
).apply(lambda x: x.n)

# Cohort table
cohort = (
    df.groupby(
        ["cohort_month", "month_number"]
    )["user_id"]
    .nunique()
    .reset_index()
)

# Pivot
cohort_table = cohort.pivot(
    index="cohort_month",
    columns="month_number",
    values="user_id"
)

# Retention %
retention = (
    cohort_table.divide(
        cohort_table[0],
        axis=0
    ) * 100
)

# Save output
retention.to_csv("retention_matrix.csv")

# Heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(
    retention,
    annot=True,
    fmt=".1f"
)

plt.title("Cohort Retention Analysis")
plt.show()
