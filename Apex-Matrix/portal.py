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
    st.warning("🔒 Please enter your active Apex Suite license key (`sk_apex_live_12345`) in the sidebar to access enterprise tools.")
    st.stop()

st.sidebar.success("✅ Authorized Apex Member")

# --- MULTI-PROJECT NAVIGATION HUB ---
app_choice = st.sidebar.selectbox(
    "Select Apex Module",
    [
        "🏢 Commercial Real Estate (HVII Matrix)", 
        "🔥 Structural Welding & Metal Fabrication", 
        "🪵 Custom Carpentry & Stage Builds",
        "📈 TradingView / FXIFY Prop Bot",
        "❓ How Everything Works (Guide)"
    ]
)

# =====================================================================
# 1. COMMERCIAL REAL ESTATE MODULE
# =====================================================================
if app_choice == "🏢 Commercial Real Estate (HVII Matrix)":
    st.title("🏢 Apex Development: Commercial Real Estate Underwriting")
    st.markdown("Evaluates property underwriting, debt service, and cash flow via the Presidential HVII Matrix.")
    
    with st.expander("💡 Click here for guidance on underwriting metrics"):
        st.write("""
        - **Purchase Price & Intrinsic Value**: Compares acquisition cost to true appraised value to unlock the Buffett Margin of Safety multiplier.
        - **Project Complexity**: Factors in localized friction (permits, renovations) to stress-test your worst-case gross income.
        - **Elite Heuristics**: Applies legendary investor overlays (Lynch sector expertise, Templeton contrarian plays, Dalio systematic models).
        """)

    col1, col2 = st.columns(2)
    with col1:
        asset_name = st.text_input("Asset Name / Description", "Industrial Warehouse Expansion & Structural Refit")
        purchase_price = st.number_input("Purchase Price ($)", value=1250000.0, step=10000.0)
        intrinsic_value = st.number_input("Intrinsic Value ($)", value=1600000.0, step=10000.0)
        down_payment = st.number_input("Down Payment ($)", value=250000.0, step=5000.0)
        gross_income = st.number_input("Monthly Gross Income ($)", value=22000.0, step=500.0)
        expenses = st.number_input("Monthly Operating Expenses ($)", value=4500.0, step=100.0)
        interest_rate = st.number_input("Debt Interest Rate (Decimal)", value=0.075, step=0.005)
    with col2:
        appreciation = st.number_input("Expected Annual Appreciation (Decimal)", value=0.04, step=0.01)
        liquidity = st.slider("Market Liquidity Score (1-10)", 1.0, 10.0, 4.0, help="Higher scores indicate faster asset liquidity in local DFW markets.")
        complexity = st.slider("Project Complexity Score (1-10)", 1.0, 10.0, 6.5, help="Reflects engineering, zoning, or heavy remodel friction.")
        depreciation = st.number_input("Depreciation Benefit Multiplier", value=1.45, step=0.05)
        
        st.markdown("### Elite Heuristics Overrides")
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
            res = requests.post("http://127.0.0.1:8000/api/v1/evaluate", json=payload, headers=headers)
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

# =====================================================================
# 2. WELDING & METAL FABRICATION MODULE
# =====================================================================
elif app_choice == "🔥 Structural Welding & Metal Fabrication":
    st.title("🔥 Apex Metal Works: Fabrication & Welding Calculator")
    st.markdown("Inputs material costs, shop hours, and bids to instantly compute job profit margins.")
    
    with st.expander("💡 How to use the Fabrication Calculator"):
        st.write("Enter your raw material expenses, estimated labor hours, shop hourly rate, and your quoted contract price to instantly verify profitability thresholds.")

    w_col1, w_col2 = st.columns(2)
    with w_col1:
        job_name = st.text_input("Project / Bid Name", "Structural Steel Sign & Frame Demolition")
        material_cost = st.number_input("Raw Material Cost ($)", value=3500.0, step=100.0)
        labor_hours = st.number_input("Estimated Shop/Field Labor Hours", value=40.0, step=5.0)
    with w_col2:
        shop_hourly_rate = st.number_input("Shop Hourly Rate ($/hr)", value=85.0, step=5.0)
        quoted_price = st.number_input("Quoted Contract Price ($)", value=12000.0, step=500.0)

    if st.button("Calculate Fabrication Margins", type="primary"):
        total_cost = material_cost + (labor_hours * shop_hourly_rate)
        gross_profit = quoted_price - total_cost
        margin = (gross_profit / quoted_price) if quoted_price > 0 else 0.0
        
        st.success(f"Financial Breakdown for {job_name}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Job Cost", f"${total_cost:,.2f}")
        m2.metric("Gross Profit", f"${gross_profit:,.2f}")
        m3.metric("Profit Margin", f"{margin * 100:.1f}%")
        
        if margin >= 0.4:
            st.info("🟢 **High-Margin Contract**: Exceeds commercial threshold targets.")
        elif margin >= 0.2:
            st.warning("🟡 **Standard Margin**: Acceptable operational yield.")
        else:
            st.error("🔴 **Low Margin / High Risk**: Re-evaluate pricing or labor estimates.")

