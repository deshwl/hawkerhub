import streamlit as st
import pandas as pd
import altair as alt

# -------------------------------
# Page Settings
# -------------------------------
st.set_page_config(page_title="📈 Rental & Footfall Insights", layout="wide")

# -------------------------------
# Title & Intro
# -------------------------------
st.title("📈 Rental & Footfall Insights")
st.markdown(
    "Analyze historical **rental bid data** and **estimated foot traffic** "
    "for hawker centres across Singapore to make smarter business decisions."
)
st.markdown(
    "👈 Use the panel on the left to choose your **Region** and **Trade Type**."
)

st.divider()

# -------------------------------
# Load & Prepare Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/rental_data.csv")  # Adjust path if needed
    df["Month"] = pd.to_datetime(df["Month"])
    df.rename(columns={
        "Hawker Centre": "hawker_centre",
        "Trade Type": "trade_type",
        "Bid Amount": "bid_amount",
        "Region": "region",
        "Footfall Estimate": "footfall"
    }, inplace=True)
    return df

df = load_data()

# -------------------------------
# 🧭 Step 1: Filter Data (Sidebar)
# -------------------------------
with st.sidebar:
    with st.expander("🧭 Step 1: Filter Data", expanded=True):
        st.markdown("Use these filters to explore specific regions or trade types.")

        region_options = ["All"] + sorted(df["region"].unique())
        selected_region = st.selectbox("🌏 Select Region:", region_options, index=0)

        trade_options = ["All"] + sorted(df["trade_type"].unique())
        selected_trade = st.selectbox("🍜 Select Trade Type:", trade_options, index=0)

    st.sidebar.divider()

# -------------------------------
# Apply Filters
# -------------------------------
filtered_df = df.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]
if selected_trade != "All":
    filtered_df = filtered_df[filtered_df["trade_type"] == selected_trade]

# -------------------------------
# 📢 Display Current Filter Status (Clean Grammar)
# -------------------------------
if selected_region == "All" and selected_trade == "All":
    filter_text = "all trades across all regions"
elif selected_region == "All":
    filter_text = f"{selected_trade} trades across all regions"
elif selected_trade == "All":
    filter_text = f"all trades in the {selected_region} region"
else:
    filter_text = f"{selected_trade} trades in the {selected_region} region"

st.markdown(f"Currently viewing data for **{filter_text}**.")

st.divider()

# -------------------------------
# 📊 Step 2: Summary Statistics
# -------------------------------
st.header("📊 Step 2: View Key Figures")

if not filtered_df.empty:
    avg_rent = filtered_df["bid_amount"].mean()
    avg_footfall = filtered_df["footfall"].mean()

    col1, col2 = st.columns(2)
    col1.metric("💰 Average Rent", f"${avg_rent:,.0f}")
    col2.metric("🚶 Average Footfall", f"{avg_footfall:,.0f} people/day")
else:
    st.warning("No data available for the selected filters.")

st.divider()

# -------------------------------
# 📅 Step 3: Rental Trends
# -------------------------------
st.header("📅 Step 3: Rental Trends Over Time")

if not filtered_df.empty:
    top_hawkers = (
        filtered_df.groupby("hawker_centre")["bid_amount"].mean().nlargest(5).index
    )
    chart_df = filtered_df[filtered_df["hawker_centre"].isin(top_hawkers)]

    # Format month axis to show both year and month (YYYY-MM)
    line_chart = (
        alt.Chart(chart_df)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "Month:T",
                title="Month (Year-Month)",
                axis=alt.Axis(
                    format="%Y-%b",
                    labelAngle=-45,
                    tickCount="month"
                )
            ),
            y=alt.Y("bid_amount:Q", title="Bid Amount (SGD)"),
            color=alt.Color("hawker_centre:N", title="Hawker Centre"),
            tooltip=[
                alt.Tooltip("hawker_centre:N", title="Hawker Centre"),
                alt.Tooltip("trade_type:N", title="Trade Type"),
                alt.Tooltip("bid_amount:Q", title="Bid Amount (SGD)", format=",.0f"),
                alt.Tooltip("Month:T", title="Month", format="%Y-%b")
            ],
        )
        .properties(height=400)
    )

    st.altair_chart(line_chart, use_container_width=True)

    latest_month = chart_df["Month"].max().strftime("%b %Y")
    st.info(
        f"📈 Showing data up to **{latest_month}** "
        "for the top 5 hawker centres with the highest average bids."
    )
else:
    st.warning("No trend data available for your selection.")

st.divider()

# -------------------------------
# 🚶 Step 4: Footfall Comparison
# -------------------------------
st.header("🚶 Step 4: Compare Footfall Between Centres")

if not filtered_df.empty:
    footfall_df = (
        filtered_df.groupby(["hawker_centre", "region"], as_index=False)
        .agg({"footfall": "mean"})
    )
    top_footfall = footfall_df.nlargest(5, "footfall")

    bar_chart = alt.Chart(top_footfall).mark_bar(size=40).encode(
        x=alt.X("hawker_centre:N", sort="-y", title="Hawker Centre"),
        y=alt.Y("footfall:Q", title="Avg. Daily Footfall"),
        color=alt.Color("region:N", title="Region"),
        tooltip=["hawker_centre", "region", "footfall"]
    )

    text_labels = bar_chart.mark_text(
        align="center", baseline="bottom", dy=-5
    ).encode(text="footfall:Q")

    st.altair_chart(bar_chart + text_labels, use_container_width=True)

    if not top_footfall.empty:
        top_centre = top_footfall.iloc[0]["hawker_centre"]
        top_value = top_footfall.iloc[0]["footfall"]
        st.success(f"🏆 **{top_centre}** has the highest average daily footfall: **{top_value:,.0f} visitors/day**.")
else:
    st.warning("No footfall data available for your selection.")

st.divider()

# -------------------------------
# 📋 Step 5: View Full Data
# -------------------------------
st.header("📋 Step 5: View Full Data Table")

with st.expander("Show Data Table"):
    if not filtered_df.empty:
        display_df = filtered_df.copy()
        display_df["Month"] = display_df["Month"].dt.strftime("%Y-%m")
        st.dataframe(display_df.sort_values("Month", ascending=False), use_container_width=True)
    else:
        st.info("No data to display.")

st.divider()

# -------------------------------
# Footer
# -------------------------------
st.caption("HawkerHub © 2025")
