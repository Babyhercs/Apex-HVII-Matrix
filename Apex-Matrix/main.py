import math
from typing import Dict, Any
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
import requests

app = FastAPI(title="Apex Ecosystem Universal Portfolio Engine")

GUMROAD_PRODUCT_PERMALINK = "frccez"

# --- 1. UNIFIED API PAYLOAD MODEL ---
class UniversalProjectPayload(BaseModel):
    project_type: str = Field(..., description="real_estate, welding_fabrication, carpentry_stage, or trading_bot")
    project_name: str
    
    # Real Estate & General Financials
    purchase_price: float = Field(default=0.0)
    intrinsic_value: float = Field(default=0.0)
    down_payment: float = Field(default=0.0)
    monthly_gross_income: float = Field(default=0.0)
    monthly_expenses: float = Field(default=0.0)
    debt_interest_rate: float = Field(default=0.0)
    expected_annual_appreciation: float = Field(default=0.0)
    market_liquidity_score: float = Field(default=5.0, ge=1, le=10)
    project_complexity_score: float = Field(default=5.0, ge=1, le=10)
    depreciation_benefit_multiplier: float = Field(default=1.0)
    
    # Trade / Fabrication Specifics (Welding & Carpentry)
    material_cost: float = Field(default=0.0)
    labor_hours: float = Field(default=0.0)
    hourly_rate: float = Field(default=75.0)
    quoted_contract_price: float = Field(default=0.0)
    
    # Heuristics & Flags
    sector_expertise: bool = Field(default=True)
    is_contrarian_play: bool = Field(default=False)
    systematic_model: bool = Field(default=True)
    stable_macro_zone: bool = Field(default=True)

# --- 2. GUMROAD LICENSE VERIFICATION ---
def verify_gumroad_license(license_key: str) -> bool:
    if not license_key:
        return False
    if license_key == "sk_apex_live_12345":  # Master admin backdoor key
        return True
    
    verify_url = "https://api.gumroad.com/v2/licenses/verify"
    payload = {"product_permalink": GUMROAD_PRODUCT_PERMALINK, "license_key": license_key}
    try:
        response = requests.post(verify_url, data=payload)
        data = response.json()
        if data.get("success") and not data.get("purchase", {}).get("refunded"):
            return True
    except Exception:
        pass
    return False

# --- 3. EXPANDED APEX MULTI-PROJECT ENGINE ---
class ApexPortfolioEngine:
    def __init__(self):
        self.heuristics = {
            "Buffett_Margin_Safety": 1.1,
            "Soros_Macro_Stability": 1.05,
            "Lynch_Expertise": 1.1,
            "Templeton_Contrarian": 1.05,
            "Dalio_Systematic": 1.05
        }

    def evaluate_real_estate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        price = data.get("purchase_price", 0.0)
        intrinsic_value = data.get("intrinsic_value", price) 
        down_payment = data.get("down_payment", price)
        debt_principal = price - down_payment
        
        friction_factor = data.get("project_complexity_score", 5.0) / 10.0
        bad_case_impact = 1 - (friction_factor * 0.20) 
        
        gross_annual_income = (data.get("monthly_gross_income", 0.0) * 12) * bad_case_impact
        annual_expenses = data.get("monthly_expenses", 0.0) * 12
        annual_debt_service = debt_principal * data.get("debt_interest_rate", 0.0)
        net_cash_flow = (gross_annual_income - annual_expenses) - annual_debt_service
        
        tax_shield = data.get("depreciation_benefit_multiplier", 1.0)
        cash_on_cash_return = (net_cash_flow / down_payment) if down_payment > 0 else 0.0
        
        score = ((cash_on_cash_return * 10) * tax_shield)
        if price <= (intrinsic_value * 0.8):
            score *= self.heuristics["Buffett_Margin_Safety"]
        if data.get("sector_expertise", False):
            score *= self.heuristics["Lynch_Expertise"]
            
        score = max(0.0, min(10.0, score))
        verdict = "STRONG ACQUISITION TARGET" if score >= 7.5 else "HOLD / CONDITIONAL" if score >= 5.0 else "LIQUIDITY DRAIN"
        
        return {
            "project_name": data.get("project_name"),
            "category": "Commercial Real Estate",
            "index_score": round(score, 2),
            "projected_metric": f"${net_cash_flow:,.2f} annual cash flow",
            "verdict": verdict
        }

    def evaluate_trade_contract(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates profit margins and labor efficiency for welding, metal fab, and carpentry builds."""
        material_cost = data.get("material_cost", 0.0)
        labor_hours = data.get("labor_hours", 0.0)
        hourly_rate = data.get("hourly_rate", 75.0)
        contract_price = data.get("quoted_contract_price", 0.0)
        
        total_cost = material_cost + (labor_hours * hourly_rate)
        gross_profit = contract_price - total_cost
        profit_margin = (gross_profit / contract_price) if contract_price > 0 else 0.0
        
        score = min(10.0, max(0.0, profit_margin * 20))  # 50% margin = 10.0 score
        if data.get("sector_expertise", True):
            score *= self.heuristics["Lynch_Expertise"]
        score = min(10.0, score)
        
        verdict = "HIGH-MARGIN CONTRACT" if profit_margin >= 0.4 else "STANDARD MARGIN" if profit_margin >= 0.2 else "LOW MARGIN / RESTRUCTURE"
        
        return {
            "project_name": data.get("project_name"),
            "category": "Welding & Construction Contracting",
            "index_score": round(score, 2),
            "projected_metric": f"${gross_profit:,.2f} profit ({profit_margin*100:.1f}% margin)",
            "verdict": verdict
        }

    def evaluate_project(self, data: Dict[str, Any]) -> Dict[str, Any]:
        ptype = data.get("project_type", "real_estate")
        if ptype in ["welding_fabrication", "carpentry_stage"]:
            return self.evaluate_trade_contract(data)
        return self.evaluate_real_estate(data)

engine = ApexPortfolioEngine()

# --- 4. ENDPOINTS ---
@app.post("/api/v1/evaluate-project")
async def evaluate_project_endpoint(payload: UniversalProjectPayload, x_apex_api_key: str = Header(None)):
    if not verify_gumroad_license(x_apex_api_key):
        raise HTTPException(status_code=401, detail="Invalid Gumroad license key.")
    return engine.evaluate_project(payload.dict())
