import pandas as pd

df = pd.read_csv("data/cleaned.csv")

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

daily = (
    df.groupby(df["InvoiceDate"].dt.date)["Quantity"]
    .sum()
    .reset_index()
)

daily.columns = ["ds", "y"]

daily["ds"] = pd.to_datetime(daily["ds"])

daily.to_csv(
    "data/daily_demand.csv",
    index=False
)

print("daily_demand.csv generated")
print(daily.head())