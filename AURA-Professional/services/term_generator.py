def generate_loan_terms(company_data, risk_analysis):
    """Generate loan terms based on risk analysis"""
    
    risk_score = risk_analysis["risk_score"]
    
    # Determine tenor
    if risk_score > 60:
        tenor = "3 years"
    elif risk_score > 35:
        tenor = "5 years"
    else:
        tenor = "7 years"
    
    # Determine interest margin
    if risk_score > 60:
        margin = "SOFR + 350 bps"
    elif risk_score > 35:
        margin = "SOFR + 250 bps"
    else:
        margin = "SOFR + 175 bps"
    
    # Base covenants
    covenants = ["Debt Service Coverage Ratio (DSCR) > 1.2x"]
    
    # Add covenants based on risk
    if risk_score > 35:
        covenants.append("Minimum liquidity of $2M at all times")
        covenants.append("Quarterly financial reporting required")
    
    if risk_score > 60:
        covenants.append("No dividends without lender approval")
        covenants.append("Maximum Capital Expenditure limit")
    
    # Purpose-specific covenants
    if company_data.get("purpose") == "Acquisition":
        covenants.append("No additional acquisitions without lender approval")
    
    if company_data.get("purpose") == "Working Capital":
        covenants.append("Inventory turnover monitoring")
    
    return {
        "tenor": tenor,
        "interest_margin": margin,
        "amortization": "Quarterly principal payments",
        "collateral": "First lien on all company assets",
        "covenants": covenants
    }