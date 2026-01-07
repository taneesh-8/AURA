import streamlit as st
from datetime import datetime
import pandas as pd

# ==========================================
# 1. PAGE CONFIG & SECURITY
# ==========================================
st.set_page_config(page_title="Manager Approval Portal", layout="wide")

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

# Strict Role-Based Access Control (RBAC)
raw_role = st.session_state.get("user_role") or st.session_state.get("role") or "analyst"
user_role = str(raw_role).strip().lower()

# If the user is an Analyst, block access to the Approval actions
if user_role not in ["manager", "admin"]:
    st.error("🚫 **Access Denied**: Your account level (Analyst) does not have approval authority.")
    st.info("Please contact your system administrator to request Managerial permissions.")
    if st.button("Return to Dashboard"):
        st.switch_page("pages/2_📊_Dashboard.py")
    st.stop()

# ==========================================
# 2. INITIALIZE DATA
# ==========================================
if "pending_approvals" not in st.session_state:
    st.session_state.pending_approvals = []

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

# ==========================================
# 3. HEADER & EXECUTIVE METRICS
# ==========================================
st.title("💼 Manager Approval Portal")
st.markdown("### Credit Committee Decision Engine")

# Calculate metrics for the manager
pending_list = [a for a in st.session_state.pending_approvals if a["status"] == "Pending"]
total_pending = len(pending_list)
total_decisions = len([a for a in st.session_state.audit_log if a['Action'] in ['APPROVED', 'REJECTED']])

m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric("Pending Reviews", total_pending)
with m_col2:
    st.metric("Total Decisions", total_decisions)
with m_col3:
    st.metric("Avg. Risk Score", f"{int(sum(a['risk_score'] for a in pending_list)/total_pending if total_pending > 0 else 0)}/100")
with m_col4:
    st.metric("System Status", "Secure ✅")

st.divider()

# ==========================================
# 4. DECISION QUEUE (The "Work" Section)
# ==========================================
st.subheader("📥 Applications Awaiting Decision")

if total_pending > 0:
    # Sort by risk score descending so Manager sees high risk first
    sorted_pending = sorted(pending_list, key=lambda x: x['risk_score'], reverse=True)
    
    for approval in sorted_pending:
        # Risk indicators
        risk_color = "🔴" if approval['risk_score'] >= 70 else "🟡" if approval['risk_score'] >= 40 else "🟢"
        
        with st.expander(f"{risk_color} {approval['company_name']} | ${approval['loan_amount']}M | Risk Score: {approval['risk_score']}", expanded=True):
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.write("**Submission Info**")
                st.write(f"**Analyst:** {approval['submitted_by']}")
                st.write(f"**Date:** {approval['timestamp'][:10]}")
                st.write(f"**Application ID:** `#AURA-{approval['id']}`")
            
            with col2:
                st.write("**Risk Profile**")
                st.write(f"**Level:** {approval['risk_level']}")
                st.progress(approval['risk_score'] / 100)
                if approval.get('notes'):
                    st.info(f"**Analyst Notes:** {approval['notes']}")
            
            with col3:
                st.write("**Decision Actions**")
                # Approval Button
                if st.button(f"✅ Approve ##{approval['id']}", key=f"app_{approval['id']}", use_container_width=True, type="primary"):
                    approval["status"] = "Approved"
                    approval["approved_by"] = st.session_state.username
                    
                    # Log to Audit
                    st.session_state.audit_log.append({
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "User": st.session_state.username,
                        "Action": "APPROVED",
                        "Company": approval['company_name'],
                        "Details": f"Approved {approval['loan_amount']}M loan"
                    })
                    st.success(f"Successfully Approved {approval['company_name']}")
                    st.rerun()
                
                # Rejection Button
                if st.button(f"❌ Reject ##{approval['id']}", key=f"rej_{approval['id']}", use_container_width=True):
                    approval["status"] = "Rejected"
                    approval["rejected_by"] = st.session_state.username
                    
                    # Log to Audit
                    st.session_state.audit_log.append({
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "User": st.session_state.username,
                        "Action": "REJECTED",
                        "Company": approval['company_name'],
                        "Details": "Did not meet credit policy"
                    })
                    st.error(f"Rejected {approval['company_name']}")
                    st.rerun()
else:
    st.info("📭 The queue is empty. No applications require action at this time.")

# ==========================================
# 5. AUDIT LOG & COMPLIANCE
# ==========================================
st.divider()
st.subheader("📜 Compliance Audit Trail")
st.caption("Immutable record of all credit decisions and system actions.")

if st.session_state.audit_log:
    audit_df = pd.DataFrame(st.session_state.audit_log)
    # Display the most recent actions at the top
    st.dataframe(audit_df.iloc[::-1], use_container_width=True, hide_index=True)
else:
    st.info("No audit logs recorded for this session.")

st.divider()
st.caption("🤖 Powered by AURA Approval Engine | Enterprise Governance Mode")
