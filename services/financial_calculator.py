def calculate_dscr(ebitda, debt_service):
    """Calculate Debt Service Coverage Ratio"""
    if debt_service == 0:
        return None
    return ebitda / debt_service

def calculate_leverage_ratio(total_debt, ebitda):
    """Calculate Debt/EBITDA"""
    if ebitda == 0:
        return None
    return total_debt / ebitda

def calculate_interest_coverage(ebit, interest_expense):
    """Calculate Interest Coverage Ratio"""
    if interest_expense == 0:
        return None
    return ebit / interest_expense

def calculate_all_ratios(financial_data):
    """Calculate all financial ratios"""
    
    ebitda = financial_data.get("ebitda", 0)
    debt_service = financial_data.get("debt_service", 0)
    total_debt = financial_data.get("total_debt", 0)
    ebit = financial_data.get("ebit", 0)
    interest_expense = financial_data.get("interest_expense", 0)
    
    dscr = calculate_dscr(ebitda, debt_service)
    leverage = calculate_leverage_ratio(total_debt, ebitda)
    interest_coverage = calculate_interest_coverage(ebit, interest_expense)
    
    return {
        "dscr": dscr,
        "leverage_ratio": leverage,
        "interest_coverage": interest_coverage
    }