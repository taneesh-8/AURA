import streamlit as st
from datetime import datetime
import pandas as pd

# 1. SECURITY CHECK
if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

# 2. STRICT ROLE IDENTIFICATION
# We strip whitespace and force lowercase to prevent "Manager " or "MANAGER" from failing
raw_role = st.session_state.get("user_role") or st.session_state.get("role") or "analyst"
user_role = str(raw_role).strip().lower()

st.title("🔄 Approval Workflow")
st.markdown(f"### Credit Decision Review & Approval Process")
st.caption(f"Logged in as: **{st.session_state.get('username')}** | Role: **{user_role.upper()}**")

# Initialize session state for approvals
if "pending_approvals" not in st.session_state:
    st.session_state.pending_approvals = []

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

st.divider()

# 3. SUBMISSION SECTION (Available to Analysts)
if st.session_state.get("risk_analysis") and st.session_state.get("company_data"):
    with st.expander("📤 Submit Current Analysis for Approval", expanded=False):
        company = st.session_state.company_data
        risk = st.session_state.risk_analysis
        
        st.write(f"**Company:** {company['company_name']}")
        st.write(f"**Risk Score:** {risk['risk_score']}/100")
        st.write(f"**Loan Amount:** ${company['loan_amount']}M")
        
        notes = st.text_area("Additional Notes", placeholder="Add any comments for the manager...")
        
        if st.button("📨 Submit for Approval", type="primary"):
            approval_request = {
                "id": len(st.session_state.pending_approvals) + 1,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "submitted_by": st.session_state.username,
                "company_name": company['company_name'],
                "loan_amount": company['loan_amount'],
                "risk_score": risk['risk_score'],
                "risk_level": risk['risk_level'],
                "status": "Pending",
                "notes": notes
            }
            
            st.session_state.pending_approvals.append(approval_request)
            
            # Log action
            st.session_state.audit_log.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "User": st.session_state.username,
                "Role": user_role,
                "Action": "SUBMITTED",
                "Company": company['company_name']
            })
            
            st.success("✅ Submitted for approval!")
            st.rerun()

st.divider()

# 4. PENDING APPROVALS (Manager/Admin Only see Buttons)
st.subheader("📋 Pending Approvals")

if st.session_state.pending_approvals:
    pending_items = [a for a in st.session_state.pending_approvals if a["status"] == "Pending"]
    
    if not pending_items:
        st.info("📭 No pending approvals at this time.")
    
    for approval in pending_items:
        with st.expander(f"🔍 {approval['company_name']} - ${approval['loan_amount']}M", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Risk Score", f"{approval['risk_score']}/100")
                st.write(f"**Level:** {approval['risk_level']}")
                st.write(f"**Submitted by:** {approval['submitted_by']}")
            with col2:
                st.write(f"**Date:** {approval['timestamp']}")
                if approval.get('notes'):
                    st.info(f"**Notes:** {approval['notes']}")
            
            st.divider()
            
            # --- THE ACCESS CONTROL GATE ---
            if user_role in ["manager", "admin"]:
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"✅ Approve ##{approval['id']}", key=f"app_{approval['id']}", use_container_width=True, type="primary"):
                        approval["status"] = "Approved"
                        st.session_state.audit_log.append({
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User": st.session_state.username,
                            "Role": user_role,
                            "Action": "APPROVED",
                            "Company": approval['company_name']
                        })
                        st.success(f"Approved {approval['company_name']}")
                        st.rerun()
                
                with col_btn2:
                    if st.button(f"❌ Reject ##{approval['id']}", key=f"rej_{approval['id']}", use_container_width=True):
                        approval["status"] = "Rejected"
                        st.session_state.audit_log.append({
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "User": st.session_state.username,
                            "Role": user_role,
                            "Action": "REJECTED",
                            "Company": approval['company_name']
                        })
                        st.error(f"Rejected {approval['company_name']}")
                        st.rerun()
            else:
                st.warning("🔒 **Read-Only:** Only Managers or Admins can Approve/Reject.")
else:
    st.info("📭 No data available.")

st.divider()

# 5. RECENT DECISIONS & STATS
st.subheader("📊 Recent Decisions")
completed = [a for a in st.session_state.pending_approvals if a["status"] in ["Approved", "Rejected"]]

if completed:
    df_recent = pd.DataFrame(completed)[["company_name", "loan_amount", "status", "risk_score"]]
    st.table(df_recent.tail(5))
else:
    st.info("No completed decisions yet.")

# 6. SYSTEM AUDIT LOG (Required for Demo)
st.divider()
st.subheader("📜 Compliance Audit Trail")
if st.session_state.audit_log:
    # Convert list of dicts to a DataFrame for professional display
    audit_df = pd.DataFrame(st.session_state.audit_log)
    st.dataframe(audit_df, use_container_width=True)
    st.caption("This log provides a permanent record for regulatory compliance.")
else:
    st.info("Audit log is currently empty.")

st.divider()
st.caption("🤖 Powered by AURA Approval Engine | End-to-End Governance")
