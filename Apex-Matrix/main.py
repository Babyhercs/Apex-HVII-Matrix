import math
from typing import Dict, Any
from fastapi import FastAPI
from pydantic import BaseModel, Field

# 1. Initialize Web App
app = FastAPI(title="Apex HVII Property Matrix API")

# 2. Define Data Schemas
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

class TradeAlert(BaseModel):
    action: str
    symbol: str
    volume: float
    sl: float
    tp: float

# 3. The Core Matrix Engine
class HighValueInvestorGem:
    """
    Presidential-Tier Analysis Engine: Evaluates assets via enterprise-grade 
    risk assessment, tax-efficiency modeling, and project friction variables.
    Integrated with elite investor heuristics.
    """
    
    def __init__(self, investor_profile: str = "Presidential Aggressive"):
        self.profile = investor_profile
        self.kiyosaki_weight = 0.50
        self.schwab_weight = 0.50
        
        # Elite Investor Heuristics (Multipliers)
        self.heuristics = {
            "Buffett_Margin_Safety": 1.1,  # Bonus for buying below intrinsic value
            "Soros_Macro_Stability": 1.05, # Bonus for low-risk zone assets
            "Lynch_Expertise": 1.1,        # Bonus for high-conviction/experienced sectors
            "Templeton_Contrarian": 1.05,  # Bonus for high-pessimism/undervalued plays
            "Dalio_Systematic": 1.05       # Bonus for systematic/diversified models
        }

    def evaluate_asset(self, data: PropertyData) -> Dict[str, Any]:
        """
        Runs a Presidential-grade matrix evaluation including tax/friction modeling
        and elite investor heuristic overrides.
        """
        price = data.purchase_price
        intrinsic_value = data.intrinsic_value
        down_payment = data.down_payment
        debt_principal = price - down_payment
        
        # 1. Stress Test: Bad-Case Scenario
        friction_factor = data.project_complexity_score / 10.0
        bad_case_impact = 1 - (friction_factor * 0.20) 
        
        gross_annual_income = (data.monthly_gross_income * 12) * bad_case_impact
        annual_expenses = data.monthly_expenses * 12
        
        # Realistic annual debt service / interest cost calculation
        annual_debt_service = debt_principal * data.debt_interest_rate
        net_cash_flow = (gross_annual_income - annual_expenses) - annual_debt_service
        
        # 2. Tax Efficiency & Kiyosaki Score
        cash_on_cash_return = (net_cash_flow / down_payment) if down_payment > 0 else 0.0
        kiyosaki_score = ((cash_on_cash_return * 10) * data.depreciation_benefit_multiplier)
        
        # Applying Heuristics to Kiyosaki Score
        if price <= (intrinsic_value * 0.8):
            kiyosaki_score *= self.heuristics["Buffett_Margin_Safety"]
        if data.sector_expertise:
            kiyosaki_score *= self.heuristics["Lynch_Expertise"]
            
        kiyosaki_score = max(0.0, min(10.0, kiyosaki_score))

        # 3. Schwab Score
        schwab_score = (data.market_liquidity_score * 0.4) + (data.expected_annual_appreciation * 100) - (friction_factor * 2)
        
        # Applying Heuristics to Schwab Score
        if data.is_contrarian_play:
            schwab_score *= self.heuristics["Templeton_Contrarian"]
            
        schwab_score = max(0.0, min(10.0, schwab_score))

        # 4. Composite HVII Index
        hvii = (kiyosaki_score * self.kiyosaki_weight) + (schwab_score * self.schwab_weight)
        
        # Final Dalio Systemic Check
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

# 4. Web Endpoints
@app.get("/")
def root():
    return {"status": "online", "system": "Apex HVII Engine"}

@app.post("/api/v1/evaluate")
async def evaluate(data: PropertyData):
    return gem_engine.evaluate_asset(data)

@app.post("/api/v1/webhook")
async def receive_tradingview_alert(alert: TradeAlert):
    """
    Receives JSON alerts from TradingView Pine Script for automated trade execution.
    """
    print(f"\n[TRADINGVIEW WEBHOOK] Action: {alert.action.upper()} | Symbol: {alert.symbol} | Vol: {alert.volume} | SL: {alert.sl} | TP: {alert.tp}")
    
    # Insert broker / prop firm API execution integration here if needed
    
    return {
        "status": "success", 
        "message": f"Successfully processed {alert.action} order for {alert.symbol}"
    }
