import streamlit as st
import requests

st.set_page_config(page_title="Apex HVII Matrix", layout="wide")
st.title("Apex Real Estate Evaluation Matrix")
st.markdown("Enter property financials to generate a Presidential-Tier HVII Score.")

with st.sidebar:
    st.header("Authentication")
    api_key = st.text_input("Enter License Key (API Key)", type="password")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Financials")
    asset_name = st.text_input("Asset Name", "Industrial Warehouse Expansion")
    purchase_price = st.number_input("Purchase Price ($)", value=1250000.0)
    intrinsic_value = st.number_input("Intrinsic Value ($)", value=1600000.0)
    down_payment = st.number_input("Down Payment ($)", value=250000.0)
    gross_income = st.number_input("Monthly Gross Income ($)", value=22000.0)
    expenses = st.number_input("Monthly Expenses ($)", value=4500.0)
    interest_rate = st.number_input("Debt Interest Rate (Decimal)", value=0.075)

with col2:
    st.subheader("Risk & Friction Matrix")
    appreciation = st.number_input("Expected Annual Appreciation (Decimal)", value=0.04)
    liquidity = st.slider("Market Liquidity Score (1-10)", 1.0, 10.0, 4.0)
    complexity = st.slider("Project Complexity (1-10)", 1.0, 10.0, 6.5)
    depreciation = st.number_input("Depreciation Benefit Multiplier", value=1.45)
    
    st.markdown("### Heuristics")
    expertise = st.checkbox("Sector Expertise Bonus")
    contrarian = st.checkbox("Contrarian Play Bonus")
    systematic = st.checkbox("Systematic Model Bonus")

if st.button("Generate Asset Report"):
    if not api_key:
        st.error("Please enter your License Key in the sidebar.")
    else:
        payload = https://apex-hvii-backend.onrender.com/api/v1/evaluate](https://apex-hvii-backend.onrender.com/api/v1/evaluate)
            "asset_name": asset_name, "purchase_price": purchase_price,
            "intrinsic_value": intrinsic_value, "down_payment": down_payment,
            "monthly_gross_income": gross_income, "monthly_expenses": expenses,
            "debt_interest_rate": interest_rate, "expected_annual_appreciation": appreciation,
            "market_liquidity_score": liquidity, "project_complexity_score": complexity,
            "depreciation_benefit_multiplier": depreciation, "sector_expertise": expertise,
            "is_contrarian_play": contrarian, "systematic_model": systematic
        }
        
        headers = {"X-Apex-API-Key": api_key}
        response = requests.post("http://localhost:8000/api/v1/evaluate", json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"Verdict: {result['verdict']}")
            st.metric("HVII Index Score", result['hvii_index'])
            st.metric("Stress-Tested Annual Cash Flow", f"${result['stress_tested_annual_cash_flow']:,.2f}")
            st.metric("Cash on Cash Return", f"{result['cash_on_cash_return_pct']}%")
        else:
            st.error("Invalid API Key or Server Error.")
