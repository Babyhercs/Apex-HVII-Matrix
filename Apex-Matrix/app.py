import math
import requests
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Apex HVII Commercial Underwriting Matrix", 
    layout="wide"
)

# --- GUMROAD LICENSE VERIFICATION CONFIGURATION ---
GUMROAD_PRODUCT_PERMALINK = "frccez"  # Replace with your exact Gumroad product permalink

def verify_gumroad_license(license_key: str) -> bool:
    """
    Validates the customer's license key against Gumroad's API in real time.
    Also permits a master testing key for immediate admin access.
    """
    if not license_key:
        return False
        
    # Allow master test key for debugging
    if license_key == "sk_apex_live_12345":
        return True
        
    verify_url = "https://api.gumroad.com/v2/licenses/verify"
    payload = {
        "product_permalink": GUMROAD_PRODUCT_PERMALINK,
        "license_key": license_key
    }
    
    try:
        response = requests.post(verify_url, data=payload)
        data = response.json()
        if data.get("success") and not data.get("purchase", {}).get("refunded"):
            return True
    except Exception:
        pass
    return False

# --- CORE MATRIX ENGINE ---
class HighValueInvestorGem:
    def __init__(self, investor_profile: str = "Presidential Aggressive"):
        self.profile = investor_profile
        self.kiyosaki_weight = 0.50
        self.schwab_weight = 0.50
        
        self.heuristics = {
            "Buffett_Margin_Safety": 1.1,
            "Soros_Macro_Stability": 1.05,
            "Lynch_Expertise": 1.1,
            "Templeton_Contrarian": 1.05,
            "Dalio_Systematic": 1.05
        }

    def evaluate_asset(self, asset_metadata: dict) -> dict:
        price = asset_metadata.get("purchase_price", 0.0)
        intrinsic_value = asset_metadata.get("intrinsic_value", price) 
        down_payment = asset_metadata.get("down_payment", price)
        debt_principal = price - down_payment
        
        friction_factor = asset_metadata.get("project_complexity_score", 5.0) / 10.0
        bad_case_impact = 1 - (friction_factor * 0.20) 
        
        gross_annual_income = (asset_metadata.get("monthly_gross_income", 0.0) * 12) * bad_case_impact
        annual_expenses = asset_metadata.get("monthly_expenses", 0.0) * 12
        
        annual_debt_service = debt_principal * asset_metadata.get("debt_interest_rate", 0.0)
        net_cash_flow = (gross_annual_income - annual_expenses) - annual_debt_service
        
        tax_shield = asset_metadata.get("depreciation_benefit_multiplier", 1.0)
        
        cash_on_cash_return = (net_cash_flow / down_payment) if down_payment > 0 else 0.0
        kiyosaki_score = ((cash_on_cash_return * 10) * tax_shield)
        
        if price <= (intrinsic_value * 0.8):
            kiyosaki_score *= self.heuristics["Buffett_Margin_Safety"]
        if asset_metadata.get("sector_expertise", False):
            kiyosaki_score *= self.heuristics["Lynch_Expertise"]
            
        kiyosaki_score = max(0.0, min(10.0, kiyosaki_score))

        liquidity = asset_metadata.get("market_liquidity_score", 5.0)
        appreciation = asset_metadata.get("expected_annual_appreciation", 0.0)
        schwab_score = (liquidity * 0.4) + (appreciation * 100) - (friction_factor * 2)
        
        if asset_metadata.get("stable_macro_zone", True):
            schwab_score *= self.heuristics["Soros_Macro_Stability"]
        if asset_metadata.get("is_contrarian_play", False):
            schwab_score *= self.heuristics["Templeton_Contrarian"]
            
        schwab_score = max(0.0, min(10.0, schwab_score))

        hvii = (kiyosaki_score * self.kiyosaki_weight) + (schwab_score * self.schwab_weight)
        
        if asset_metadata.get("systematic_model", False):
            hvii *= self.heuristics["Dalio_Systematic"]
            
        hvii = max(0.0, min(10.0, hvii))
        
        verdict = "STRONG ACQUISITION TARGET" if hvii >= 7.5 else "HOLD / CONDITIONAL" if hvii >= 5.0 else "LIQUIDITY DRAIN"
        
        return {
            "asset_name": asset_metadata.get("asset_name"),
            "hvii_index": round(hvii, 2),
            "stress_tested_cash_flow": round(net_cash_flow, 2),
            "verdict": verdict,
            "risk_profile": "High Friction/High Reward" if friction_factor > 0.7 else "Efficient/Stable"
        }

