import streamlit as st
from services.risk_engine import calculate_risk_score
import json
from datetime import datetime

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("🔍 Risk Analysis")
st.markdown("### Comprehensive Credit Risk Assessment")

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Company Information")
    
    company_name = st.text_input("Company Name *", placeholder="e.g., ABC Manufacturing Corp")
    
    industry = st.selectbox(
        "Industry *",
        ["Manufacturing", "IT Services", "Healthcare", "Energy", "Retail", "Construction", "Hospitality", "Finance", "Real Estate"]
    )
    
    revenue = st.number_input("Annual Revenue ($M) *", min_value=0.0, value=25.0, step=1.0)
    
    loan_amount = st.number_input("Loan Amount ($M) *", min_value=0.0, value=5.0, step=0.5)
    
    purpose = st.selectbox(
        "Loan Purpose *",
        ["Working Capital", "Equipment Purchase", "Expansion", "Acquisition", "Refinancing", "Real Estate"]
    )
    
    years_in_business = st.number_input("Years in Business", min_value=0, value=5, step=1)
    
    employees = st.number_input("Number of Employees", min_value=0, value=50, step=10)
    
    st.divider()
    
    if st.button("🔍 Analyze Risk", type="primary", use_container_width=True):
        if not company_name:
            st.error("❌ Company name is required")
        else:
            company_data = {
                "company_name": company_name,
                "industry": industry,
                "revenue": revenue,
                "loan_amount": loan_amount,
                "purpose": purpose,
                "years_in_business": years_in_business,
                "employees": employees
            }
            
            risk_result = calculate_risk_score(company_data)
            
            st.session_state.risk_analysis = risk_result
            st.session_state.company_data = company_data
            
            # Log to audit
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "user": st.session_state.username,
                "action": "Risk Analysis",
                "company": company_name,
                "risk_score": risk_result["risk_score"],
                "risk_level": risk_result["risk_level"]
            }
            
            try:
                with open("data/audit_log.json", "r") as f:
                    audit_log = json.load(f)
            except:
                audit_log = []
            
            audit_log.append(audit_entry)
            
            with open("data/audit_log.json", "w") as f:
                json.dump(audit_log, f, indent=2)
            
            st.rerun()

with col2:
    st.subheader("📊 Risk Assessment Results")
    
    if st.session_state.get("risk_analysis"):
        risk = st.session_state.risk_analysis
        
        # Risk score display
        if risk["risk_level"] == "HIGH RISK":
            st.error(f"{risk['color']} **{risk['risk_level']}**")
        elif risk["risk_level"] == "MODERATE RISK":
            st.warning(f"{risk['color']} **{risk['risk_level']}**")
        else:
            st.success(f"{risk['color']} **{risk['risk_level']}**")
        
        # Score gauge
        st.metric("Risk Score", f"{risk['risk_score']}/100")
        
        st.progress(risk['risk_score'] / 100)
        
        st.divider()
        
        st.markdown("**Key Risk Factors:**")
        for factor in risk["risk_factors"]:
            st.markdown(f"- {factor}")
        
        st.divider()
        
        st.info(f"**Recommendation:** {risk['recommendation']}")
        
        # Action buttons
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📄 Generate Term Sheet", use_container_width=True):
                st.switch_page("pages/4_📄_Term_Sheet.py")
        
        with col_btn2:
            if st.button("📈 View Ratios", use_container_width=True):
                st.switch_page("pages/5_📈_Financial_Ratios.py")
    
    else:
        st.info("👈 Enter company details and click **Analyze Risk**")

st.divider()
st.caption("🤖 Powered by AURA AI Risk Engine")