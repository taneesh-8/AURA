import streamlit as st
from services.risk_engine import calculate_risk_score
from services.llm_integration import generate_llm_explanation
from datetime import datetime

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

# Initialize session state
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

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
            
            # Log to audit (session state only)
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "user": st.session_state.username,
                "action": "Risk Analysis",
                "company": company_name,
                "risk_score": risk_result["risk_score"],
                "risk_level": risk_result["risk_level"]
            }
            
            st.session_state.audit_log.append(audit_entry)
            
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

# AI EXPLANATION SECTION - NEW FEATURE!
st.divider()

if st.session_state.get("risk_analysis") and st.session_state.get("company_data"):
    st.subheader("🤖 AI-Powered Credit Analysis")
    
    if st.button("✨ Generate AI Explanation", type="secondary", use_container_width=True):
        with st.spinner("🧠 AI is analyzing the credit profile..."):
            try:
                # Prepare data for LLM
                company_data = st.session_state.company_data
                risk_analysis = st.session_state.risk_analysis
                
                # Create dummy loan terms for explanation
                loan_terms = {
                    "tenor": "36 months",
                    "interest_margin": "7.5%",
                    "amortization": "Monthly",
                    "covenants": ["Debt Service Coverage > 1.25x", "Leverage < 3.0x"]
                }
                
                # Generate AI explanation
                ai_explanation = generate_llm_explanation(company_data, risk_analysis, loan_terms)
                
                # Store in session state
                st.session_state.ai_explanation = ai_explanation
                
                # Log AI usage
                audit_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "user": st.session_state.username,
                    "action": "AI Explanation Generated",
                    "company": company_data["company_name"]
                }
                
                st.session_state.audit_log.append(audit_entry)
                
                st.success("✅ AI analysis complete!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ AI Error: {str(e)}")
                st.info("💡 Falling back to rule-based explanation...")
    
    # Display AI explanation if available
    if st.session_state.get("ai_explanation"):
        st.markdown("---")
        st.markdown("### 📊 Detailed Credit Assessment")
        st.markdown(st.session_state.ai_explanation)
        
        # Download button
        st.download_button(
            label="📥 Download Analysis",
            data=st.session_state.ai_explanation,
            file_name=f"credit_analysis_{st.session_state.company_data['company_name'].replace(' ', '_')}.txt",
            mime="text/plain"
        )

st.divider()
st.caption("🤖 Powered by AURA AI Risk Engine")
