import streamlit as st
from PIL import Image
import pandas as pd
import json
from datetime import datetime

if not st.session_state.get("logged_in"):
    st.warning("Please login first")
    st.stop()

st.title("📤 Document Upload")
st.markdown("### Upload Financial Statements & Supporting Documents")

st.divider()

# Initialize upload history
if "upload_history" not in st.session_state:
    st.session_state.upload_history = []

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 Upload Documents")
    
    company_name_upload = st.text_input("Company Name", key="upload_company")
    
    document_type = st.selectbox(
        "Document Type",
        [
            "Financial Statements",
            "Balance Sheet",
            "Income Statement",
            "Cash Flow Statement",
            "Tax Returns",
            "Bank Statements",
            "Business Plan",
            "Legal Documents",
            "Other"
        ]
    )
    
    uploaded_file = st.file_uploader(
        "Choose file",
        type=["pdf", "xlsx", "xls", "csv", "jpg", "png", "docx"],
        help="Supported formats: PDF, Excel, CSV, Images, Word"
    )
    
    notes = st.text_area("Notes (Optional)", placeholder="Add any relevant notes about this document")
    
    st.divider()
    
    if st.button("📤 Upload Document", type="primary", use_container_width=True):
        if uploaded_file and company_name_upload:
            # Simulate document processing
            file_details = {
                "timestamp": datetime.now().isoformat(),
                "uploaded_by": st.session_state.username,
                "company": company_name_upload,
                "document_type": document_type,
                "filename": uploaded_file.name,
                "file_size": uploaded_file.size,
                "notes": notes
            }
            
            st.session_state.upload_history.insert(0, file_details)
            
            # Log to audit
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "user": st.session_state.username,
                "action": "Document Upload",
                "company": company_name_upload,
                "document_type": document_type,
                "filename": uploaded_file.name
            }
            
            try:
                with open("data/audit_log.json", "r") as f:
                    audit_log = json.load(f)
            except:
                audit_log = []
            
            audit_log.append(audit_entry)
            
            with open("data/audit_log.json", "w") as f:
                json.dump(audit_log, f, indent=2)
            
            st.success(f"✅ Document uploaded successfully: {uploaded_file.name}")
            st.rerun()
        else:
            st.error("❌ Please provide company name and select a file")

with col2:
    st.subheader("📋 Upload History")
    
    if st.session_state.upload_history:
        for idx, upload in enumerate(st.session_state.upload_history[:10]):
            with st.expander(f"📄 {upload['filename']} - {upload['company']}", expanded=(idx == 0)):
                st.markdown(f"**Document Type:** {upload['document_type']}")
                st.markdown(f"**Uploaded By:** {upload['uploaded_by']}")
                st.markdown(f"**Company:** {upload['company']}")
                st.markdown(f"**Size:** {upload['file_size']:,} bytes")
                st.markdown(f"**Date:** {upload['timestamp'][:19]}")
                
                if upload['notes']:
                    st.markdown(f"**Notes:** {upload['notes']}")
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("🔍 Analyze", key=f"analyze_{idx}"):
                        st.info("Document analysis feature coming soon")
                
                with col_btn2:
                    if st.button("🗑️ Delete", key=f"delete_{idx}"):
                        st.session_state.upload_history.pop(idx)
                        st.rerun()
    else:
        st.info("No documents uploaded yet")

st.divider()

# Document statistics
st.subheader("📊 Upload Statistics")

if st.session_state.upload_history:
    doc_types = [u["document_type"] for u in st.session_state.upload_history]
    doc_type_counts = pd.Series(doc_types).value_counts()
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.metric("Total Uploads", len(st.session_state.upload_history))
    
    with col_stat2:
        st.metric("Document Types", len(doc_type_counts))
    
    with col_stat3:
        total_size = sum([u["file_size"] for u in st.session_state.upload_history])
        st.metric("Total Size", f"{total_size / 1024 / 1024:.2f} MB")
    
    st.divider()
    
    # Document type breakdown
    st.markdown("**Documents by Type:**")
    
    chart_data = pd.DataFrame({
        "Document Type": doc_type_counts.index,
        "Count": doc_type_counts.values
    })
    
    st.bar_chart(chart_data.set_index("Document Type"))

else:
    st.info("Upload documents to see statistics")

st.divider()
st.caption("📤 Document Management System - AURA")