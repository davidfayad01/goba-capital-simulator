
import streamlit as st

st.set_page_config(page_title="Goba Capital Simulator", layout="centered")
st.title("📊 Goba Capital Simulator")

st.markdown("""
Este simulador muestra el impacto financiero de tomar un producto de financiamiento estructurado de Goba Capital. 
Dependiendo del producto, se simula el ahorro en días de operación (cuentas por cobrar, por pagar o inventario), el costo financiero, el aumento en flujo de caja y el ROI.
""")

# --- Selección de producto ---
product = st.selectbox("Select Financial Product", [
    "Factoring",
    "Finance to Suppliers",
    "Inventory Financing",
    "Asset-Based Lending (ABL)",
    "Loan"
])

# --- Datos generales ---
st.header("📥 Input Data")
annual_sales = st.number_input("Annual Sales (USD)", min_value=0.0, value=10000000.0, step=100000.0)
operating_margin = st.number_input("Operating Margin (%)", min_value=0.0, value=10.0, step=0.5) / 100
financing_amount = st.number_input("Financing Amount Requested (USD)", min_value=0.0, value=2000000.0, step=100000.0)
annual_interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=18.0, step=0.5) / 100

# --- Variables específicas según producto ---
st.subheader("Operational Data Affected by Product")

if product == "Factoring":
    ar_before = st.number_input("Accounts Receivable Days (Before)", min_value=0, value=60)
    ar_after = st.number_input("Accounts Receivable Days (After)", min_value=0, value=30)
    days_saved = ar_before - ar_after
elif product == "Finance to Suppliers":
    ap_before = st.number_input("Accounts Payable Days (Before)", min_value=0, value=30)
    ap_after = st.number_input("Accounts Payable Days (After)", min_value=0, value=60)
    days_saved = ap_after - ap_before
elif product == "Inventory Financing":
    inv_before = st.number_input("Inventory Days (Before)", min_value=0, value=90)
    inv_after = st.number_input("Inventory Days (After)", min_value=0, value=60)
    days_saved = inv_before - inv_after
elif product == "Asset-Based Lending (ABL)":
    days_saved = st.slider("Estimated Efficiency Days Saved", min_value=0, max_value=90, value=15)
elif product == "Loan":
    days_saved = st.slider("Estimated Cash Flow Benefit Days", min_value=0, max_value=90, value=10)

# --- Cálculos financieros ---
daily_sales = annual_sales / 360
cash_benefit = daily_sales * days_saved

quarterly_sales = annual_sales / 4
operating_income_annual = annual_sales * operating_margin
operating_income_quarterly = quarterly_sales * operating_margin

quarterly_interest = financing_amount * ((1 + annual_interest_rate) ** (90 / 360) - 1)
annual_interest = financing_amount * annual_interest_rate

cash_after_financing_q = operating_income_quarterly + (cash_benefit / 4) - quarterly_interest
cash_after_financing_a = operating_income_annual + cash_benefit - annual_interest

roi_q = ((cash_after_financing_q - operating_income_quarterly) / quarterly_interest) * 100 if quarterly_interest > 0 else 0
roi_a = ((cash_after_financing_a - operating_income_annual) / annual_interest) * 100 if annual_interest > 0 else 0

# --- Resultados ---
st.header("📈 Financial Impact")

st.write(f"🔹 **Days Saved**: {days_saved} days")
st.write(f"🔹 **Annual Cash Flow Benefit**: USD {cash_benefit:,.0f}")
st.write(f"🔹 **Quarterly Interest Cost**: USD {quarterly_interest:,.0f}")
st.write(f"🔹 **Annual Interest Cost**: USD {annual_interest:,.0f}")

st.subheader("💰 Cash Flow After Financing")
st.write(f"Quarterly Cash Flow (After Financing): USD {cash_after_financing_q:,.0f}")
st.write(f"Annual Cash Flow (After Financing): USD {cash_after_financing_a:,.0f}")

st.subheader("📊 ROI from Financing")
st.write(f"Quarterly ROI: {roi_q:.2f}%")
st.write(f"Annual ROI: {roi_a:.2f}%")
