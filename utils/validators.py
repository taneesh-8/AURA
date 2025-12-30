def validate_company_data(company_data):
    """Validate company information"""
    errors = []
    
    # Required fields
    if not company_data.get("company_name"):
        errors.append("Company name is required")
    
    if not company_data.get("industry"):
        errors.append("Industry is required")
    
    # Numeric validations
    revenue = company_data.get("revenue", 0)
    if revenue <= 0:
        errors.append("Revenue must be greater than 0")
    
    loan_amount = company_data.get("loan_amount", 0)
    if loan_amount <= 0:
        errors.append("Loan amount must be greater than 0")
    
    # Business logic validations
    if revenue > 0 and loan_amount > 0:
        ltv = (loan_amount / revenue) * 100
        if ltv > 100:
            errors.append(f"Loan amount (${loan_amount}M) exceeds annual revenue (${revenue}M)")
    
    years_in_business = company_data.get("years_in_business", 0)
    if years_in_business < 0:
        errors.append("Years in business cannot be negative")
    
    return errors

def validate_financial_data(financial_data):
    """Validate financial metrics"""
    errors = []
    
    ebitda = financial_data.get("ebitda", 0)
    if ebitda < 0:
        errors.append("EBITDA cannot be negative for this analysis")
    
    debt_service = financial_data.get("debt_service", 0)
    if debt_service < 0:
        errors.append("Debt service cannot be negative")
    
    total_debt = financial_data.get("total_debt", 0)
    if total_debt < 0:
        errors.append("Total debt cannot be negative")
    
    ebit = financial_data.get("ebit", 0)
    interest_expense = financial_data.get("interest_expense", 0)
    
    if ebit < 0:
        errors.append("EBIT is negative - indicates operating losses")
    
    if interest_expense < 0:
        errors.append("Interest expense cannot be negative")
    
    # Ratio validations
    if debt_service > 0 and ebitda > 0:
        dscr = ebitda / debt_service
        if dscr < 0.5:
            errors.append(f"DSCR of {dscr:.2f} is critically low")
    
    return errors

def validate_user_role(required_role, user_role):
    """Check if user has required role"""
    role_hierarchy = {
        "Admin": 3,
        "Manager": 2,
        "Analyst": 1
    }
    
    required_level = role_hierarchy.get(required_role, 0)
    user_level = role_hierarchy.get(user_role, 0)
    
    return user_level >= required_level

def validate_file_upload(file):
    """Validate uploaded file"""
    errors = []
    
    if not file:
        errors.append("No file selected")
        return errors
    
    # Check file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    if file.size > max_size:
        errors.append(f"File size ({file.size / 1024 / 1024:.2f}MB) exceeds maximum allowed (10MB)")
    
    # Check file extension
    allowed_extensions = ['pdf', 'xlsx', 'xls', 'csv', 'jpg', 'png', 'jpeg', 'docx']
    file_extension = file.name.split('.')[-1].lower()
    
    if file_extension not in allowed_extensions:
        errors.append(f"File type '.{file_extension}' not allowed. Allowed: {', '.join(allowed_extensions)}")
    
    return errors

def validate_loan_terms(loan_terms):
    """Validate loan term structure"""
    errors = []
    
    if not loan_terms.get("tenor"):
        errors.append("Tenor is required")
    
    if not loan_terms.get("interest_margin"):
        errors.append("Interest margin is required")
    
    if not loan_terms.get("covenants"):
        errors.append("At least one covenant is required")
    elif len(loan_terms["covenants"]) == 0:
        errors.append("At least one covenant must be defined")
    
    return errors