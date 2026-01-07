import streamlit as st
from auth import show_login_page, logout
import pandas as pd

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

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "full_name" not in st.session_state:
    st.session_state.full_name = None

if "email" not in st.session_state:
    st.session_state.email = None

# Authentication gate
if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# Sync user_role with role for compatibility
if st.session_state.role and not st.session_state.user_role:
    st.session_state.user_role = st.session_state.role

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
    
    if st.button("🚪 Logout", width="stretch"):
        logout()

# Main welcome page
st.title("🏦 AURA - AI Unified Risk & Loan Origination Assistant")
st.markdown("### Welcome to the Professional Credit Decisioning Platform")

# Demo mode indicator
if st.session_state.get("company_data") and st.session_state.get("risk_analysis"):
    st.info("🎬 **Demo Mode Active** - Sample data loaded. Try navigating to Risk Analysis or generating a Term Sheet!")

st.divider()

# Demo statistics with realistic data
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Active Users", "24", "+3")
    st.metric("Pending Approvals", "8", "-2")

with col2:
    st.metric("Loans Analyzed", "342", "+27")
    st.metric("Avg Risk Score", "65/100", "↑ 5")

with col3:
    st.metric("Term Sheets Generated", "156", "+18")
    st.metric("Approval Rate", "82%", "↑ 6%")

st.divider()

# Quick actions
st.markdown("### 🚀 Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔍 New Risk Analysis", width="stretch"):
        st.switch_page("pages/3_🔍_Risk_Analysis.py")

with col2:
    if st.button("📄 Generate Term Sheet", width="stretch"):
        st.switch_page("pages/4_📄_Term_Sheet.py")

with col3:
    if st.button("📈 View Ratios", width="stretch"):
        st.switch_page("pages/5_📈_Financial_Ratios.py")

with col4:
    if st.button("🎬 Load Demo Data", width="stretch", type="secondary"):
        # Load demo company for quick demonstration
        demo_company = {
            "company_name": "Tech Innovations Inc",
            "industry": "IT Services",
            "revenue": 12.5,
            "loan_amount": 2.5,
            "purpose": "Expansion",
            "years_in_business": 8,
            "employees": 150
        }
        
        demo_risk = {
            "risk_score": 78,
            "risk_level": "LOW RISK",
            "color": "🟢",
            "risk_factors": [
                "Strong revenue base of $12.5M annually",
                "Established 8-year operational history",
                "Healthy loan-to-revenue ratio of 20%",
                "Growing IT services sector"
            ],
            "recommendation": "APPROVE with favorable terms",
            "debt_to_asset_ratio": 0.35
        }
        
        st.session_state.company_data = demo_company
        st.session_state.risk_analysis = demo_risk
        st.success("✅ Demo data loaded! Go to Risk Analysis to see results.")
        st.balloons()

st.divider()

# Recent activity with realistic demo data
st.markdown("### 📊 Recent Activity")

recent_data = pd.DataFrame({
    "Time": ["15 mins ago", "1 hour ago", "3 hours ago", "5 hours ago", "Today 9:30 AM"],
    "User": ["Sarah Analyst", "Michael Manager", "Sarah Analyst", "John Admin", "Sarah Analyst"],
    "Action": ["Risk Analysis", "Approved Loan", "Generated Term Sheet", "Document Upload", "Risk Analysis"],
    "Company": ["Tech Innovations Inc", "ABC Manufacturing", "Retail Solutions Ltd", "Green Energy Corp", "Healthcare Partners"],
    "Status": ["✅ Complete", "✅ Approved", "✅ Complete", "⏳ Pending Review", "✅ Complete"]
})

st.dataframe(recent_data, hide_index=True)

st.divider()
st.caption("🤖 AURA - Professional AI Credit Decisioning Platform v2.0")