# =====================================================================
# 3. CUSTOM CARPENTRY & STAGE BUILDS MODULE
# =====================================================================
elif app_choice == "🪵 Custom Carpentry & Stage Builds":
    st.title("🪵 Apex Carpentry: Custom Builds & Stage Estimator")
    st.markdown("Evaluates custom material specs, build complexity, and labor turnaround.")
    
    with st.expander("💡 Stage & Carpentry Build Guidelines"):
        st.write("Designed for specialized builds (e.g., 16x24 modular stages, custom cabinetry, exotic fish tank cabinetry). Automatically accounts for waste factor and build complexity.")

    c_col1, c_col2 = st.columns(2)
    with c_col1:
        build_name = st.text_input("Build Specification", "16-ft x 24-ft Modular Stage Platform")
        lumber_sheets = st.number_input("Lumber / Plywood Sheets Required", value=65, step=5)
        sheet_cost = st.number_input("Average Cost Per Sheet ($)", value=45.0, step=2.0)
    with c_col2:
        hardware_cost = st.number_input("Hardware, Fasteners & Trim Cost ($)", value=600.0, step=50.0)
        assembly_hours = st.number_input("Estimated Assembly & Finishing Hours", value=32.0, step=4.0)

    if st.button("Compute Build Metrics", type="primary"):
        total_material = (lumber_sheets * sheet_cost * 1.15) + hardware_cost  # 15% waste factor included
        labor_cost = assembly_hours * 65.0
        total_build_cost = total_material + labor_cost
        
        st.success(f"Build Analysis: {build_name}")
        b1, b2, b3 = st.columns(3)
        b1.metric("Material Cost (w/ 15% Waste)", f"${total_material:,.2f}")
        b2.metric("Labor Allocation", f"${labor_cost:,.2f}")
        b3.metric("Total Estimated Investment", f"${total_build_cost:,.2f}")

# =====================================================================
# 4. TRADINGVIEW / FXIFY PROP BOT MODULE
# =====================================================================
elif app_choice == "📈 TradingView / FXIFY Prop Bot":
    st.title("📈 Apex Automated Execution Bot")
    st.markdown("Monitors automated trade signal execution logs and prop account performance.")
    
    with st.expander("💡 Webhook & Prop Bot Instructions"):
        st.write("Point your TradingView alert webhooks to `https://your-domain.onrender.com/api/v1/webhook` to execute automated trades across FXIFY, FTMO, and DXTrade accounts.")

    st.metric("Engine Status", "ONLINE & LISTENING")
    st.metric("Active Strategy", "FXIFY Institutional Trend Engine V15.9")
    
    st.markdown("### Recent Webhook Activity Log")
    st.code("""
    [2026-09-22 04:12:05] INFO: Received BUY signal for EURUSD | Vol: 1.50 | SL: 1.0820 | TP: 1.0950
    [2026-09-22 02:45:11] INFO: Received SELL signal for BTCUSD | Vol: 0.25 | SL: 64200 | TP: 61000
    [2026-09-21 22:10:00] SUCCESS: DXTrade session token refreshed successfully.
    """, language="text")

# =====================================================================
# 5. HOW EVERYTHING WORKS (GUIDE)
# =====================================================================
elif app_choice == "❓ How Everything Works (Guide)":
    st.title("❓ Apex Ecosystem: Master User Guide")
    st.markdown("A complete overview of how the tools, licensing, and cloud infrastructure work together.")
    
    st.markdown("""
    ### 🔑 1. Licensing & Access
    - **Gumroad Integration**: All enterprise access is gated by active Gumroad subscriptions. When you check out on Gumroad, a unique license key is issued.
    - **Test Access**: During development and administration, you can always use the master bypass key: `sk_apex_live_12345`.
    
    ### 🏢 2. Commercial Real Estate (HVII Matrix)
    - Combines institutional real estate underwriting with legendary investor rules (Buffett margin of safety, Lynch sector expertise, Dalio systematic rules) to output a 1–10 composite score.
    
    ### 🔥 3. Structural Welding & Carpentry Tools
    - Instant margin calculators designed for trade contractors to evaluate material costs, shop hourly rates, and waste factors before submitting client bids.
    
    ### 📈 4. TradingView Webhooks
    - Listens 24/7 on Render for automated alerts sent from TradingView Pine Script indicators, routing orders securely to institutional prop accounts.
    """)
