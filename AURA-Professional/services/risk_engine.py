def calculate_risk_score(company_data):
    """Enhanced risk calculation"""
    
    risk_score = 0
    risk_factors = []
    
    # Revenue analysis
    revenue = company_data.get("revenue", 0)
    if revenue < 10:
        risk_score += 30
        risk_factors.append("⚠️ Low revenue base (<$10M)")
    elif revenue < 50:
        risk_score += 15
        risk_factors.append("ℹ️ Moderate revenue ($10M-$50M)")
    else:
        risk_factors.append("✅ Strong revenue base (>$50M)")
    
    # Loan-to-revenue ratio
    loan_amount = company_data.get("loan_amount", 0)
    if revenue > 0:
        ltv = (loan_amount / revenue) * 100
        if ltv > 50:
            risk_score += 25
            risk_factors.append(f"⚠️ High loan-to-revenue ratio ({ltv:.1f}%)")
        elif ltv > 25:
            risk_score += 10
            risk_factors.append(f"ℹ️ Moderate leverage ({ltv:.1f}%)")
        else:
            risk_factors.append(f"✅ Conservative leverage ({ltv:.1f}%)")
    
    # Industry risk
    high_risk_industries = ["Energy", "Hospitality", "Retail"]
    industry = company_data.get("industry", "")
    if industry in high_risk_industries:
        risk_score += 20
        risk_factors.append(f"⚠️ {industry} sector volatility")
    else:
        risk_factors.append(f"✅ {industry} sector stability")
    
    # Purpose risk
    if company_data.get("purpose") == "Working Capital":
        risk_score += 10
        risk_factors.append("ℹ️ Working capital refinancing risk")
    
    # Determine risk level
    if risk_score > 60:
        risk_level = "HIGH RISK"
        color = "🔴"
    elif risk_score > 35:
        risk_level = "MODERATE RISK"
        color = "🟡"
    else:
        risk_level = "LOW RISK"
        color = "🟢"
    
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "color": color,
        "risk_factors": risk_factors,
        "recommendation": "Proceed with caution" if risk_score > 60 else "Proceed with standard terms" if risk_score > 35 else "Proceed"
    }