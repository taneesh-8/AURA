import streamlit as st
from auth import show_login_page, logout

# Page config
st.set_page_config(
    page_title="AURA - AI Loan Origination",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

if "full_name" not in st.session_state:
    st.session_state.full_name = None

# Authentication gate
if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# Sidebar navigation
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.full_name}")
    st.markdown(f"**Role:** {st.session_state.role}")
    st.markdown(f"**Email:** {st.session_state.email}")
    
    st.divider()
    
    st.markdown("### 🧭 Navigation")
    st.markdown("""
    - 🏠 Home
    - 📊 Dashboard
    - 🔍 Risk Analysis
    - 📄 Term Sheet Generator
    - 📈 Financial Ratios
    - 📤 Document Upload
    - 🔄 Approval Workflow
    - 📋 Audit Log
    """)
    
    st.divider()
    
    if st.button("🚪 Logout", use_container_width=True):
        logout()

# Main welcome page
st.title("🏦 AURA - AI Unified Risk & Loan Origination Assistant")
st.markdown("### Welcome to the Professional Credit Decisioning Platform")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Active Users", "3", "+1")
    st.metric("Pending Approvals", "5", "-2")

with col2:
    st.metric("Loans Analyzed", "127", "+12")
    st.metric("Avg Risk Score", "42/100", "↓ 3")

with col3:
    st.metric("Term Sheets", "89", "+8")
    st.metric("Approval Rate", "76%", "↑ 4%")

st.divider()

# Quick actions
st.markdown("### 🚀 Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔍 New Risk Analysis", use_container_width=True):
        st.switch_page("pages/3_🔍_Risk_Analysis.py")

with col2:
    if st.button("📄 Generate Term Sheet", use_container_width=True):
        st.switch_page("pages/4_📄_Term_Sheet.py")

with col3:
    if st.button("📈 View Ratios", use_container_width=True):
        st.switch_page("pages/5_📈_Financial_Ratios.py")

with col4:
    if st.button("📋 Audit Log", use_container_width=True):
        st.switch_page("pages/8_📋_Audit_Log.py")

st.divider()

# Recent activity
st.markdown("### 📊 Recent Activity")

import pandas as pd

recent_data = pd.DataFrame({
    "Time": ["2 hours ago", "5 hours ago", "1 day ago", "2 days ago"],
    "User": ["Sarah Analyst", "John Admin", "Michael Manager", "Sarah Analyst"],
    "Action": ["Risk Analysis", "Term Sheet Generated", "Approval", "Document Upload"],
    "Company": ["ABC Corp", "XYZ Ltd", "Tech Innovations", "Retail Co"],
    "Status": ["✅ Complete", "✅ Complete", "✅ Approved", "⏳ Pending"]
})

st.dataframe(recent_data, use_container_width=True, hide_index=True)

st.divider()

st.caption("🤖 AURA - Professional AI Credit Decisioning Platform v2.0")
