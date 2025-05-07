
import streamlit as st

st.set_page_config(page_title="Goba Capital Simulator", layout="centered")

st.title("📊 Goba Capital Simulator")

# --- Entrada de datos ---
product = st.selectbox("Select Financial Product", [
    "Factoring",
    "Finance to Suppliers",
    "Asset-Based Lending (ABL)",
    "Loan",
    "Inventory Financing"
])

st.header("📥 Input Data")

financing_amount = st.number_input("Financing Amount (USD)", min_value=0.0, value=1000000.0, step=10000.0)
annual_interest_rate = st.number_input("Effective Annual Interest Rate (%)", min_value=0.0, value=18.0, step=0.5) / 100
annual_sales = st.number_input("Projected Annual Sales (USD)", min_value=0.0, value=70000000.0, step=1000000.0)
operating_margin = st.number_input("Operating Margin (%)", min_value=0.0, value=12.0, step=0.5) / 100

# Ciclo operativo según producto
st.subheader("Operational Cycle Impact")
ar_days_before = st.number_input("Accounts Receivable Days (Before)", min_value=0, value=60)
ar_days_after = st.number_input("Accounts Receivable Days (After)", min_value=0, value=30)
ap_days_before = st.number_input("Accounts Payable Days (Before)", min_value=0, value=30)
ap_days_after = st.number_input("Accounts Payable Days (After)", min_value=0, value=60)
inventory_days_before = st.number_input("Inventory Days (Before)", min_value=0, value=90)
inventory_days_after = st.number_input("Inventory Days (After)", min_value=0, value=60)

# --- Cálculos base ---
quarterly_sales = annual_sales / 4
operating_income_annual = annual_sales * operating_margin
operating_income_quarterly = quarterly_sales * operating_margin

# Mejora en flujo de caja por días ahorrados
daily_sales = annual_sales / 360
cash_improvement = 0

if product == "Factoring":
    cash_improvement = daily_sales * (ar_days_before - ar_days_after)
elif product == "Finance to Suppliers":
    cash_improvement = daily_sales * (ap_days_after - ap_days_before)
elif product == "Inventory Financing":
    cash_improvement = daily_sales * (inventory_days_before - inventory_days_after)
elif product == "Asset-Based Lending (ABL)":
    cash_improvement = financing_amount * 0.25  # Supuesto estimado
elif product == "Loan":
    cash_improvement = financing_amount * 0.15  # Supuesto estimado

# Costo financiero trimestral y anual
quarterly_interest = financing_amount * ((1 + annual_interest_rate) ** (90 / 360) - 1)
annual_interest = financing_amount * annual_interest_rate

# Flujo de caja después del financiamiento
quarterly_cash_after = operating_income_quarterly + (cash_improvement / 4) - quarterly_interest
annual_cash_after = operating_income_annual + cash_improvement - annual_interest

# ROI
roi_quarterly = ((quarterly_cash_after - operating_income_quarterly) / quarterly_interest) * 100 if quarterly_interest != 0 else 0
roi_annual = ((annual_cash_after - operating_income_annual) / annual_interest) * 100 if annual_interest != 0 else 0

# --- Resultados ---
st.header("📈 Results and Projections")

st.subheader("Cash Flow Projections")
st.write(f"Quarterly Sales: USD {quarterly_sales:,.0f}")
st.write(f"Operating Income (Quarter): USD {operating_income_quarterly:,.0f}")
st.write(f"Operating Income (Annual): USD {operating_income_annual:,.0f}")

st.subheader("Cash Flow After Financing")
st.write(f"Estimated Cash Improvement (Annual): USD {cash_improvement:,.0f}")
st.write(f"Financing Cost (Quarter): USD {quarterly_interest:,.0f}")
st.write(f"Financing Cost (Annual): USD {annual_interest:,.0f}")
st.write(f"Cash Flow After Financing (Quarter): USD {quarterly_cash_after:,.0f}")
st.write(f"Cash Flow After Financing (Annual): USD {annual_cash_after:,.0f}")

st.subheader("📊 ROI")
st.write(f"Quarterly ROI: {roi_quarterly:.2f}%")
st.write(f"Annual ROI: {roi_annual:.2f}%")
