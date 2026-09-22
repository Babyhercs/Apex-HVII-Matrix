import math
from typing import Dict, Any

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

    def evaluate_asset(self, asset_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs a Presidential-grade matrix evaluation including tax/friction modeling
        and elite investor heuristic overrides.
        """
        price = asset_metadata.get("purchase_price", 0.0)
        intrinsic_value = asset_metadata.get("intrinsic_value", price) 
        down_payment = asset_metadata.get("down_payment", price)
        debt_principal = price - down_payment
        
        # 1. Stress Test: Bad-Case Scenario
        friction_factor = asset_metadata.get("project_complexity_score", 5.0) / 10.0
        bad_case_impact = 1 - (friction_factor * 0.20) 
        
        gross_annual_income = (asset_metadata.get("monthly_gross_income", 0.0) * 12) * bad_case_impact
        annual_expenses = asset_metadata.get("monthly_expenses", 0.0) * 12
        
        # Realistic annual debt service / interest cost calculation
        annual_debt_service = debt_principal * asset_metadata.get("debt_interest_rate", 0.0)
        net_cash_flow = (gross_annual_income - annual_expenses) - annual_debt_service
        
        # 2. Tax Efficiency Multiplier
        tax_shield = asset_metadata.get("depreciation_benefit_multiplier", 1.0)
        
        # 3. Kiyosaki Score
        cash_on_cash_return = (net_cash_flow / down_payment) if down_payment > 0 else 0.0
        kiyosaki_score = ((cash_on_cash_return * 10) * tax_shield)
        
        # Applying Heuristics to Kiyosaki Score
        if price <= (intrinsic_value * 0.8):
            kiyosaki_score *= self.heuristics["Buffett_Margin_Safety"]
        if asset_metadata.get("sector_expertise", False):
            kiyosaki_score *= self.heuristics["Lynch_Expertise"]
            
        kiyosaki_score = max(0.0, min(10.0, kiyosaki_score))

        # 4. Schwab Score
        liquidity = asset_metadata.get("market_liquidity_score", 5.0)
        appreciation = asset_metadata.get("expected_annual_appreciation", 0.0)
        schwab_score = (liquidity * 0.4) + (appreciation * 100) - (friction_factor * 2)
        
        # Applying Heuristics to Schwab Score
        if asset_metadata.get("stable_macro_zone", True):
            schwab_score *= self.heuristics["Soros_Macro_Stability"]
        if asset_metadata.get("is_contrarian_play", False):
            schwab_score *= self.heuristics["Templeton_Contrarian"]
            
        schwab_score = max(0.0, min(10.0, schwab_score))

        # 5. Composite HVII Index
        hvii = (kiyosaki_score * self.kiyosaki_weight) + (schwab_score * self.schwab_weight)
        
        # Final Dalio Systemic Check
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

if __name__ == "__main__":
    gem_engine = HighValueInvestorGem()
    
    commercial_rehab_project = {
        "asset_name": "Industrial Warehouse Expansion & Structural Refit",
        "purchase_price": 1250000.0,
        "intrinsic_value": 1600000.0, 
        "down_payment": 250000.0,
        "monthly_gross_income": 22000.0,
        "monthly_expenses": 4500.0,
        "debt_interest_rate": 0.075,
        "expected_annual_appreciation": 0.04,
        "market_liquidity_score": 4.0, 
        "project_complexity_score": 6.5, 
        "depreciation_benefit_multiplier": 1.45, 
        "sector_expertise": True,     
        "is_contrarian_play": True,    
        "systematic_model": True       
    }

    results = gem_engine.evaluate_asset(commercial_rehab_project)
    print("--- Running Presidential Matrix ---")
    for k, v in results.items():
        print(f"{k.replace('_', ' ').title()}: {v}")
