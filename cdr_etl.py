import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# =========================
# 1. Load Raw Data
# =========================
df = pd.read_csv("raw/CDR-Call-Details.csv")

print("Raw Data Sample:")
print(df.head())

# =========================
# 2. Transform into Dimensions
# =========================

# --- dim_customer ---
dim_customer = df[["Phone Number", "Account Length", "VMail Message"]].copy()
dim_customer = dim_customer.drop_duplicates().reset_index(drop=True)
dim_customer = dim_customer.rename(
    columns={
        "Phone Number": "phone_number",
        "Account Length": "account_length",
        "VMail Message": "vmail_message",
    }
)
dim_customer["customer_id"] = dim_customer.index + 1  # surrogate key

# --- dim_time (just snapshot) ---
snapshot_date = datetime.today().date()
dim_time = pd.DataFrame(
    {
        "time_id": [1],
        "snapshot_date": [snapshot_date],
        "year": [snapshot_date.year],
        "month": [snapshot_date.month],
        "day": [snapshot_date.day],
        "weekday": [snapshot_date.strftime("%A")],
    }
)

# --- fact_usage ---
fact_usage = df.copy()
fact_usage = fact_usage.rename(
    columns={
        "Day Mins": "day_mins",
        "Day Calls": "day_calls",
        "Day Charge": "day_charge",
        "Eve Mins": "eve_mins",
        "Eve Calls": "eve_calls",
        "Eve Charge": "eve_charge",
        "Night Mins": "night_mins",
        "Night Calls": "night_calls",
        "Night Charge": "night_charge",
        "Intl Mins": "intl_mins",
        "Intl Calls": "intl_calls",
        "Intl Charge": "intl_charge",
        "CustServ Calls": "custserv_calls",
        "Churn": "churn_flag",
    }
)

# Map customers (foreign key)
fact_usage = fact_usage.merge(
    dim_customer[["customer_id", "phone_number"]],
    left_on="Phone Number",
    right_on="phone_number",
    how="left"
)

fact_usage["time_id"] = 1  # single snapshot
fact_usage = fact_usage[
    [
        "customer_id", "time_id",
        "day_mins", "day_calls", "day_charge",
        "eve_mins", "eve_calls", "eve_charge",
        "night_mins", "night_calls", "night_charge",
        "intl_mins", "intl_calls", "intl_charge",
        "custserv_calls", "churn_flag"
    ]
]

# =========================
# 3. Load into Postgres
# =========================

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5433/cdr_db")

with engine.connect() as conn:
    # Load dimensions and fact
    dim_customer.to_sql("dim_customer", conn, if_exists="replace", index=False)
    dim_time.to_sql("dim_time", conn, if_exists="replace", index=False)
    fact_usage.to_sql("fact_usage", conn, if_exists="replace", index=False)

print("✅ Data successfully loaded into Postgres star schema!")
