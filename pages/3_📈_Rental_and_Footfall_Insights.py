import streamlit as st
import pandas as pd
import altair as alt

# Page config
st.set_page_config(page_title="📈 Rental & Footfall Insights", layout="wide")

# Title
st.title("📈 Rental & Footfall Insights")
st.markdown("Analyze historical rental bid data and estimated foot traffic for hawker centres in Singapore.")

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("data/rental_data.csv")  # Adjust path if needed

    # Convert Month to datetime
    df["Month"] = pd.to_datetime(df["Month"])

    # Rename columns for convenience
    df.rename(columns={
        "Hawker Centre": "hawker_centre",
        "Trade Type": "trade_type",
        "Bid Amount": "bid_amount",
        "Region": "region",
        "Footfall Estimate": "footfall"
    }, inplace=True)

    return df

df = load_data()

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Data")

    region_options = ["All"] + sorted(df["region"].unique())
    selected_region = st.selectbox("Region", region_options)

    trade_options = ["All"] + sorted(df["trade_type"].unique())
    selected_trade = st.selectbox("Trade Type", trade_options)

# Apply filters
filtered_df = df.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]
if selected_trade != "All":
    filtered_df = filtered_df[filtered_df["trade_type"] == selected_trade]

# Summary metrics
st.subheader("📊 Summary Statistics")
col1, col2 = st.columns(2)
col1.metric("Average Rent", f"${filtered_df['bid_amount'].mean():,.0f}")
col2.metric("Average Footfall", f"{filtered_df['footfall'].mean():,.0f} people/day")

st.divider()

# Line chart: Bid trends over time
st.subheader("📅 Rental Trends Over Time")
line_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
    x=alt.X("Month:T", title="Month"),
    y=alt.Y("bid_amount:Q", title="Bid Amount (SGD)"),
    color="hawker_centre:N",
    tooltip=["hawker_centre", "trade_type", "bid_amount", "Month"]
).properties(width=800, height=400)

st.altair_chart(line_chart, use_container_width=True)

# Bar chart: Footfall by Hawker Centre (aggregated)
st.subheader("🚶 Footfall by Hawker Centre")

# Aggregate footfall by hawker centre and region
footfall_df = (
    filtered_df.groupby(["hawker_centre", "region"], as_index=False)
    .agg({"footfall": "mean"})  # Use "sum" instead of "mean" if total footfall is preferred
)

# Bar chart
bar_chart = alt.Chart(footfall_df).mark_bar().encode(
    x=alt.X("hawker_centre:N", sort="-y", title="Hawker Centre"),
    y=alt.Y("footfall:Q", title="Avg. Estimated Daily Footfall"),
    color="region:N",
    tooltip=["hawker_centre", "footfall", "region"]
).properties(width=800, height=400)

st.altair_chart(bar_chart, use_container_width=True)

# Data table with formatted Month column
st.divider()
with st.expander("🔍 Show Data Table"):
    display_df = filtered_df.copy()
    display_df["Month"] = display_df["Month"].dt.strftime("%Y-%m")  # Format month
    st.dataframe(display_df.sort_values("Month", ascending=False), use_container_width=True)

# Footer
st.caption("HawkerHub © 2025")
