import streamlit as st
import pandas as pd

st.set_page_config(page_title="Retirement Pool Simulator", layout="wide")

st.title("📊 Retirement Pool Simulator")

# --- Sidebar Inputs ---
st.sidebar.header("Inputs")

contributors = st.sidebar.number_input("Number of Contributors", value=1000)
monthly_contribution = st.sidebar.slider("Monthly Contribution (€)", 50, 2000, 200)
elderly = st.sidebar.slider("Number of Elderly", 1, 200, 20)
monthly_payout = st.sidebar.slider("Monthly Payout per Elderly (€)", 200, 3000, 800)
property_value = st.sidebar.number_input("Initial Property Value (€)", value=500000)
growth_rate = st.sidebar.slider("Annual Growth Rate (%)", 0.0, 15.0, 5.0) / 100
years = st.sidebar.slider("Years", 1, 40, 20)

# --- Calculations ---
months = years * 12

total_contributions = contributors * monthly_contribution * months
total_payouts = elderly * monthly_payout * months

property_future_value = property_value * ((1 + growth_rate) ** years)

net_surplus = total_contributions - total_payouts + property_future_value

return_per_contributor = net_surplus / contributors

# --- Metrics ---
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Contributions", f"€{total_contributions:,.0f}")
col2.metric("Total Payouts", f"€{total_payouts:,.0f}")
col3.metric("Net Surplus", f"€{net_surplus:,.0f}")

col4, col5 = st.columns(2)
col4.metric("Property Value (Future)", f"€{property_future_value:,.0f}")
col5.metric("Return per Contributor", f"€{return_per_contributor:,.0f}")

# --- Time Series Data ---
year_list = list(range(1, years + 1))
fund_values = []
property_values = []

for y in year_list:
    contrib = contributors * monthly_contribution * 12 * y
    payout = elderly * monthly_payout * 12 * y
    current_property = property_value * ((1 + growth_rate) ** y)
    total_value = contrib - payout + current_property

    fund_values.append(total_value)
    property_values.append(current_property)

df = pd.DataFrame({
    "Year": year_list,
    "Fund Value": fund_values,
    "Property Value": property_values
})

# --- Charts ---
st.subheader("Growth Over Time")
st.line_chart(df.set_index("Year"))

# --- Table ---
st.subheader("Detailed Data")
st.dataframe(df)

# --- Insights ---
st.subheader("Insights")

if net_surplus > 0:
    st.success("✅ The model is profitable under current assumptions.")
else:
    st.error("⚠️ The model is not sustainable. Adjust inputs.")

st.markdown("---")
st.caption("Built with Streamlit")
