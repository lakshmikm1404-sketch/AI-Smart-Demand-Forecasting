import pandas as pd

df = pd.read_csv(
    "data/ecommerce.csv",
    encoding="ISO-8859-1"
)

# Remove nulls
df = df.dropna()

# Remove returns/cancellations
df = df[df["Quantity"] > 0]

# Convert date
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Create sales column
df["Sales"] = df["Quantity"] * df["UnitPrice"]

df.to_csv(
    "data/cleaned.csv",
    index=False
)

print("cleaned.csv generated successfully")
print(df.head())