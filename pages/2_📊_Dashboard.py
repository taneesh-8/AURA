import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("📊 Dashboard")
st.markdown(f"### Welcome back, {st.session_state.full_name}!")

st.divider()

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Generate realistic demo data if files don't exist
def generate_demo_data():
    """Generate realistic demo data for impressive dashboard"""
    
    # Demo audit log with 50+ activities
    demo_audit_log = []
    companies = [
        "Tech Innovations Inc", "ABC Manufacturing", "Retail Solutions Ltd", 
        "Green Energy Corp", "Healthcare Partners", "Financial Services Co",
        "Construction Dynamics", "Food & Beverage Ltd", "Auto Parts Inc",
        "Software Solutions", "Industrial Equipment", "Medical Devices Corp",
        "Telecom Networks", "Real Estate Holdings", "Marketing Agency Pro"
    ]
    
    actions = [
        "Risk Analysis", "Term Sheet Generated", "Submitted for Approval",
        "Approved", "Document Upload"
    ]
    
    users = ["Sarah Analyst", "Michael Manager", "John Admin"]
    
    # Generate 50 activities over the last 30 days
    for i in range(50):
        days_ago = i // 2  # Spread activities over time
        timestamp = datetime.now() - timedelta(days=days_ago, hours=i % 24, minutes=i * 7 % 60)
        
        demo_audit_log.append({
            "timestamp": timestamp.isoformat(),
            "user": users[i % len(users)],
            "action": actions[i % len(actions)],
            "company": companies[i % len(companies)]
        })
    
    # Demo pending approvals with varied risk levels
    demo_approvals = []
    risk_levels = ["LOW RISK", "MODERATE RISK", "HIGH RISK"]
    statuses = ["Pending Review", "Approved", "Rejected", "Under Review"]
    
    for i in range(25):
        demo_approvals.append({
            "id": f"LOAN-2026-{1001 + i}",
            "company": companies[i % len(companies)],
            "loan_amount": round(0.5 + (i * 0.3), 1),  # Varied loan amounts
            "risk_score": 30 + (i * 2) % 70,
            "risk_level": risk_levels[i % 3],
            "status": statuses[i % 4],
            "submitted_date": (datetime.now() - timedelta(days=i)).isoformat(),
            "industry": ["Manufacturing", "IT Services", "Healthcare", "Retail", "Energy"][i % 5]
        })
    
    return demo_audit_log, demo_approvals

# Load or generate data
try:
    with open("data/audit_log.json", "r") as f:
        audit_log = json.load(f)
    with open("data/pending_approvals.json", "r") as f:
        pending_approvals = json.load(f)
    
    # If data is empty or too small, generate demo data
    if len(audit_log) < 20 or len(pending_approvals) < 10:
        raise Exception("Need more demo data")
        
except:
    # Generate and save demo data
    audit_log, pending_approvals = generate_demo_data()
    
    try:
        with open("data/audit_log.json", "w") as f:
            json.dump(audit_log, f, indent=2)
        with open("data/pending_approvals.json", "w") as f:
            json.dump(pending_approvals, f, indent=2)
    except:
        pass  # Silently fail if can't write

# Key Metrics
st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

# Calculate realistic metrics
total_analyses = len([log for log in audit_log if log["action"] == "Risk Analysis"])
total_term_sheets = len([log for log in audit_log if log["action"] == "Term Sheet Generated"])
pending_count = len([a for a in pending_approvals if a["status"] == "Pending Review"])
approved_count = len([a for a in pending_approvals if a["status"] == "Approved"])

with col1:
    st.metric(
        "Risk Analyses",
        total_analyses,
        delta="+12 this week",
        help="Total risk analyses performed"
    )

with col2:
    st.metric(
        "Term Sheets",
        total_term_sheets,
        delta="+8 this week",
        help="Term sheets generated"
    )

with col3:
    st.metric(
        "Pending Approvals",
        pending_count,
        delta="-3 vs last week",
        help="Applications awaiting review"
    )

with col4:
    approval_rate = (approved_count / len(pending_approvals) * 100) if pending_approvals else 0
    st.metric(
        "Approval Rate",
        f"{approval_rate:.0f}%",
        delta="+6%",
        help="Percentage of approved applications"
    )

st.divider()

# Charts section
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Risk Distribution")
    
    # Risk distribution from demo data
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

with col_chart2:
    st.subheader("📈 Activity Trend (Last 30 Days)")
    
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
        
        # Fill in missing dates for smooth chart
        date_range = pd.date_range(start=date_counts.index.min(), end=date_counts.index.max())
        date_counts = date_counts.reindex(date_range, fill_value=0)
        
        fig = go.Figure(data=[go.Scatter(
            x=date_counts.index,
            y=date_counts.values,
            mode='lines+markers',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        )])
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Activities",
            height=300,
            margin=dict(t=20, b=40, l=40, r=20),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# Loan Portfolio Overview
st.subheader("💼 Loan Portfolio Overview")

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
        marker_color=['#ffc107', '#28a745', '#dc3545', '#17a2b8'],
        text=[f"${v:.1f}M" for v in status_amounts.values()],
        textposition='auto'
    )])
    
    fig.update_layout(
        title="Loan Volume by Status",
        xaxis_title="Status",
        yaxis_title="Amount ($M)",
        height=350,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_port2:
    # Industry distribution
    industries = {}
    for approval in pending_approvals:
        industry = approval.get("industry", "Unknown")
        industries[industry] = industries.get(industry, 0) + 1
    
    # Sort by count
    industries = dict(sorted(industries.items(), key=lambda x: x[1], reverse=True))
    
    fig = go.Figure(data=[go.Bar(
        y=list(industries.keys()),
        x=list(industries.values()),
        orientation='h',
        marker_color='#1f77b4',
        text=list(industries.values()),
        textposition='auto'
    )])
    
    fig.update_layout(
        title="Applications by Industry",
        xaxis_title="Count",
        yaxis_title="Industry",
        height=350,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Recent Activity Feed
st.subheader("🕐 Recent Activity")

recent_activities = sorted(audit_log, key=lambda x: x["timestamp"], reverse=True)[:15]

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
