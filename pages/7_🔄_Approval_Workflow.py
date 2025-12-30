import streamlit as st
import json
from datetime import datetime
import pandas as pd

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("🔄 Approval Workflow")
st.markdown("### Credit Decision Review & Approval Process")

st.divider()

# Initialize pending approvals
try:
    with open("data/pending_approvals.json", "r") as f:
        pending_approvals = json.load(f)
except:
    pending_approvals = [
        {
            "id": "AURA-2024-001",
            "company": "ABC Manufacturing Corp",
            "loan_amount": 5.0,
            "risk_level": "MODERATE RISK",
            "risk_score": 42,
            "submitted_by": "analyst",
            "submitted_date": "2024-12-28T10:30:00",
            "status": "Pending Review"
        },
        {
            "id": "AURA-2024-002",
            "company": "XYZ Tech Solutions",
            "loan_amount": 10.0,
            "risk_level": "LOW RISK",
            "risk_score": 28,
            "submitted_by": "analyst",
            "submitted_date": "2024-12-28T14:15:00",
            "status": "Pending Review"
        },
        {
            "id": "AURA-2024-003",
            "company": "Retail Innovations Ltd",
            "loan_amount": 15.0,
            "risk_level": "HIGH RISK",
            "risk_score": 68,
            "submitted_by": "analyst",
            "submitted_date": "2024-12-27T16:45:00",
            "status": "Pending Review"
        }
    ]
    
    with open("data/pending_approvals.json", "w") as f:
        json.dump(pending_approvals, f, indent=2)

# Role-based view
if st.session_state.role == "Analyst":
    st.info("ℹ️ Analysts can submit loan applications for review")
    
    st.subheader("📤 Submit New Application")
    
    # Check if analysis exists
    if st.session_state.get("risk_analysis") and st.session_state.get("company_data"):
        company_data = st.session_state.company_data
        risk_analysis = st.session_state.risk_analysis
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Company:** {company_data.get('company_name')}")
            st.markdown(f"**Loan Amount:** ${company_data.get('loan_amount')}M")
            st.markdown(f"**Risk Level:** {risk_analysis['risk_level']}")
        
        with col2:
            st.markdown(f"**Industry:** {company_data.get('industry')}")
            st.markdown(f"**Purpose:** {company_data.get('purpose')}")
            st.markdown(f"**Risk Score:** {risk_analysis['risk_score']}/100")
        
        st.divider()
        
        submission_notes = st.text_area(
            "Submission Notes",
            placeholder="Add notes for the reviewer..."
        )
        
        if st.button("📤 Submit for Approval", type="primary", use_container_width=True):
            # Create new approval entry
            new_approval = {
                "id": f"AURA-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "company": company_data.get('company_name'),
                "loan_amount": company_data.get('loan_amount'),
                "risk_level": risk_analysis['risk_level'],
                "risk_score": risk_analysis['risk_score'],
                "submitted_by": st.session_state.username,
                "submitted_date": datetime.now().isoformat(),
                "status": "Pending Review",
                "notes": submission_notes
            }
            
            pending_approvals.insert(0, new_approval)
            
            with open("data/pending_approvals.json", "w") as f:
                json.dump(pending_approvals, f, indent=2)
            
            # Log to audit
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "user": st.session_state.username,
                "action": "Submitted for Approval",
                "company": company_data.get('company_name'),
                "approval_id": new_approval['id']
            }
            
            try:
                with open("data/audit_log.json", "r") as f:
                    audit_log = json.load(f)
            except:
                audit_log = []
            
            audit_log.append(audit_entry)
            
            with open("data/audit_log.json", "w") as f:
                json.dump(audit_log, f, indent=2)
            
            st.success(f"✅ Application {new_approval['id']} submitted for approval!")
            st.balloons()
            st.rerun()
    else:
        st.warning("⚠️ Complete risk analysis first before submitting for approval")
        if st.button("🔍 Go to Risk Analysis"):
            st.switch_page("pages/3_🔍_Risk_Analysis.py")

