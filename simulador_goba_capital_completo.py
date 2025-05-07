
import streamlit as st

st.set_page_config(page_title="Goba Capital Simulator", layout="centered")
st.title("📊 Goba Capital Simulator")

st.markdown("""
Este simulador estima el impacto financiero de tomar un producto de financiamiento de Goba Capital. Según el producto, calcula:
- Ahorros por eficiencia en días operativos (AR, AP, inventario).
- Mejora en flujo de caja.
- ROI y comparativo antes/después.
- Costo financiero trimestral y anual.
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
st.header("📥 Input Financial Data")
annual_sales = st.number_input("Annual Sales (USD)", min_value=0.0, value=20000000.0, step=100000.0)
operating_margin = st.number_input("Operating Margin (%)", min_value=0.0, value=12.0, step=0.5) / 100
financing_amount = st.number_input("Financing Amount Requested (USD)", min_value=0.0, value=5000000.0, step=100000.0)
annual_interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=18.0, step=0.5) / 100

# --- Variables específicas por producto ---
st.subheader("Operational Data Based on Product")

if product == "Factoring":
    ar_before = st.number_input("Accounts Receivable Days (Before)", min_value=0, value=75)
    ar_after = st.number_input("Accounts Receivable Days (After)", min_value=0, value=45)
    savings_days = ar_before - ar_after
    cash_type = "AR"
elif product == "Finance to Suppliers":
    ap_before = st.number_input("Accounts Payable Days (Before)", min_value=0, value=30)
    ap_after = st.number_input("Accounts Payable Days (After)", min_value=0, value=60)
    savings_days = ap_after - ap_before
    cash_type = "AP"
elif product == "Inventory Financing":
    inv_before = st.number_input("Inventory Days (Before)", min_value=0, value=90)
    inv_after = st.number_input("Inventory Days (After)", min_value=0, value=60)
    savings_days = inv_before - inv_after
    cash_type = "Inventory"
elif product == "Asset-Based Lending (ABL)":
    savings_days = st.slider("Estimated Operational Days Gained", min_value=0, max_value=60, value=15)
    cash_type = "Working Capital"
elif product == "Loan":
    savings_days = st.slider("Estimated Cash Flow Benefit (in Days)", min_value=0, max_value=60, value=10)
    cash_type = "Cash Position"

# --- Cálculos financieros ---
daily_sales = annual_sales / 360
cash_release = daily_sales * savings_days

# Ingresos operativos base
op_income_annual = annual_sales * operating_margin
op_income_q = op_income_annual / 4

# Costo financiero
quarterly_interest = financing_amount * ((1 + annual_interest_rate) ** (90 / 360) - 1)
annual_interest = financing_amount * annual_interest_rate

# Proyecciones con financiamiento
cash_with_financing_q = op_income_q + (cash_release / 4) - quarterly_interest
cash_with_financing_a = op_income_annual + cash_release - annual_interest

# ROI
roi_q = ((cash_with_financing_q - op_income_q) / quarterly_interest) * 100 if quarterly_interest > 0 else 0
roi_a = ((cash_with_financing_a - op_income_annual) / annual_interest) * 100 if annual_interest > 0 else 0

# --- Resultados ---
st.header("📈 Financial Impact Summary")

st.markdown(f"""
- **Product:** {product}  
- **Cash Efficiency Source:** {cash_type}  
- **Days Saved:** {savings_days}  
- **Cash Flow Gain (Annual):** USD {cash_release:,.0f}  
- **Quarterly Interest Cost:** USD {quarterly_interest:,.0f}  
- **Annual Interest Cost:** USD {annual_interest:,.0f}  
""")

st.subheader("💰 Cash Flow After Financing")
st.write(f"Quarterly: USD {cash_with_financing_q:,.0f}")
st.write(f"Annual: USD {cash_with_financing_a:,.0f}")

st.subheader("📊 ROI")
st.write(f"Quarterly ROI: {roi_q:.2f}%")
st.write(f"Annual ROI: {roi_a:.2f}%")

st.markdown("---")
st.markdown("💼 Created by Goba Capital - Financial Modeling Unit")
