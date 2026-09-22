import math
import requests
from typing import Dict, Any
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Apex Ecosystem Core Engine API")

GUMROAD_PRODUCT_PERMALINK = "frccez"

# --- 1. DATA MODELS ---
class PropertyData(BaseModel):
    asset_name: str = Field(..., description="Name or address of the asset")
    purchase_price: float = Field(..., gt=0)
    intrinsic_value: float = Field(..., gt=0)
    down_payment: float = Field(..., ge=0)
    monthly_gross_income: float = Field(..., ge=0)
    monthly_expenses: float = Field(..., ge=0)
    debt_interest_rate: float = Field(..., ge=0)
    expected_annual_appreciation: float = Field(..., ge=0)
    market_liquidity_score: float = Field(..., ge=1, le=10)
    project_complexity_score: float = Field(..., ge=1, le=10)
    depreciation_benefit_multiplier: float = Field(default=1.0)
    sector_expertise: bool = Field(default=False)
    is_contrarian_play: bool = Field(default=False)
    systematic_model: bool = Field(default=False)
    stable_macro_zone: bool = Field(default=True)

class TradeAlert(BaseModel):
    action: str  # "buy" or "sell"
    symbol: str  # e.g., "EURUSD", "BTCUSD"
    volume: float  # Lot size / contracts
    sl: float  # Stop Loss price
    tp: float  # Take Profit price

# --- 2. GUMROAD LICENSE VERIFICATION ---
def verify_gumroad_license(license_key: str) -> bool:
    if not license_key:
        return False
    if license_key == "sk_apex_live_12345":  # Master admin backdoor
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

# --- 3. HIGH VALUE INVESTOR GEM ENGINE ---
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

    def evaluate_asset(self, asset_metadata: Dict[str, Any]) -> Dict[str, Any]:
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

# --- 4. API ENDPOINTS ---
@app.get("/")
def root():
    return {"status": "online", "system": "Apex Ecosystem Core Engine"}

@app.post("/api/v1/evaluate")
async def evaluate(data: PropertyData, x_apex_api_key: str = Header(None)):
    if not verify_gumroad_license(x_apex_api_key):
        raise HTTPException(status_code=401, detail="Invalid or inactive Gumroad license key.")
    return gem_engine.evaluate_asset(data.dict())

@app.post("/api/v1/webhook")
async def receive_tradingview_alert(alert: TradeAlert):
    """
    Receives JSON webhooks from TradingView and routes execution logic.
    """
    print(f"\n[TRADINGVIEW WEBHOOK] Action: {alert.action.upper()} | Symbol: {alert.symbol} | Vol: {alert.volume} | SL: {alert.sl} | TP: {alert.tp}")
    
    # Insert DXTrade / Prop Firm execution calls here if needed
    
    return {
        "status": "success",
        "message": f"Successfully processed {alert.action} signal for {alert.symbol}"
    }
