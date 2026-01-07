import streamlit as st
from services.term_generator import generate_loan_terms
from services.explanation_engine import generate_explanation
from utils.pdf_generator import generate_term_sheet_pdf
from datetime import datetime
import json

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("📄 Term Sheet Generator")
st.markdown("### AI-Powered Loan Term Structuring")

# Check if risk analysis exists
if not st.session_state.get("risk_analysis"):
    st.warning("⚠️ Please complete risk analysis first")
    if st.button("🔍 Go to Risk Analysis"):
        st.switch_page("pages/3_🔍_Risk_Analysis.py")
    st.stop()

# ✅ FIXED: Check role permissions with proper normalization
user_role = st.session_state.get("user_role") or st.session_state.get("role") or "analyst"
user_role_normalized = str(user_role).strip().lower()

if user_role_normalized not in ["admin", "manager"]:
    st.error("🔒 Term sheet generation is restricted to Admin and Manager roles")
    st.info(f"Your current role: **{user_role}**")
    st.stop()

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Loan Details")
    
    company_data = st.session_state.get("company_data", {})
    risk_analysis = st.session_state.risk_analysis
    
    # Display company info
    st.markdown(f"**Company:** {company_data.get('company_name', 'N/A')}")
    st.markdown(f"**Industry:** {company_data.get('industry', 'N/A')}")
    st.markdown(f"**Revenue:** ${company_data.get('revenue', 0)}M")
    st.markdown(f"**Loan Amount:** ${company_data.get('loan_amount', 0)}M")
    st.markdown(f"**Purpose:** {company_data.get('purpose', 'N/A')}")
    
    st.divider()
    
    # Risk summary
    st.markdown("**Risk Assessment Summary:**")
    risk_level = risk_analysis["risk_level"]
    risk_score = risk_analysis["risk_score"]
    
    if risk_level == "HIGH RISK":
        st.error(f"🔴 {risk_level} ({risk_score}/100)")
    elif risk_level == "MODERATE RISK":
        st.warning(f"🟡 {risk_level} ({risk_score}/100)")
    else:
        st.success(f"🟢 {risk_level} ({risk_score}/100)")
    
    st.divider()
    
    # Additional terms customization
    st.markdown("**Customize Terms (Optional):**")
    
    custom_tenor = st.selectbox(
        "Override Tenor",
        ["Auto (AI Suggested)", "3 years", "5 years", "7 years", "10 years"]
    )
    
    custom_margin = st.selectbox(
        "Override Interest Margin",
        ["Auto (AI Suggested)", "SOFR + 150 bps", "SOFR + 200 bps", "SOFR + 250 bps", "SOFR + 300 bps", "SOFR + 350 bps"]
    )
    
    st.divider()
    
    if st.button("📄 Generate Term Sheet", type="primary", use_container_width=True):
        # Generate terms
        loan_terms = generate_loan_terms(company_data, risk_analysis)
        
        # Apply custom overrides
        if custom_tenor != "Auto (AI Suggested)":
            loan_terms["tenor"] = custom_tenor
        
        if custom_margin != "Auto (AI Suggested)":
            loan_terms["interest_margin"] = custom_margin
        
        # Generate explanation
        explanation = generate_explanation(company_data, risk_analysis, loan_terms)
        
        st.session_state.loan_terms = loan_terms
        st.session_state.explanation = explanation
        
        # Log to audit
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": st.session_state.username,
            "action": "Term Sheet Generated",
            "company": company_data.get("company_name"),
            "tenor": loan_terms["tenor"],
            "margin": loan_terms["interest_margin"]
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
    st.subheader("📑 Generated Term Sheet")
    
    if st.session_state.get("loan_terms"):
        terms = st.session_state.loan_terms
        
        # Display terms
        st.markdown(f"""
### Proposed Loan Terms

**Borrower:** {company_data.get('company_name')}  
**Loan Amount:** ${company_data.get('loan_amount')}M  
**Purpose:** {company_data.get('purpose')}

---

#### Key Terms

**Tenor:** {terms['tenor']}  
**Interest Rate:** {terms['interest_margin']}  
**Amortization:** {terms['amortization']}  
**Collateral:** {terms['collateral']}

#### Financial Covenants
""")
        
        for covenant in terms["covenants"]:
            st.markdown(f"- {covenant}")
        
        st.divider()
        
        # AI Explanation
        with st.expander("💡 AI Reasoning & Explainability", expanded=True):
            st.markdown(st.session_state.explanation)
        
        st.divider()
        
        # Download options
        st.markdown("**📥 Download Options:**")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            # Text version
            term_sheet_text = f"""
TERM SHEET
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Generated by: {st.session_state.full_name}

BORROWER INFORMATION
Company Name: {company_data.get('company_name')}
Industry: {company_data.get('industry')}
Annual Revenue: ${company_data.get('revenue')}M

LOAN DETAILS
Loan Amount: ${company_data.get('loan_amount')}M
Purpose: {company_data.get('purpose')}

PROPOSED TERMS
Tenor: {terms['tenor']}
Interest Rate: {terms['interest_margin']}
Amortization: {terms['amortization']}
Collateral: {terms['collateral']}

FINANCIAL COVENANTS
{chr(10).join('- ' + c for c in terms['covenants'])}

RISK ASSESSMENT
Risk Level: {risk_analysis['risk_level']}
Risk Score: {risk_analysis['risk_score']}/100
Recommendation: {risk_analysis['recommendation']}
"""
            
            st.download_button(
                label="📄 Download TXT",
                data=term_sheet_text,
                file_name=f"AURA_TermSheet_{company_data.get('company_name', 'Unknown').replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_btn2:
            # PDF version
            pdf_buffer = generate_term_sheet_pdf(
                company_name=company_data.get('company_name'),
                industry=company_data.get('industry'),
                loan_amount=company_data.get('loan_amount'),
                purpose=company_data.get('purpose'),
                risk_analysis=risk_analysis,
                loan_terms=terms
            )
            
            st.download_button(
                label="📄 Download PDF",
                data=pdf_buffer,
                file_name=f"AURA_TermSheet_{company_data.get('company_name', 'Unknown').replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        st.divider()
        
        # Workflow actions
        if user_role_normalized == "admin":  # ✅ FIXED: Use normalized role
            st.markdown("**🔄 Workflow Actions:**")
            
            col_act1, col_act2 = st.columns(2)
            
            with col_act1:
                if st.button("✅ Approve & Finalize", use_container_width=True):
                    st.success("✅ Term sheet approved!")
                    # Add to approval log
            
            with col_act2:
                if st.button("🔄 Send for Review", use_container_width=True):
                    st.info("📤 Sent for manager review")
    
    else:
        st.info("👈 Click **Generate Term Sheet** to proceed")

st.divider()
st.caption("📄 Term Sheet Generator - AURA Professional")
