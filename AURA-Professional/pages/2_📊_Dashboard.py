import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("📊 Dashboard")
st.markdown(f"### Welcome back, {st.session_state.full_name}!")

st.divider()

# Load data
try:
    with open("data/audit_log.json", "r") as f:
        audit_log = json.load(f)
except:
    audit_log = []

try:
    with open("data/pending_approvals.json", "r") as f:
        pending_approvals = json.load(f)
except:
    pending_approvals = []

# Key Metrics
st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

# Calculate metrics
total_analyses = len([log for log in audit_log if log["action"] == "Risk Analysis"])
total_term_sheets = len([log for log in audit_log if log["action"] == "Term Sheet Generated"])
pending_count = len([a for a in pending_approvals if a["status"] == "Pending Review"])
approved_count = len([a for a in pending_approvals if a["status"] == "Approved"])

with col1:
    st.metric(
        "Risk Analyses",
        total_analyses,
        delta="+5 this week",
        help="Total risk analyses performed"
    )

with col2:
    st.metric(
        "Term Sheets",
        total_term_sheets,
        delta="+3 this week",
        help="Term sheets generated"
    )

with col3:
    st.metric(
        "Pending Approvals",
        pending_count,
        delta="-2 vs last week",
        help="Applications awaiting review"
    )

with col4:
    approval_rate = (approved_count / len(pending_approvals) * 100) if pending_approvals else 0
    st.metric(
        "Approval Rate",
        f"{approval_rate:.0f}%",
        delta="+4%",
        help="Percentage of approved applications"
    )

st.divider()

# Charts section
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Risk Distribution")
    
    # Sample risk distribution data
    if pending_approvals:
        risk_levels = [a["risk_level"] for a in pending_approvals]
        risk_counts = pd.Series(risk_levels).value_counts()
        
        colors = {
            "LOW RISK": "#28a745",
            "MODERATE RISK": "#ffc107",
            "HIGH RISK": "#dc3545"
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=risk_counts.index,
            values=risk_counts.values,
            marker=dict(colors=[colors.get(level, "#999") for level in risk_counts.index]),
            hole=0.4
        )])
        
        fig.update_layout(
            showlegend=True,
            height=300,
            margin=dict(t=0, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No risk data available yet")

with col_chart2:
    st.subheader("📈 Activity Trend")
    
    if audit_log:
        # Create daily activity trend
        dates = []
        for log in audit_log:
            try:
                date = datetime.fromisoformat(log["timestamp"]).date()
                dates.append(date)
            except:
                pass
        
        if dates:
            date_counts = pd.Series(dates).value_counts().sort_index()
            
            fig = go.Figure(data=[go.Scatter(
                x=date_counts.index,
                y=date_counts.values,
                mode='lines+markers',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=8)
            )])
            
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Activities",
                height=300,
                margin=dict(t=20, b=40, l=40, r=20),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No activity data available")
    else:
        st.info("No activity data available yet")

st.divider()

# Loan Portfolio Overview
st.subheader("💼 Loan Portfolio Overview")

if pending_approvals:
    col_port1, col_port2 = st.columns(2)
    
    with col_port1:
        # Total loan volume by status
        status_amounts = {}
        for approval in pending_approvals:
            status = approval["status"]
            amount = approval["loan_amount"]
            status_amounts[status] = status_amounts.get(status, 0) + amount
        
        fig = go.Figure(data=[go.Bar(
            x=list(status_amounts.keys()),
            y=list(status_amounts.values()),
            marker_color=['#ffc107', '#28a745', '#dc3545', '#17a2b8']
        )])
        
        fig.update_layout(
            title="Loan Volume by Status ($M)",
            xaxis_title="Status",
            yaxis_title="Amount ($M)",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_port2:
        # Industry distribution
        industries = [a.get("company", "Unknown") for a in pending_approvals]
        
        # For demo, create sample industry data
        industry_data = {
            "Manufacturing": 3,
            "IT Services": 2,
            "Healthcare": 1,
            "Retail": 2,
            "Energy": 1
        }
        
        fig = go.Figure(data=[go.Bar(
            y=list(industry_data.keys()),
            x=list(industry_data.values()),
            orientation='h',
            marker_color='#1f77b4'
        )])
        
        fig.update_layout(
            title="Applications by Industry",
            xaxis_title="Count",
            yaxis_title="Industry",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# Recent Activity Feed
st.subheader("🕐 Recent Activity")

if audit_log:
    recent_activities = sorted(audit_log, key=lambda x: x["timestamp"], reverse=True)[:10]
    
    for activity in recent_activities:
        timestamp = datetime.fromisoformat(activity["timestamp"])
        time_ago = datetime.now() - timestamp
        
        if time_ago.days > 0:
            time_str = f"{time_ago.days} day{'s' if time_ago.days > 1 else ''} ago"
        elif time_ago.seconds > 3600:
            hours = time_ago.seconds // 3600
            time_str = f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            minutes = time_ago.seconds // 60
            time_str = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        
        # Determine icon and color
        action_styles = {
            "Risk Analysis": ("🔍", "#17a2b8"),
            "Term Sheet Generated": ("📄", "#28a745"),
            "Approved": ("✅", "#28a745"),
            "Rejected": ("❌", "#dc3545"),
            "Document Upload": ("📤", "#6c757d"),
            "Submitted for Approval": ("🔄", "#ffc107")
        }
        
        icon, color = action_styles.get(activity["action"], ("📝", "#6c757d"))
        
        with st.container():
            col_act1, col_act2, col_act3 = st.columns([1, 4, 2])
            
            with col_act1:
                st.markdown(f"<h2 style='margin:0'>{icon}</h2>", unsafe_allow_html=True)
            
            with col_act2:
                st.markdown(f"**{activity['action']}**")
                st.caption(f"{activity['user']} • {activity.get('company', 'N/A')}")
            
            with col_act3:
                st.caption(time_str)
            
            st.divider()
else:
    st.info("No recent activities")

# Quick Actions
st.subheader("⚡ Quick Actions")

col_qa1, col_qa2, col_qa3 = st.columns(3)

with col_qa1:
    if st.button("🔍 New Risk Analysis", use_container_width=True, type="primary"):
        st.switch_page("pages/3_🔍_Risk_Analysis.py")

with col_qa2:
    if st.button("📄 Generate Term Sheet", use_container_width=True):
        st.switch_page("pages/4_📄_Term_Sheet.py")

with col_qa3:
    if st.button("🔄 View Approvals", use_container_width=True):
        st.switch_page("pages/7_🔄_Approval_Workflow.py")

st.divider()
st.caption("📊 Real-time Dashboard - AURA Professional")