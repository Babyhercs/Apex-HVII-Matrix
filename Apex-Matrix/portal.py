import os
import streamlit as st
import requests

# Dynamically route requests based on environment
BACKEND_URL = os.getenv("BACKEND_URL", "https://apex-hvii-backend.onrender.com")

# ... (your sidebar and authentication gate code)

    if st.button("Run HVII Evaluation", type="primary"):
        payload = {
            "asset_name": asset_name,
            "purchase_price": purchase_price,
            "intrinsic_value": intrinsic_value,
            "down_payment": down_payment,
            "monthly_gross_income": gross_income,
            "monthly_expenses": expenses,
            "debt_interest_rate": interest_rate,
            "expected_annual_appreciation": appreciation,
            "market_liquidity_score": liquidity,
            "project_complexity_score": complexity,
            "depreciation_benefit_multiplier": depreciation,
            "sector_expertise": sector_exp,
            "is_contrarian_play": contrarian,
            "systematic_model": systematic
        }
        headers = {"X-Apex-API-Key": license_key}
        
        try:
            # Send request to your live Render FastAPI backend
            res = requests.post(f"{BACKEND_URL}/api/v1/evaluate", json=payload, headers=headers)
            if res.status_code == 200:
                data = res.json()
                st.success(f"Verdict: {data['verdict']}")
                r1, r2, r3 = st.columns(3)
                r1.metric("HVII Index Score", f"{data['hvii_index']} / 10")
                r2.metric("Stress-Tested Cash Flow", f"${data['stress_tested_cash_flow']:,.2f} / yr")
                r3.metric("Risk Profile", data['risk_profile'])
            else:
                st.error(f"Error ({res.status_code}): {res.text}")
        except Exception as e:
            st.error(f"Connection failed: {e}")
