import math
import random
from typing import Dict, Any

class HighValueInvestorGem:
    """
    Presidential-Tier Analysis Engine: Evaluates assets via enterprise-grade 
    risk assessment, tax-efficiency modeling, DSCR, Cap Rate, 5-Year IRR, 
    and Automated Lead Scoring for client acquisition.
    """
    
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
        
        noi = gross_annual_income - annual_expenses
        annual_debt_service = debt_principal * asset_metadata.get("debt_interest_rate", 0.0)
        net_cash_flow = noi - annual_debt_service
        dscr = (noi / annual_debt_service) if annual_debt_service > 0 else 99.9
        cap_rate = (noi / price) * 100 if price > 0 else 0.0
        
        hold_period_years = 5
        appreciation = asset_metadata.get("expected_annual_appreciation", 0.04)
        exit_val = price * ((1 + appreciation) ** hold_period_years)
        
        cumulative_cash_flows = sum([net_cash_flow * ((1.025) ** y) for y in range(hold_period_years)])
        total_cash_returned = down_payment + cumulative_cash_flows + (exit_val - debt_principal)
        equity_multiple = total_cash_returned / down_payment if down_payment > 0 else 0.0
        approx_irr = ((equity_multiple ** (1 / hold_period_years)) - 1) * 100

        tax_shield = asset_metadata.get("depreciation_benefit_multiplier", 1.0)
        cash_on_cash_return = (net_cash_flow / down_payment) if down_payment > 0 else 0.0
        kiyosaki_score = ((cash_on_cash_return * 10) * tax_shield)
        
        if price <= (intrinsic_value * 0.8):
            kiyosaki_score *= self.heuristics["Buffett_Margin_Safety"]
        if asset_metadata.get("sector_expertise", False):
            kiyosaki_score *= self.heuristics["Lynch_Expertise"]
            
        kiyosaki_score = max(0.0, min(10.0, kiyosaki_score))

        liquidity = asset_metadata.get("market_liquidity_score", 5.0)
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
        
        success_count = 0
        iterations = 1000
        for _ in range(iterations):
            rand_income = gross_annual_income * random.uniform(0.85, 1.15)
            rand_exp = annual_expenses * random.uniform(0.90, 1.20)
            if (rand_income - rand_exp - annual_debt_service) > 0:
                success_count += 1
        probability_of_profit = (success_count / iterations) * 100

        verdict = "STRONG ACQUISITION TARGET" if hvii >= 7.5 and dscr >= 1.25 and approx_irr >= 15.0 else "HOLD / CONDITIONAL" if hvii >= 5.0 else "LIQUIDITY DRAIN"
        
        # Automated Client Acquisition Lead Score (0 - 100 scale)
        lead_score = int(min(100, max(0, (hvii * 6) + (approx_irr * 1.5) + (dscr * 5))))
        lead_priority = "HOT LEAD (Immediate Outreach)" if lead_score >= 75 else "WARM LEAD (Nurture)" if lead_score >= 50 else "COLD / DISQUALIFIED"

        return {
            "asset_name": asset_metadata.get("asset_name"),
            "hvii_index": round(hvii, 2),
            "net_operating_income": round(noi, 2),
            "cap_rate_pct": round(cap_rate, 2),
            "dscr": round(dscr, 2),
            "projected_5yr_irr_pct": round(approx_irr, 2),
            "equity_multiple": round(equity_multiple, 2),
            "monte_carlo_success_probability": f"{probability_of_profit:.1f}%",
            "lead_score": lead_score,
            "lead_priority": lead_priority,
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
    print("--- Running Presidential Matrix (Client Acquisition Upgraded) ---")
    for k, v in results.items():
        print(f"{k.replace('_', ' ').title()}: {v}")