elif st.session_state.role in ["Admin", "Manager"]:
    st.success("✅ You have approval authority")
    
    # Pending approvals section
    st.subheader("📋 Pending Approvals")
    
    pending = [a for a in pending_approvals if a["status"] == "Pending Review"]
    
    if pending:
        for approval in pending:
            risk_color = "🔴" if approval["risk_level"] == "HIGH RISK" else "🟡" if approval["risk_level"] == "MODERATE RISK" else "🟢"
            
            with st.expander(f"{risk_color} {approval['company']} - ${approval['loan_amount']}M ({approval['id']})", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Company:** {approval['company']}")
                    st.markdown(f"**Loan Amount:** ${approval['loan_amount']}M")
                    st.markdown(f"**Submitted By:** {approval['submitted_by']}")
                
                with col2:
                    st.markdown(f"**Risk Level:** {approval['risk_level']}")
                    st.markdown(f"**Risk Score:** {approval['risk_score']}/100")
                    st.markdown(f"**Date:** {approval['submitted_date'][:10]}")
                
                with col3:
                    st.markdown(f"**Status:** {approval['status']}")
                    if approval.get('notes'):
                        st.markdown(f"**Notes:** {approval['notes']}")
                
                st.divider()
                
                # Reviewer comments
                reviewer_comments = st.text_area(
                    "Reviewer Comments",
                    key=f"comments_{approval['id']}",
                    placeholder="Add your review comments..."
                )
                
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    if st.button("✅ Approve", key=f"approve_{approval['id']}", use_container_width=True):
                        approval["status"] = "Approved"
                        approval["reviewed_by"] = st.session_state.username
                        approval["reviewed_date"] = datetime.now().isoformat()
                        approval["reviewer_comments"] = reviewer_comments
                        
                        with open("data/pending_approvals.json", "w") as f:
                            json.dump(pending_approvals, f, indent=2)
                        
                        # Log to audit
                        audit_entry = {
                            "timestamp": datetime.now().isoformat(),
                            "user": st.session_state.username,
                            "action": "Approved",
                            "company": approval['company'],
                            "approval_id": approval['id']
                        }
                        
                        try:
                            with open("data/audit_log.json", "r") as f:
                                audit_log = json.load(f)
                        except:
                            audit_log = []
                        
                        audit_log.append(audit_entry)
                        
                        with open("data/audit_log.json", "w") as f:
                            json.dump(audit_log, f, indent=2)
                        
                        st.success(f"✅ Approved: {approval['company']}")
                        st.rerun()
                
                with col_btn2:
                    if st.button("❌ Reject", key=f"reject_{approval['id']}", use_container_width=True):
                        approval["status"] = "Rejected"
                        approval["reviewed_by"] = st.session_state.username
                        approval["reviewed_date"] = datetime.now().isoformat()
                        approval["reviewer_comments"] = reviewer_comments
                        
                        with open("data/pending_approvals.json", "w") as f:
                            json.dump(pending_approvals, f, indent=2)
                        
                        # Log to audit
                        audit_entry = {
                            "timestamp": datetime.now().isoformat(),
                            "user": st.session_state.username,
                            "action": "Rejected",
                            "company": approval['company'],
                            "approval_id": approval['id']
                        }
                        
                        try:
                            with open("data/audit_log.json", "r") as f:
                                audit_log = json.load(f)
                        except:
                            audit_log = []
                        
                        audit_log.append(audit_entry)
                        
                        with open("data/audit_log.json", "w") as f:
                            json.dump(audit_log, f, indent=2)
                        
                        st.error(f"❌ Rejected: {approval['company']}")
                        st.rerun()
                
                with col_btn3:
                    if st.button("🔄 Request Info", key=f"request_{approval['id']}", use_container_width=True):
                        approval["status"] = "Information Requested"
                        approval["reviewed_by"] = st.session_state.username
                        approval["reviewed_date"] = datetime.now().isoformat()
                        approval["reviewer_comments"] = reviewer_comments
                        
                        with open("data/pending_approvals.json", "w") as f:
                            json.dump(pending_approvals, f, indent=2)
                        
                        st.info(f"ℹ️ Information requested: {approval['company']}")
                        st.rerun()
    else:
        st.info("📭 No pending approvals")
    
    st.divider()
    
    # Approved/Rejected history
    st.subheader("📊 Approval History")
    
    completed = [a for a in pending_approvals if a["status"] in ["Approved", "Rejected", "Information Requested"]]
    
    if completed:
        history_data = []
        for approval in completed:
            history_data.append({
                "ID": approval["id"],
                "Company": approval["company"],
                "Amount ($M)": approval["loan_amount"],
                "Risk Level": approval["risk_level"],
                "Status": approval["status"],
                "Reviewed By": approval.get("reviewed_by", "N/A"),
                "Date": approval.get("reviewed_date", "N/A")[:10]
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No completed approvals yet")

st.divider()

# Statistics
st.subheader("📈 Workflow Statistics")

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

total_approvals = len(pending_approvals)
pending_count = len([a for a in pending_approvals if a["status"] == "Pending Review"])
approved_count = len([a for a in pending_approvals if a["status"] == "Approved"])
rejected_count = len([a for a in pending_approvals if a["status"] == "Rejected"])

with col_stat1:
    st.metric("Total Applications", total_approvals)

with col_stat2:
    st.metric("Pending Review", pending_count)

with col_stat3:
    st.metric("Approved", approved_count, delta=f"{(approved_count/total_approvals*100) if total_approvals > 0 else 0:.0f}%")

with col_stat4:
    st.metric("Rejected", rejected_count)

st.divider()
st.caption("🔄 Approval Workflow Management - AURA")