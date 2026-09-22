import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
import requests
from matrix import HighValueInvestorGem

app = FastAPI(title="Apex Ecosystem Core Engine API", version="2.0")

GUMROAD_PRODUCT_PERMALINK = "frccez"
MASTER_ADMIN_KEY = os.getenv("APEX_MASTER_KEY", "sk_apex_live_12345")

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

def verify_gumroad_license(license_key: str) -> bool:
    if not license_key:
        return False
    if MASTER_ADMIN_KEY and license_key == MASTER_ADMIN_KEY:
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

gem_engine = HighValueInvestorGem()

@app.get("/")
def root():
    return {"status": "online", "system": "Apex Ecosystem Core Engine API"}

@app.post("/api/v1/evaluate")
async def evaluate_property(data: PropertyData, x_apex_api_key: str = Header(None)):
    if not verify_gumroad_license(x_apex_api_key):
        raise HTTPException(status_code=401, detail="Invalid or inactive Gumroad license key.")
    return gem_engine.evaluate_asset(data.dict())