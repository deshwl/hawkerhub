import streamlit as st

# Config
st.set_page_config(page_title="HawkerHub", layout="centered")

# Logo
st.image("assets/logo.jpg", width=200)  

# Introduction
st.markdown("""
Welcome to **HawkerHub** — a digital assistant for hawkers in Singapore.  
This platform helps you:

✅ Estimate your monthly revenue  
✅ Discover which grants you're eligible for  
✅ Make better business decisions  
""")

st.divider()

# Navigation buttons (Optional)
st.header("🧭 Explore Tools")
st.markdown("<br>", unsafe_allow_html=True)  # Add vertical spacing here

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/1_📊_Revenue_Estimator.py", label="📊 Revenue Estimator", use_container_width=True)
with col2:
    st.page_link("pages/2_🧮_Grant_Finder.py", label="🧮 Grant Finder", use_container_width=True)
with col3:
    st.page_link("pages/3_📈_Rental_and_Footfall_Insights.py", label="📈 Rental & Footfall Insights", use_container_width=True)


st.divider()
st.caption("HawkerHub © 2025")
