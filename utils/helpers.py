from datetime import datetime
import json

def format_currency(amount, currency="USD"):
    """Format number as currency"""
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "EUR":
        return f"€{amount:,.2f}"
    elif currency == "GBP":
        return f"£{amount:,.2f}"
    elif currency == "INR":
        return f"₹{amount:,.2f}"
    else:
        return f"{amount:,.2f}"

def format_percentage(value):
    """Format number as percentage"""
    return f"{value:.2f}%"

def calculate_loan_to_value(loan_amount, asset_value):
    """Calculate Loan-to-Value ratio"""
    if asset_value == 0:
        return 0
    return (loan_amount / asset_value) * 100

def calculate_payment(principal, annual_rate, years):
    """Calculate monthly payment for a loan"""
    monthly_rate = annual_rate / 12 / 100
    num_payments = years * 12
    
    if monthly_rate == 0:
        return principal / num_payments
    
    payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / \
              ((1 + monthly_rate) ** num_payments - 1)
    
    return payment

def get_risk_color(risk_score):
    """Get color based on risk score"""
    if risk_score >= 60:
        return "#dc3545"  # Red
    elif risk_score >= 35:
        return "#ffc107"  # Yellow
    else:
        return "#28a745"  # Green

def get_risk_emoji(risk_level):
    """Get emoji based on risk level"""
    if risk_level == "HIGH RISK":
        return "🔴"
    elif risk_level == "MODERATE RISK":
        return "🟡"
    else:
        return "🟢"

def save_to_json(filename, data):
    """Save data to JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving to JSON: {e}")
        return False

def load_from_json(filename):
    """Load data from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading from JSON: {e}")
        return []

def generate_unique_id(prefix="AURA"):
    """Generate unique ID with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}-{timestamp}"

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def truncate_text(text, max_length=50):
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def time_ago(timestamp):
    """Convert timestamp to 'time ago' format"""
    try:
        dt = datetime.fromisoformat(timestamp)
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 365:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
        elif diff.days > 30:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    except:
        return "Unknown"