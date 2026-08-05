import pandas as pd
from prophet import Prophet
import joblib

df = pd.read_csv("data/daily_demand.csv")

df["ds"] = pd.to_datetime(df["ds"])

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True
)

model.fit(df)

joblib.dump(
    model,
    "models/prophet_model.pkl"
)

print("Prophet model trained")