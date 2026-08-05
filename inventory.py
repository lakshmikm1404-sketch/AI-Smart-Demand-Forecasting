import pandas as pd

forecast = pd.read_csv(
    "data/forecast.csv"
)

avg_demand = (
    forecast["yhat"]
    .tail(30)
    .mean()
)

lead_time = 7

safety_stock = (
    avg_demand * 0.3
)

reorder_point = (
    avg_demand * lead_time
    + safety_stock
)

print()

print("Average Demand")
print(round(avg_demand))

print()

print("Safety Stock")
print(round(safety_stock))

print()

print("Reorder Point")
print(round(reorder_point))