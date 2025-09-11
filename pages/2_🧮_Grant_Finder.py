import streamlit as st

# Page settings
st.set_page_config(page_title="Grant Finder", layout="centered")

# Title
st.title("🧮 Grant Finder")
st.markdown(
    "Answer a few quick questions and we’ll show you which government schemes "
    "you may be eligible for based on your current situation."
)

st.divider()

# -------------------------------
# 👤 User Information Section
# -------------------------------
st.header("👤 About You")

# Q1: Are you an existing hawker?
is_existing_hawker = st.radio(
    "Are you currently running a hawker stall?",
    ["Yes", "No"],
    index=0,
    key="existing_hawker"
)

# Q2: Are you planning to start a hawker stall?
is_aspiring_hawker = st.radio(
    "Are you planning to start a hawker stall soon?",
    ["Yes", "No"],
    index=1,
    key="aspiring_hawker"
)

# Q3: Are you interested in promoting hawker culture?
interested_in_culture = st.radio(
    "Are you interested in doing a community or cultural project related to hawker life?",
    ["Yes", "No"],
    index=1,
    key="culture_project"
)

# Q4: Are you looking to improve productivity using equipment?
wants_productivity_tools = st.radio(
    "Would you like support to buy equipment or improve productivity?",
    ["Yes", "No"],
    index=1,
    key="productivity_support"
)

st.divider()

# -------------------------------
# 📝 Summary Section
# -------------------------------
st.header("📝 Your Responses Summary")
st.markdown(f"""
- **Existing Hawker:** {is_existing_hawker}  
- **Aspiring Hawker:** {is_aspiring_hawker}  
- **Interested in Hawker Culture Projects:** {interested_in_culture}  
- **Needs Equipment/Productivity Support:** {wants_productivity_tools}
""")

st.divider()

# -------------------------------
# 📋 Grant Results Section
# -------------------------------
st.header("📋 Your Eligible Grants")

matches = 0  # Track how many grants matched

if is_existing_hawker == "Yes" and wants_productivity_tools == "Yes":
    matches += 1
    st.success("🛠️ Hawkers’ Productivity Grant")
    st.markdown(
        "Improve your kitchen efficiency with approved equipment like automatic rice cookers, fryers, or food warmers.  \n"
        "👉 [Apply or Learn More](https://www.nea.gov.sg/our-services/hawker-management/programmes-and-grants/hawkers-productivity-grant)"
    )

if is_aspiring_hawker == "Yes":
    matches += 1
    st.success("🐣 Incubation Stall Programme (ISP)")
    st.markdown(
        "Get started as a hawker with subsidised stall rent, basic equipment, and mentoring for 6–12 months.  \n"
        "👉 [Apply or Learn More](https://www.nea.gov.sg/our-services/hawker-management/programmes-and-grants/isp)"
    )

if interested_in_culture == "Yes":
    matches += 1
    st.success("🎨 Vibrant Hawker Culture Programme")
    st.markdown(
        "Receive funding to organise projects or events that promote Singapore’s rich hawker heritage.  \n"
        "👉 [Apply or Learn More](https://www.nea.gov.sg/our-services/hawker-management/programmes-and-grants/vibrant-hawker-culture)"
    )

if matches == 0:
    st.warning("🙁 No matching schemes found based on your answers.")
    st.markdown(
        "You can still [view all available hawker grants here](https://www.nea.gov.sg/our-services/hawker-management/programmes-and-grants)."
    )

st.divider()

st.info(
    "This is a simplified eligibility checker. Always check the official NEA pages "
    "for full criteria and application details."
)

st.caption("HawkerHub © 2025")
