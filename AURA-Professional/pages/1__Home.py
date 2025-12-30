import streamlit as st

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("🏠 Home Dashboard")
st.markdown("### System Overview")

# Role-based content
if st.session_state.role == "Admin":
    st.success("✅ You have full system access")
elif st.session_state.role == "Analyst":
    st.info("ℹ️ You can perform risk analysis and view reports")
elif st.session_state.role == "Manager":
    st.info("ℹ️ You can approve loans and view audit logs")

# Add charts, stats, etc.