import streamlit as st
from auth.users import authenticate

def show_login_page():
    """Display professional login page"""
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>🏦</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>AURA</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>AI Unified Risk & Loan Origination Assistant</p>", unsafe_allow_html=True)
        
        st.divider()
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                submit = st.form_submit_button("🔐 Login", use_container_width=True)
            
            with col_btn2:
                st.form_submit_button("ℹ️ Demo Credentials", use_container_width=True)
        
        if submit:
            if username and password:
                user_data = authenticate(username, password)
                
                if user_data:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = user_data["role"]
                    st.session_state.full_name = user_data["full_name"]
                    st.session_state.email = user_data["email"]
                    st.success(f"✅ Welcome back, {user_data['full_name']}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            else:
                st.warning("⚠️ Please enter both username and password")
        
        # Demo credentials
        with st.expander("📋 Demo Credentials"):
            st.markdown("""
            **Admin Access:**
            - Username: `admin`
            - Password: `admin123`
            
            **Analyst Access:**
            - Username: `analyst`
            - Password: `risk123`
            
            **Manager Access:**
            - Username: `manager`
            - Password: `manager123`
            """)

def logout():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.full_name = None
    st.session_state.email = None
    st.rerun()