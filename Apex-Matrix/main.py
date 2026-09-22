import math
from typing import Dict, Any
from fastapi import FastAPI
from pydantic import BaseModel, Field

# Initialize Web Server
app = FastAPI(title="Apex HVII Property Matrix API")

# Define Data Input Rules
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

# The Core Matrix
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

    def evaluate_asset(self, data: PropertyData) -> Dict[str, Any]:
        debt_principal = data.purchase_price - data.down_payment
        friction_factor = data.project_complexity_score / 10.0
        bad_case_impact = 1 - (friction_factor * 0.20)
        
        gross_annual_income = (data.monthly_gross_income * 12) * bad_case_impact
        annual_expenses = data.monthly_expenses * 12
        annual_debt_service = debt_principal * data.debt_interest_rate
        net_cash_flow = (gross_annual_income - annual_expenses) - annual_debt_service
        
        cash_on_cash_return = (net_cash_flow / data.down_payment) if data.down_payment > 0 else 0.0
        kiyosaki_score = ((cash_on_cash_return * 10) * data.depreciation_benefit_multiplier)
        
        if data.purchase_price <= (data.intrinsic_value * 0.8):
            kiyosaki_score *= self.heuristics["Buffett_Margin_Safety"]
        if data.sector_expertise:
            kiyosaki_score *= self.heuristics["Lynch_Expertise"]
            
        kiyosaki_score = max(0.0, min(10.0, kiyosaki_score))
        schwab_score = (data.market_liquidity_score * 0.4) + (data.expected_annual_appreciation * 100) - (friction_factor * 2)
        
        if data.is_contrarian_play:
            schwab_score *= self.heuristics["Templeton_Contrarian"]
            
        schwab_score = max(0.0, min(10.0, schwab_score))
        hvii = (kiyosaki_score * self.kiyosaki_weight) + (schwab_score * self.schwab_weight)
        
        if data.systematic_model:
            hvii *= self.heuristics["Dalio_Systematic"]
            
        hvii = max(0.0, min(10.0, hvii))
        verdict = "STRONG ACQUISITION TARGET" if hvii >= 7.5 else "HOLD / CONDITIONAL" if hvii >= 5.0 else "LIQUIDITY DRAIN"
        
        return {
            "asset_name": data.asset_name,
            "hvii_index": round(hvii, 2),
            "stress_tested_cash_flow": round(net_cash_flow, 2),
            "verdict": verdict,
            "risk_profile": "High Friction/High Reward" if friction_factor > 0.7 else "Efficient/Stable"
        }

gem_engine = HighValueInvestorGem()

# API Endpoints
@app.get("/")
def root():
    return {"status": "online", "system": "Apex HVII Engine"}

@app.post("/api/v1/evaluate")
async def evaluate(data: PropertyData):
    return gem_engine.evaluate_asset(data)
