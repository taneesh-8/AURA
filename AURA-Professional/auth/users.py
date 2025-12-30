# User database with roles
USERS = {
    "admin": {
        "password": "admin123",
        "role": "Admin",
        "full_name": "John Admin",
        "email": "admin@aura.ai"
    },
    "analyst": {
        "password": "risk123",
        "role": "Analyst",
        "full_name": "Sarah Analyst",
        "email": "analyst@aura.ai"
    },
    "manager": {
        "password": "manager123",
        "role": "Manager",
        "full_name": "Michael Manager",
        "email": "manager@aura.ai"
    }
}

def authenticate(username, password):
    """Authenticate user credentials"""
    if username in USERS:
        if USERS[username]["password"] == password:
            return USERS[username]
    return None

def get_user_info(username):
    """Get user information"""
    return USERS.get(username, None)