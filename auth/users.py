import streamlit as st

# User database with roles
USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",  # CHANGED: lowercase for consistency
        "full_name": "John Admin",
        "email": "admin@aura.ai"
    },
    "analyst": {
        "password": "risk123",
        "role": "analyst",  # CHANGED: lowercase for consistency
        "full_name": "Sarah Analyst",
        "email": "analyst@aura.ai"
    },
    "manager": {
        "password": "manager123",
        "role": "manager",  # CHANGED: lowercase for consistency
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

def show_login_page():
    """Display login page"""
    st.title("🏦 AURA")
    st.markdown("### AI Unified Risk & Loan Origination Assistant")
    
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔐 Login")
        
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        if st.button("Login", type="primary", width="stretch"):
            user_info = authenticate(username, password)
            
            if user_info:
                # Set ALL session state variables
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = user_info["role"]
                st.session_state.user_role = user_info["role"]  # CRITICAL: Set this!
                st.session_state.full_name = user_info["full_name"]
                st.session_state.email = user_info["email"]
                
                st.success(f"✅ Welcome, {user_info['full_name']}!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
        
        st.divider()
        
        st.info("""
        *Demo Credentials:*
        - *Admin:* admin / admin123
        - *Analyst:* analyst / risk123
        - *Manager:* manager / manager123
        """)
        
        st.caption("🔒 Secure Authentication System")


def logout():
    """Clear session state and logout"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.user_role = None  # CRITICAL: Clear this!
    st.session_state.full_name = None
    st.session_state.email = None
    st.rerun()
