import pandas as pd
import numpy as np

np.random.seed(42)

# -----------------------------
# CONFIG
# -----------------------------
NUM_USERS = 10000

COUNTRIES = ["India", "USA", "UK", "Canada", "Germany"]

CHANNELS = [
    "Google Ads",
    "Facebook",
    "Organic",
    "Referral"
]

# -----------------------------
# USERS
# -----------------------------
signup_dates = np.random.choice(
    pd.date_range("2025-01-01", "2025-12-31"),
    NUM_USERS
)

users = pd.DataFrame({
    "user_id": range(1, NUM_USERS + 1),
    "signup_date": signup_dates,
    "country": np.random.choice(COUNTRIES, NUM_USERS),
    "acquisition_channel": np.random.choice(
        CHANNELS,
        NUM_USERS,
        p=[0.3, 0.25, 0.3, 0.15]
    )
})

users.to_csv("users.csv", index=False)

# -----------------------------
# SESSIONS
# -----------------------------
sessions = []
session_id = 1

for user in users.itertuples():

    num_sessions = np.random.randint(1, 11)

    for _ in range(num_sessions):

        days_after_signup = np.random.randint(0, 180)

        session_date = (
            pd.Timestamp(user.signup_date)
            + pd.Timedelta(days=int(days_after_signup))
            + pd.Timedelta(hours=np.random.randint(0, 24))
        )

        sessions.append([
            session_id,
            user.user_id,
            session_date,
            np.random.choice(
                ["Mobile", "Desktop", "Tablet"],
                p=[0.70, 0.25, 0.05]
            )
        ])

        session_id += 1

sessions_df = pd.DataFrame(
    sessions,
    columns=[
        "session_id",
        "user_id",
        "session_date",
        "device_type"
    ]
)

sessions_df.to_csv("sessions.csv", index=False)

# -----------------------------
# EVENTS
# -----------------------------
events = []
event_id = 1

for user in users.itertuples():

    signup_date = pd.Timestamp(user.signup_date)

    # Every user opens app
    event_time = signup_date + pd.Timedelta(
        days=np.random.randint(0, 7)
    )

    events.append([
        event_id,
        user.user_id,
        "app_open",
        event_time
    ])
    event_id += 1

    # 70% search
    if np.random.random() < 0.70:

        event_time += pd.Timedelta(
            hours=np.random.randint(1, 48)
        )

        events.append([
            event_id,
            user.user_id,
            "search",
            event_time
        ])
        event_id += 1

        # 50% of searchers add to cart
        if np.random.random() < 0.50:

            event_time += pd.Timedelta(
                hours=np.random.randint(1, 24)
            )

            events.append([
                event_id,
                user.user_id,
                "add_to_cart",
                event_time
            ])
            event_id += 1

            # 40% of add_to_cart purchase
            if np.random.random() < 0.40:

                event_time += pd.Timedelta(
                    hours=np.random.randint(1, 24)
                )

                events.append([
                    event_id,
                    user.user_id,
                    "purchase",
                    event_time
                ])
                event_id += 1

    # Retention events
    retention_probs = {
        1: 0.45,
        2: 0.30,
        3: 0.20,
        4: 0.15,
        5: 0.10
    }

    for month, prob in retention_probs.items():

        if np.random.random() < prob:

            retained_event = (
                signup_date
                + pd.DateOffset(months=month)
                + pd.Timedelta(
                    days=np.random.randint(0, 28)
                )
            )

            events.append([
                event_id,
                user.user_id,
                "app_open",
                retained_event
            ])
            event_id += 1

events_df = pd.DataFrame(
    events,
    columns=[
        "event_id",
        "user_id",
        "event_name",
        "event_time"
    ]
)

events_df.to_csv("events.csv", index=False)

# -----------------------------
# ORDERS
# -----------------------------
orders = []
order_id = 1

purchase_users = events_df[
    events_df["event_name"] == "purchase"
]

for row in purchase_users.itertuples():

    revenue = round(
        np.random.uniform(200, 5000),
        2
    )

    orders.append([
        order_id,
        row.user_id,
        row.event_time,
        revenue
    ])

    order_id += 1

orders_df = pd.DataFrame(
    orders,
    columns=[
        "order_id",
        "user_id",
        "order_date",
        "revenue"
    ]
)

orders_df.to_csv("orders.csv", index=False)

print("Generated:")
print("users.csv")
print("sessions.csv")
print("events.csv")
print("orders.csv")
print()
print(f"Users: {len(users_df) if 'users_df' in globals() else len(users)}")
print(f"Sessions: {len(sessions_df)}")
print(f"Events: {len(events_df)}")
print(f"Orders: {len(orders_df)}")
