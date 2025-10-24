import streamlit as st

st.set_page_config(page_title="Revenue Estimator", layout="wide")

st.title("📊 Revenue Estimator")

st.markdown("""
Estimate your hawker stall’s monthly **revenue, costs, and profit** based on your location, pricing, and expenses.
""")

st.divider()

# --- Location & Rent ---
st.header("1. Location & Rent")
location = st.selectbox(
    "Choose your stall location:",
    [
        "🏡 New Estate (~$1800)", 
        "🌆 Mature Estate (~$2500)", 
        "🏢 CBD Area (~$4000)", 
        "✍️ Custom"
    ]
)

# Extract rent based on location
if "New Estate" in location:
    rent = 1800
elif "Mature Estate" in location:
    rent = 2500
elif "CBD Area" in location:
    rent = 4000
else:
    rent = st.number_input("Enter custom rent ($)", min_value=0, value=2500)

st.divider()

# --- Monthly Operations & Cost ---
st.header("2. Monthly Operations & Cost")
days = st.slider("Operating days per month", min_value=0, max_value=31, value=26)

manpower = st.number_input("Manpower cost ($)", min_value=0, value=2000)
cleaning = st.number_input("Cleaning fee ($)", min_value=0, value=500)
scc_fee = st.number_input("Service & Conservancy Charges ($)", min_value=0, value=175)
utilities = st.number_input("Utilities ($)", min_value=0, value=400)
misc = st.number_input("Miscellaneous fees ($)", min_value=0, value=200)

st.divider()

# --- Revenue Inputs ---
st.header("3. Revenue")
price_per_item = st.number_input("Price per item sold ($)", min_value=0.5, value=5.0, step=0.5)
items_sold_per_day = st.number_input("Estimated items sold per day", min_value=0, value=80)

st.divider()

# --- Calculation ---
monthly_revenue = price_per_item * items_sold_per_day * days
monthly_costs = rent + manpower + cleaning + scc_fee + utilities + misc
net_profit = monthly_revenue - monthly_costs

# --- Results ---
st.header("📊 Results")

col1, col2, col3 = st.columns(3)
col1.metric("Estimated Monthly Revenue", f"${monthly_revenue:,.2f}")
col2.metric("Estimated Monthly Costs", f"${monthly_costs:,.2f}")

if net_profit > 0:
    col3.metric("Net Profit", f"${net_profit:,.2f}", delta="+Profit", delta_color="normal")
    st.success(f"🎉 You're making a profit of **${net_profit:,.2f}** per month!")
elif net_profit < 0:
    col3.metric("Net Profit", f"-${-net_profit:,.2f}", delta="-Loss", delta_color="inverse")
    st.error(f"💸 You're losing **${-net_profit:,.2f}** per month.")
else:
    col3.metric("Net Profit", "$0.00")
    st.info("😐 You're breaking even.")

st.divider()

# Detailed cost breakdown
with st.expander("See detailed cost breakdown"):
    st.write(f"- Rent: ${rent}")
    st.write(f"- Manpower: ${manpower}")
    st.write(f"- Cleaning Fee: ${cleaning}")
    st.write(f"- S&CC Fee: ${scc_fee}")
    st.write(f"- Utilities: ${utilities}")
    st.write(f"- Miscellaneous: ${misc}")

st.divider()

# Footer
st.caption("HawkerHub © 2025")

