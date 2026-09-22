import streamlit as st
import requests

st.set_page_config(
    page_title="Apex Ecosystem Portal",
    layout="wide"
)

# --- MASTER AUTHENTICATION GATE ---
st.sidebar.title("Apex Portal Access")
license_key = st.sidebar.text_input("Enter Gumroad License Key", type="password")

VALID_ACCESS = (license_key == "sk_apex_live_12345")

if not VALID_ACCESS and license_key:
    st.sidebar.error("Invalid License Key.")

if not VALID_ACCESS:
    st.title("⚡ Apex Ecosystem Portal")
    st.warning("🔒 Please enter your active Apex Suite license key in the sidebar to access enterprise tools.")
    st.stop()

st.sidebar.success("✅ Authorized Apex Member")

# --- MULTI-PROJECT NAVIGATION HUB ---
app_choice = st.sidebar.selectbox(
    "Select Apex Module",
    [
        "HVII Real Estate Matrix", 
        "TradingView Webhook Bot", 
        "Apex Project Pipeline"
    ]
)

if app_choice == "HVII Real Estate Matrix":
    st.title("🏢 Apex HVII Commercial Underwriting Suite")
    st.markdown("Presidential-Tier Real Estate Matrix & Risk Assessment Engine.")
    
    col1, col2 = st.columns(2)
    with col1:
        asset_name = st.text_input("Asset Name / Description", "Industrial Warehouse Expansion & Structural Refit")
        purchase_price = st.number_input("Purchase Price ($)", value=1250000.0)
        intrinsic_value = st.number_input("Intrinsic Value ($)", value=1600000.0)
        down_payment = st.number_input("Down Payment ($)", value=250000.0)
        gross_income = st.number_input("Monthly Gross Income ($)", value=22000.0)
        expenses = st.number_input("Monthly Operating Expenses ($)", value=4500.0)
        interest_rate = st.number_input("Debt Interest Rate (Decimal)", value=0.075)
    with col2:
        appreciation = st.number_input("Expected Annual Appreciation (Decimal)", value=0.04)
        liquidity = st.slider("Market Liquidity Score (1-10)", 1.0, 10.0, 4.0)
        complexity = st.slider("Project Complexity Score (1-10)", 1.0, 10.0, 6.5)
        depreciation = st.number_input("Depreciation Benefit Multiplier", value=1.45)
        
        st.markdown("### Elite Heuristics")
        sector_exp = st.checkbox("Sector Expertise Bonus (Lynch)", value=True)
        contrarian = st.checkbox("Contrarian Play Bonus (Templeton)", value=True)
        systematic = st.checkbox("Systematic Model Bonus (Dalio)", value=True)

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
            # Change to your live Render backend URL when deployed
            res = requests.post("http://127.0.0.1:8000/api/v1/evaluate", json=payload, headers=headers)
            if res.status_code == 200:
                data = res.json()
                st.success(f"Verdict: {data['verdict']}")
                res_col1, res_col2, res_col3 = st.columns(3)
                with res_col1:
                    st.metric("HVII Index Score", f"{data['hvii_index']} / 10")
                with res_col2:
                    st.metric("Stress-Tested Cash Flow", f"${data['stress_tested_cash_flow']:,.2f} / yr")
                with res_col3:
                    st.metric("Risk Profile", data['risk_profile'])
            else:
                st.error(f"Error ({res.status_code}): {res.text}")
        except Exception as e:
            st.error(f"Connection failed: {e}")

elif app_choice == "TradingView Webhook Bot":
    st.title("📈 Apex Automated Execution Bot")
    st.markdown("Live status monitor for TradingView Webhook triggers and prop firm routing.")
    st.metric("Bot Status", "ONLINE & LISTENING")

elif app_choice == "Apex Project Pipeline":
    st.title("🛠️ Apex Developmental Services Pipeline")
    st.table([
        {"Project": "Industrial Warehouse Expansion", "Sector": "Commercial Real Estate", "Status": "Underwriting Complete"},
        {"Project": "Structural Steel Retrofit", "Sector": "Welding & Fabrication", "Status": "In Execution"},
        {"Project": "Modular Stage Blueprint", "Sector": "Custom Carpentry", "Status": "Fabrication Ready"}
    ])
