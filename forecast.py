import pandas as pd
import joblib

print("Loading model...")

model = joblib.load(
    "models/prophet_model.pkl"
)

print("Creating future dates...")

future = model.make_future_dataframe(
    periods=90
)

print("Generating forecast...")

forecast = model.predict(future)

print(forecast.head())

forecast = forecast[
    [
        "ds",
        "yhat",
        "yhat_lower",
        "yhat_upper"
    ]
]

forecast.to_csv(
    "data/forecast.csv",
    index=False
)

print("forecast.csv generated")
print(forecast.tail())