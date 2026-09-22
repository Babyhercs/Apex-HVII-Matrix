import os
import requests
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from matrix import HighValueInvestorGem

app = FastAPI(
    title="Apex Ecosystem Enterprise API",
    version="2.0.0",
    description="Institutional Real Estate Underwriting, Fabrication Estimators, and Trading Bot Webhooks."
)

GUMROAD_PRODUCT_ID = os.getenv("GUMROAD_PRODUCT_ID", "your_product_id_here")
MASTER_ADMIN_KEY = os.getenv("APEX_MASTER_KEY", "sk_apex_live_12345")

class AssetUnderwritingRequest(BaseModel):
    asset_name: str
    purchase_price: float
    intrinsic_value: float
    down_payment: float
    monthly_gross_income: float
    monthly_expenses: float
    debt_interest_rate: float
    expected_annual_appreciation: float
    market_liquidity_score: float
    project_complexity_score: float
    depreciation_benefit_multiplier: float
    sector_expertise: bool = True
    is_contrarian_play: bool = True
    systematic_model: bool = True

def verify_gumroad_license(license_key: str) -> bool:
    if not license_key:
        return False
    if license_key == MASTER_ADMIN_KEY:
        return True
        
    url = "https://api.gumroad.com/v2/licenses/verify"
    payload = {
        "product_id": GUMROAD_PRODUCT_ID,
        "license_key": license_key
    }
    try:
        response = requests.post(url, data=payload, timeout=5)
        data = response.json()
        return data.get("success", False) and not data.get("purchase", {}).get("refunded", False)
    except Exception:
        return license_key == MASTER_ADMIN_KEY

@app.get("/")
def read_root():
    return {
        "system": "Apex Ecosystem Enterprise Portal",
        "status": "ONLINE",
        "modules": [
            "Commercial Real Estate HVII Matrix",
            "Structural Welding Calculator",
            "Custom Carpentry Estimator",
            "TradingView / FXIFY Prop Bot"
        ]
    }

@app.post("/api/evaluate-real-estate")
def evaluate_real_estate(payload: AssetUnderwritingRequest, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing License Key / Authorization Header.")
    
    license_key = authorization.replace("Bearer ", "").strip()
    
    if not verify_gumroad_license(license_key):
        raise HTTPException(status_code=403, detail="Invalid or expired Gumroad license key.")
        
    engine = HighValueInvestorGem()
    result = engine.evaluate_asset(payload.dict())
    return {
        "status": "success",
        "data": result
    }

@app.post("/api/tradingview-webhook")
def tradingview_webhook(signal_data: dict, authorization: str = Header(None)):
    if not authorization or authorization.replace("Bearer ", "").strip() != MASTER_ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized webhook trigger.")
        
    print(f"[EXECUTION ENGINE] Received Signal: {signal_data}")
    return {
        "status": "executed",
        "signal_received": signal_data,
        "broker": "FXIFY / FTMO Prop Account"
    }
