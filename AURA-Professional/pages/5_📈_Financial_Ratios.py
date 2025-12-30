import streamlit as st
from services.financial_calculator import calculate_all_ratios
import plotly.graph_objects as go

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("📈 Financial Ratios Analysis")
st.markdown("### Key Credit Metrics & Covenants")

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Financial Inputs")
    
    ebitda = st.number_input("EBITDA ($M)", min_value=0.0, value=10.0, step=0.5, help="Earnings Before Interest, Taxes, Depreciation, and Amortization")
    
    debt_service = st.number_input("Annual Debt Service ($M)", min_value=0.0, value=6.0, step=0.5, help="Principal + Interest payments per year")
    
    total_debt = st.number_input("Total Debt ($M)", min_value=0.0, value=50.0, step=1.0)
    
    ebit = st.number_input("EBIT ($M)", min_value=0.0, value=8.0, step=0.5, help="Earnings Before Interest and Taxes")
    
    interest_expense = st.number_input("Interest Expense ($M)", min_value=0.0, value=3.0, step=0.5)
    
    st.divider()
    
    if st.button("📊 Calculate Ratios", type="primary", use_container_width=True):
        financial_data = {
            "ebitda": ebitda,
            "debt_service": debt_service,
            "total_debt": total_debt,
            "ebit": ebit,
            "interest_expense": interest_expense
        }
        
        ratios = calculate_all_ratios(financial_data)
        st.session_state.financial_ratios = ratios
        st.rerun()

with col2:
    st.subheader("📈 Calculated Ratios")
    
    if st.session_state.get("financial_ratios"):
        ratios = st.session_state.financial_ratios
        
        # DSCR
        if ratios["dscr"]:
            st.metric("Debt Service Coverage Ratio (DSCR)", f"{ratios['dscr']:.2f}x")
            
            if ratios["dscr"] >= 1.25:
                st.success("✅ Strong debt service capacity")
            elif ratios["dscr"] >= 1.0:
                st.warning("⚠️ Adequate but tight coverage")
            else:
                st.error("❌ Insufficient debt coverage")
        
        st.divider()
        
        # Leverage
        if ratios["leverage_ratio"]:
            st.metric("Leverage Ratio (Debt/EBITDA)", f"{ratios['leverage_ratio']:.2f}x")
            
            if ratios["leverage_ratio"] <= 3.0:
                st.success("✅ Conservative leverage")
            elif ratios["leverage_ratio"] <= 5.0:
                st.warning("⚠️ Moderate leverage")
            else:
                st.error("❌ High leverage risk")
        
        st.divider()
        
        # Interest Coverage
        if ratios["interest_coverage"]:
            st.metric("Interest Coverage Ratio", f"{ratios['interest_coverage']:.2f}x")
            
            if ratios["interest_coverage"] >= 3.0:
                st.success("✅ Strong interest coverage")
            elif ratios["interest_coverage"] >= 1.5:
                st.warning("⚠️ Adequate coverage")
            else:
                st.error("❌ Weak interest coverage")
        
        # Gauge chart
        st.divider()
        st.markdown("**DSCR Visual Indicator**")
        
        if ratios["dscr"]:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = ratios["dscr"],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "DSCR"},
                gauge = {
                    'axis': {'range': [None, 3]},
                    'bar': {'color': "darkblue"},
                    'steps' : [
                        {'range': [0, 1], 'color': "lightcoral"},
                        {'range': [1, 1.25], 'color': "lightyellow"},
                        {'range': [1.25, 3], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 1.25
                    }
                }
            ))
            
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("👈 Enter financial data and click **Calculate Ratios**")

st.divider()
st.caption("📊 Financial Analysis Module - AURA")