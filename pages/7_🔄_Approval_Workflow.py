import streamlit as st
from datetime import datetime

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("🔄 Approval Workflow")
st.markdown("### Credit Decision Review & Approval Process")

# Initialize session state for approvals
if "pending_approvals" not in st.session_state:
    st.session_state.pending_approvals = []

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

st.divider()

# Check if there's a risk analysis to submit for approval
if st.session_state.get("risk_analysis") and st.session_state.get("company_data"):
    with st.expander("📤 Submit Current Analysis for Approval", expanded=False):
        company = st.session_state.company_data
        risk = st.session_state.risk_analysis
        
        st.write(f"**Company:** {company['company_name']}")
        st.write(f"**Risk Score:** {risk['risk_score']}/100")
        st.write(f"**Risk Level:** {risk['risk_level']}")
        st.write(f"**Loan Amount:** ${company['loan_amount']}M")
        
        notes = st.text_area("Additional Notes", placeholder="Add any comments or special considerations...")
        
        if st.button("📨 Submit for Approval", type="primary"):
            approval_request = {
                "id": len(st.session_state.pending_approvals) + 1,
                "timestamp": datetime.now().isoformat(),
                "submitted_by": st.session_state.username,
                "company_name": company['company_name'],
                "loan_amount": company['loan_amount'],
                "risk_score": risk['risk_score'],
                "risk_level": risk['risk_level'],
                "status": "Pending",
                "notes": notes,
                "company_data": company,
                "risk_analysis": risk
            }
            
            st.session_state.pending_approvals.append(approval_request)
            
            # Log action
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "user": st.session_state.username,
                "action": "Submitted for Approval",
                "company": company['company_name']
            }
            st.session_state.audit_log.append(audit_entry)
            
            st.success("✅ Submitted for approval!")
            st.rerun()

st.divider()

# Display pending approvals
st.subheader("📋 Pending Approvals")

if st.session_state.pending_approvals:
    for approval in st.session_state.pending_approvals:
        if approval["status"] == "Pending":
            with st.expander(f"🔍 {approval['company_name']} - ${approval['loan_amount']}M", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Risk Score", f"{approval['risk_score']}/100")
                    st.write(f"**Risk Level:** {approval['risk_level']}")
                    st.write(f"**Submitted by:** {approval['submitted_by']}")
                    st.write(f"**Date:** {approval['timestamp'][:10]}")
                
                with col2:
                    st.write(f"**Loan Amount:** ${approval['loan_amount']}M")
                    if approval.get('notes'):
                        st.info(f"**Notes:** {approval['notes']}")
                
                st.divider()
                
                # Get user role safely - check both user_role and role (case-insensitive)
                user_role = st.session_state.get("user_role") or st.session_state.get("role") or "analyst"
                user_role_lower = str(user_role).lower()
                
                # Debug info (remove after testing)
                st.caption(f"🔍 Debug: Current role = '{user_role}' (lowercase: '{user_role_lower}')")
                
                # Approval actions (only for managers/admins)
                if user_role_lower in ["manager", "admin"]:
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        if st.button(f"✅ Approve", key=f"approve_{approval['id']}", use_container_width=True, type="primary"):
                            approval["status"] = "Approved"
                            approval["approved_by"] = st.session_state.username
                            approval["approval_date"] = datetime.now().isoformat()
                            
                            # Log action
                            audit_entry = {
                                "timestamp": datetime.now().isoformat(),
                                "user": st.session_state.username,
                                "action": "Approved",
                                "company": approval['company_name']
                            }
                            st.session_state.audit_log.append(audit_entry)
                            
                            st.success(f"✅ Approved {approval['company_name']}")
                            st.rerun()
                    
                    with col_btn2:
                        if st.button(f"❌ Reject", key=f"reject_{approval['id']}", use_container_width=True):
                            approval["status"] = "Rejected"
                            approval["rejected_by"] = st.session_state.username
                            approval["rejection_date"] = datetime.now().isoformat()
                            
                            # Log action
                            audit_entry = {
                                "timestamp": datetime.now().isoformat(),
                                "user": st.session_state.username,
                                "action": "Rejected",
                                "company": approval['company_name']
                            }
                            st.session_state.audit_log.append(audit_entry)
                            
                            st.error(f"❌ Rejected {approval['company_name']}")
                            st.rerun()
                else:
                    st.info(f"🔒 Only managers and admins can approve/reject applications (Your role: {user_role})")
else:
    st.info("📭 No pending approvals")

st.divider()

# Display recent decisions
st.subheader("📊 Recent Decisions")

completed = [a for a in st.session_state.pending_approvals if a["status"] in ["Approved", "Rejected"]]

if completed:
    for approval in completed[-5:]:  # Show last 5
        status_icon = "✅" if approval["status"] == "Approved" else "❌"
        with st.expander(f"{status_icon} {approval['company_name']} - {approval['status']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Company:** {approval['company_name']}")
                st.write(f"**Loan Amount:** ${approval['loan_amount']}M")
                st.write(f"**Risk Score:** {approval['risk_score']}/100")
            
            with col2:
                st.write(f"**Status:** {approval['status']}")
                st.write(f"**Submitted by:** {approval['submitted_by']}")
                decision_key = "approved_by" if approval["status"] == "Approved" else "rejected_by"
                if decision_key in approval:
                    st.write(f"**Decided by:** {approval[decision_key]}")
else:
    st.info("📭 No completed decisions yet")

st.divider()

# Statistics
st.subheader("📈 Approval Statistics")

if st.session_state.pending_approvals:
    total = len(st.session_state.pending_approvals)
    pending = len([a for a in st.session_state.pending_approvals if a["status"] == "Pending"])
    approved = len([a for a in st.session_state.pending_approvals if a["status"] == "Approved"])
    rejected = len([a for a in st.session_state.pending_approvals if a["status"] == "Rejected"])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total", total)
    with col2:
        st.metric("Pending", pending)
    with col3:
        st.metric("Approved", approved)
    with col4:
        st.metric("Rejected", rejected)
    
    if total > 0:
        approval_rate = (approved / total) * 100
        st.progress(approval_rate / 100)
        st.caption(f"Approval Rate: {approval_rate:.1f}%")
else:
    st.info("📊 No data available yet")

st.divider()
st.caption("🤖 Powered by AURA Approval Engine")
