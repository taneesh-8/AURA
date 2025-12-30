import streamlit as st
import json
from datetime import datetime
import pandas as pd

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("📋 Audit Log")
st.markdown("### System Activity & Compliance Tracking")

st.divider()

# Load audit log
try:
    with open("data/audit_log.json", "r") as f:
        audit_log = json.load(f)
except:
    audit_log = []

# Filters
st.subheader("🔍 Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    filter_user = st.selectbox(
        "User",
        ["All Users"] + list(set([log["user"] for log in audit_log]))
    )

with col2:
    filter_action = st.selectbox(
        "Action",
        ["All Actions"] + list(set([log["action"] for log in audit_log]))
    )

with col3:
    date_filter = st.selectbox(
        "Time Period",
        ["All Time", "Today", "Last 7 Days", "Last 30 Days"]
    )

with col4:
    sort_order = st.selectbox(
        "Sort By",
        ["Newest First", "Oldest First"]
    )

st.divider()

# Apply filters
filtered_log = audit_log.copy()

if filter_user != "All Users":
    filtered_log = [log for log in filtered_log if log["user"] == filter_user]

if filter_action != "All Actions":
    filtered_log = [log for log in filtered_log if log["action"] == filter_action]

# Date filtering
if date_filter != "All Time":
    from datetime import datetime, timedelta
    now = datetime.now()
    
    if date_filter == "Today":
        cutoff = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif date_filter == "Last 7 Days":
        cutoff = now - timedelta(days=7)
    elif date_filter == "Last 30 Days":
        cutoff = now - timedelta(days=30)
    
    filtered_log = [
        log for log in filtered_log 
        if datetime.fromisoformat(log["timestamp"]) >= cutoff
    ]

# Sort
if sort_order == "Newest First":
    filtered_log = sorted(filtered_log, key=lambda x: x["timestamp"], reverse=True)
else:
    filtered_log = sorted(filtered_log, key=lambda x: x["timestamp"])

# Display audit log
st.subheader(f"📊 Audit Entries ({len(filtered_log)} records)")

if filtered_log:
    # Create DataFrame
    audit_data = []
    
    for log in filtered_log:
        timestamp = datetime.fromisoformat(log["timestamp"])
        
        audit_data.append({
            "Timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "User": log["user"],
            "Action": log["action"],
            "Company": log.get("company", "N/A"),
            "Details": log.get("risk_score", log.get("approval_id", log.get("document_type", "N/A")))
        })
    
    df = pd.DataFrame(audit_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Detailed view
    st.subheader("🔍 Detailed Activity Log")
    
    for idx, log in enumerate(filtered_log[:20]):  # Show latest 20
        timestamp = datetime.fromisoformat(log["timestamp"])
        
        # Determine icon
        if log["action"] == "Risk Analysis":
            icon = "🔍"
        elif log["action"] == "Term Sheet Generated":
            icon = "📄"
        elif log["action"] == "Approved":
            icon = "✅"
        elif log["action"] == "Rejected":
            icon = "❌"
        elif log["action"] == "Document Upload":
            icon = "📤"
        else:
            icon = "📝"
        
        with st.expander(f"{icon} {log['action']} - {timestamp.strftime('%Y-%m-%d %H:%M')} - {log['user']}", expanded=(idx == 0)):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**User:** {log['user']}")
                st.markdown(f"**Action:** {log['action']}")
                st.markdown(f"**Timestamp:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            
            with col2:
                if log.get("company"):
                    st.markdown(f"**Company:** {log['company']}")
                
                if log.get("risk_score"):
                    st.markdown(f"**Risk Score:** {log['risk_score']}/100")
                
                if log.get("risk_level"):
                    st.markdown(f"**Risk Level:** {log['risk_level']}")
                
                if log.get("approval_id"):
                    st.markdown(f"**Approval ID:** {log['approval_id']}")
                
                if log.get("document_type"):
                    st.markdown(f"**Document Type:** {log['document_type']}")
                
                if log.get("filename"):
                    st.markdown(f"**Filename:** {log['filename']}")
    
    st.divider()
    
    # Export options
    st.subheader("📥 Export Audit Log")
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        # Export as JSON
        json_data = json.dumps(filtered_log, indent=2)
        
        st.download_button(
            label="📄 Download JSON",
            data=json_data,
            file_name=f"AURA_AuditLog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col_export2:
        # Export as CSV
        df_export = pd.DataFrame(audit_data)
        csv_data = df_export.to_csv(index=False)
        
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name=f"AURA_AuditLog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

else:
    st.info("📭 No audit records match the selected filters")

st.divider()

# Statistics
st.subheader("📈 Activity Statistics")

if audit_log:
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.metric("Total Activities", len(audit_log))
    
    with col_stat2:
        unique_users = len(set([log["user"] for log in audit_log]))
        st.metric("Active Users", unique_users)
    
    with col_stat3:
        unique_actions = len(set([log["action"] for log in audit_log]))
        st.metric("Action Types", unique_actions)
    
    with col_stat4:
        # Calculate today's activities
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_count = len([
            log for log in audit_log 
            if datetime.fromisoformat(log["timestamp"]) >= today
        ])
        st.metric("Today's Activities", today_count)
    
    st.divider()
    
    # Activity breakdown
    st.markdown("**Activity Breakdown:**")
    
    action_counts = pd.Series([log["action"] for log in audit_log]).value_counts()
    
    chart_data = pd.DataFrame({
        "Action": action_counts.index,
        "Count": action_counts.values
    })
    
    st.bar_chart(chart_data.set_index("Action"))

st.divider()
st.caption("📋 Audit & Compliance Tracking - AURA") 