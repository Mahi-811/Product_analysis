import pandas as pd
import matplotlib.pyplot as plt

# Load data
events = pd.read_csv("events.csv")

# Count unique users at each funnel stage
funnel = (
    events.groupby("event_name")["user_id"]
    .nunique()
    .reset_index()
)

# Force logical funnel order
order = [
    "app_open",
    "search",
    "add_to_cart",
    "purchase"
]

funnel["event_name"] = pd.Categorical(
    funnel["event_name"],
    categories=order,
    ordered=True
)

funnel = funnel.sort_values("event_name")

print(funnel)

# Save results
funnel.to_csv("funnel_metrics.csv", index=False)

# Plot
plt.figure(figsize=(8, 5))
plt.plot(
    funnel["event_name"],
    funnel["user_id"],
    marker="o"
)

plt.title("User Funnel")
plt.xlabel("Stage")
plt.ylabel("Users")
plt.grid(True)

plt.show()