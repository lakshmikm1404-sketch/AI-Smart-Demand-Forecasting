import streamlit as st
import pandas as pd
import plotly.express as px
import os
from openai import OpenAI
import requests

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Smart Demand Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Smart Demand Forecasting")

st.markdown(
    """
This dashboard predicts future retail demand,
provides inventory recommendations,
and supports decision-making using AI-driven insights.
"""
)

# =====================================================
# LOAD DATA
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

forecast_path = os.path.join(
    BASE_DIR,
    "data",
    "forecast.csv"
)

if not os.path.exists(forecast_path):
    st.error("forecast.csv not found.")
    st.stop()

if os.path.getsize(forecast_path) == 0:
    st.error("forecast.csv is empty.")
    st.stop()

forecast = pd.read_csv(forecast_path)

required_columns = [
    "ds",
    "yhat",
    "yhat_lower",
    "yhat_upper"
]

for col in required_columns:
    if col not in forecast.columns:
        st.error(f"Missing column: {col}")
        st.stop()

forecast["ds"] = pd.to_datetime(
    forecast["ds"]
)

# =====================================================
# KPI CALCULATIONS
# =====================================================

avg_demand = round(
    forecast["yhat"].mean()
)

peak_demand = round(
    forecast["yhat"].max()
)

forecast_records = len(
    forecast
)

growth_pct = round(
    (
        (
            forecast["yhat"].iloc[-1]
            -
            forecast["yhat"].iloc[0]
        )
        /
        forecast["yhat"].iloc[0]
    ) * 100,
    2
)

# =====================================================
# FORECAST SUMMARY
# =====================================================

st.subheader("📈 Forecast Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Forecast Records",
    forecast_records
)

c2.metric(
    "Average Demand",
    avg_demand
)

c3.metric(
    "Peak Demand",
    peak_demand
)

c4.metric(
    "Demand Growth %",
    f"{growth_pct}%"
)

# =====================================================
# FORECAST TREND
# =====================================================

st.subheader("📊 Demand Forecast Trend")

fig = px.line(
    forecast,
    x="ds",
    y="yhat",
    markers=True
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Predicted Demand"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# FORECAST DATA
# =====================================================

st.subheader("📋 Forecast Data")

st.dataframe(
    forecast,
    use_container_width=True
)

# =====================================================
# CONFIDENCE RANGE
# =====================================================

latest = forecast.iloc[-1]

st.subheader("Forecast Confidence Range")

st.info(
    f"""
Expected Demand: {round(latest['yhat'])} units

Minimum Expected Demand: {round(latest['yhat_lower'])} units

Maximum Expected Demand: {round(latest['yhat_upper'])} units
"""
)

# =====================================================
# INVENTORY RECOMMENDATION
# =====================================================

st.subheader("📦 Inventory Recommendation")

safety_stock = round(
    avg_demand * 0.30
)

reorder_point = round(
    avg_demand * 7
    + safety_stock
)

col1, col2 = st.columns(2)

col1.success(
    f"Recommended Safety Stock: {safety_stock} units"
)

col2.info(
    f"Suggested Reorder Point: {reorder_point} units"
)

# =====================================================
# BUSINESS INTERPRETATION
# =====================================================

st.subheader("Business Interpretation")

if growth_pct > 10:
    trend_msg = "Demand is increasing strongly."

elif growth_pct > 0:
    trend_msg = "Demand is showing moderate growth."

else:
    trend_msg = "Demand is declining."

st.write(trend_msg)

st.write(
    f"""
Average demand is expected to be approximately
{avg_demand} units.

To reduce stockout risk,
maintain at least {safety_stock} units
as safety stock.

Place a replenishment order when
inventory drops below
{reorder_point} units.
"""
)

# =====================================================
# OPENAI BUSINESS INSIGHTS
# =====================================================

st.subheader("🤖 OpenAI Business Insights")

st.success(
    f"""
Demand is expected to reach {peak_demand} units.

Forecast growth is {growth_pct}%.

Inventory should be increased to
accommodate future demand.

Recommended Action:

Increase procurement planning and
maintain safety stock levels.
"""
)

# =====================================================
# AI CHATBOT
# =====================================================
st.subheader("💬 Retail Assistant")

question = st.text_input(
    "Ask about demand, inventory, safety stock, or reorder point"
)

if st.button("Ask Assistant"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        user_question = question.lower().strip()

        if "safety stock" in user_question:
            answer = (
                f"The recommended safety stock is "
                f"{safety_stock:,} units. "
                f"It acts as additional inventory to protect "
                f"against unexpected demand increases."
            )

        elif "reorder point" in user_question:
            answer = (
                f"The current reorder point is "
                f"{reorder_point:,} units. "
                f"A replenishment order should be placed when "
                f"available inventory reaches this level."
            )

        elif (
            "average demand" in user_question
            or "average forecast" in user_question
        ):
            answer = (
                f"The average forecasted demand is "
                f"{avg_demand:,} units for the current "
                f"forecast period."
            )

        elif (
            "peak demand" in user_question
            or "maximum demand" in user_question
        ):
            answer = (
                f"The highest predicted demand is "
                f"{peak_demand:,} units."
            )

        elif (
            "growth" in user_question
            or "increasing" in user_question
            or "decreasing" in user_question
        ):
            if growth_pct > 10:
                trend = "increasing strongly"
            elif growth_pct > 0:
                trend = "showing moderate growth"
            elif growth_pct == 0:
                trend = "remaining stable"
            else:
                trend = "declining"

            answer = (
                f"Demand is {trend}. "
                f"The forecasted change is {growth_pct}% "
                f"from the first forecast date to the last."
            )

        elif (
            "next month" in user_question
            or "monthly demand" in user_question
        ):
            monthly_demand = round(avg_demand * 30)
            suggested_order = monthly_demand + safety_stock

            answer = (
                f"The estimated demand for the next 30 days is "
                f"{monthly_demand:,} units. Including "
                f"{safety_stock:,} units of safety stock, the "
                f"suggested inventory requirement is "
                f"{suggested_order:,} units."
            )

        elif (
            "stockout" in user_question
            or "stock out" in user_question
        ):
            answer = (
                f"The current dashboard predicts total demand, "
                f"not individual product demand. A product is at "
                f"stockout risk when its available inventory is "
                f"less than its forecasted demand plus safety stock. "
                f"Product-wise inventory data is required to identify "
                f"the exact SKU at risk."
            )

        elif (
            "which product" in user_question
            or "which sku" in user_question
            or "overstock" in user_question
        ):
            answer = (
                "Product-level results are not currently available. "
                "To answer this question accurately, the application "
                "needs SKU-level forecast demand and current stock "
                "quantities. The existing forecast represents total "
                "demand across all products."
            )

        elif (
            "inventory" in user_question
            or "reorder" in user_question
        ):
            answer = (
                f"Current inventory recommendations are: "
                f"average demand of {avg_demand:,} units, "
                f"safety stock of {safety_stock:,} units, and "
                f"a reorder point of {reorder_point:,} units."
            )

        elif (
            "forecast" in user_question
            or "demand" in user_question
        ):
            answer = (
                f"The forecast contains {forecast_records} records. "
                f"Average demand is {avg_demand:,} units, peak demand "
                f"is {peak_demand:,} units, and forecast growth is "
                f"{growth_pct}%."
            )

        else:
            answer = (
                "I can answer questions about forecast demand, "
                "average demand, peak demand, demand growth, "
                "safety stock, reorder point, monthly inventory, "
                "and stockout risk. Please ask a question related "
                "to one of these topics."
            )

        st.success(answer)