gem_engine = HighValueInvestorGem()

# --- STREAMLIT UI DESIGN ---
st.title("Apex Commercial Underwriting Suite")
st.markdown("Presidential-Tier Real Estate Matrix & Risk Assessment Engine")

# Sidebar Authentication Gate
with st.sidebar:
    st.header("Subscriber Access")
    license_key = st.text_input("Enter Gumroad License Key", type="password", value="")
    st.markdown("---")
    st.info("Subscribe via Gumroad to receive your active enterprise license key.")

# Validate License Key before rendering underwriting form
if not verify_gumroad_license(license_key):
    if license_key:
        st.error("❌ Invalid or inactive license key. Please check your credentials or active subscription.")
    else:
        st.warning("🔒 Please enter your Gumroad license key in the sidebar to unlock the underwriting matrix.")
    st.stop()

st.success("✅ License Verified Successfully. Access Granted.")

# Main Underwriting Inputs (Two Column Layout)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Financial Metrics")
    asset_name = st.text_input("Asset Name / Description", "Industrial Warehouse Expansion & Structural Refit")
    purchase_price = st.number_input("Purchase Price ($)", value=1250000.0, step=10000.0)
    intrinsic_value = st.number_input("Intrinsic / Appraisal Value ($)", value=1600000.0, step=10000.0)
    down_payment = st.number_input("Down Payment / Equity ($)", value=250000.0, step=5000.0)
    gross_income = st.number_input("Monthly Gross Income ($)", value=22000.0, step=500.0)
    expenses = st.number_input("Monthly Operating Expenses ($)", value=4500.0, step=100.0)
    debt_interest_rate = st.number_input("Debt Interest Rate (Decimal)", value=0.075, step=0.005)

with col2:
    st.subheader("Risk & Friction Matrix")
    appreciation = st.number_input("Expected Annual Appreciation (Decimal)", value=0.04, step=0.01)
    liquidity = st.slider("Market Liquidity Score (1-10)", 1.0, 10.0, 4.0)
    complexity = st.slider("Project Complexity / Friction Score (1-10)", 1.0, 10.0, 6.5)
    depreciation = st.number_input("Depreciation Benefit Multiplier", value=1.45, step=0.05)
    
    st.markdown("### Elite Heuristics Overrides")
    sector_exp = st.checkbox("Sector Expertise Bonus (Lynch)", value=True)
    contrarian = st.checkbox("Contrarian Play Bonus (Templeton)", value=True)
    systematic = st.checkbox("Systematic Model Bonus (Dalio)", value=True)
    macro_zone = st.checkbox("Stable Macro Zone (Soros)", value=True)

# Evaluation Execution Trigger
if st.button("Generate Executive Underwriting Report", type="primary"):
    asset_data = {
        "asset_name": asset_name,
        "purchase_price": purchase_price,
        "intrinsic_value": intrinsic_value,
        "down_payment": down_payment,
        "monthly_gross_income": gross_income,
        "monthly_expenses": expenses,
        "debt_interest_rate": debt_interest_rate,
        "expected_annual_appreciation": appreciation,
        "market_liquidity_score": liquidity,
        "project_complexity_score": complexity,
        "depreciation_benefit_multiplier": depreciation,
        "sector_expertise": sector_exp,
        "is_contrarian_play": contrarian,
        "systematic_model": systematic,
        "stable_macro_zone": macro_zone
    }
    
    result = gem_engine.evaluate_asset(asset_data)
    
    st.markdown("---")
    st.header(f"Underwriting Results: {result['asset_name']}")
    
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.metric("HVII Index Score", f"{result['hvii_index']} / 10")
    with res_col2:
        st.metric("Stress-Tested Cash Flow", f"${result['stress_tested_cash_flow']:,.2f} / yr")
    with res_col3:
        st.metric("Risk Profile", result['risk_profile'])
        
    if "STRONG" in result['verdict']:
        st.success(f"**Final Verdict:** {result['verdict']}")
    elif "HOLD" in result['verdict']:
        st.warning(f"**Final Verdict:** {result['verdict']}")
    else:
        st.error(f"**Final Verdict:** {result['verdict']}")
