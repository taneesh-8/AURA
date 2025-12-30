from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime
import io

def generate_term_sheet_pdf(company_name, industry, loan_amount, purpose, risk_analysis, loan_terms):
    """Generate professional bank-style PDF term sheet"""
    
    buffer = io.BytesIO()
    
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=18,
        textColor=colors.HexColor("#1f4788"),
        spaceAfter=20
    )
    
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=12,
        textColor=colors.grey,
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#1f4788"),
        spaceAfter=10,
        spaceBefore=15
    )
    
    # Header
    story.append(Paragraph("🏦 AURA", title_style))
    story.append(Paragraph("AI Unified Risk & Loan Origination Assistant", subtitle_style))
    story.append(Paragraph("<b>CONFIDENTIAL TERM SHEET</b>", title_style))
    story.append(Spacer(1, 20))
    
    # Metadata
    meta_data = [
        ["Generated:", datetime.now().strftime('%B %d, %Y at %H:%M')],
        ["Document ID:", f"AURA-{datetime.now().strftime('%Y%m%d%H%M%S')}"],
        ["Status:", "DRAFT - FOR DISCUSSION PURPOSES ONLY"]
    ]
    
    meta_table = Table(meta_data, colWidths=[120, 350])
    meta_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    story.append(meta_table)
    story.append(Spacer(1, 25))
    
    # Borrower Information
    story.append(Paragraph("BORROWER INFORMATION", heading_style))
    
    borrower_data = [
        ["Company Name:", company_name],
        ["Industry:", industry],
        ["Loan Amount:", f"${loan_amount} Million"],
        ["Purpose:", purpose]
    ]
    
    borrower_table = Table(borrower_data, colWidths=[150, 320])
    borrower_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor("#1f4788")),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.lightgrey),
    ]))
    
    story.append(borrower_table)
    story.append(Spacer(1, 20))
    
    # Risk Assessment
    story.append(Paragraph("RISK ASSESSMENT", heading_style))
    
    risk_color = colors.red if risk_analysis["risk_level"] == "HIGH RISK" else colors.orange if risk_analysis["risk_level"] == "MODERATE RISK" else colors.green
    
    risk_data = [
        ["Risk Level:", risk_analysis["risk_level"]],
        ["Risk Score:", f"{risk_analysis['risk_score']}/100"],
        ["Recommendation:", risk_analysis["recommendation"]]
    ]
    
    risk_table = Table(risk_data, colWidths=[150, 320])
    risk_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor("#1f4788")),
        ('TEXTCOLOR', (1, 0), (1, 0), risk_color),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.lightgrey),
    ]))
    
    story.append(risk_table)
    story.append(Spacer(1, 20))
    
    # Proposed Loan Terms
    story.append(Paragraph("PROPOSED LOAN TERMS", heading_style))
    
    terms_data = [
        ["Tenor:", loan_terms["tenor"]],
        ["Interest Rate:", loan_terms["interest_margin"]],
        ["Amortization:", loan_terms["amortization"]],
        ["Collateral:", loan_terms["collateral"]]
    ]
    
    terms_table = Table(terms_data, colWidths=[150, 320])
    terms_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor("#1f4788")),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.lightgrey),
    ]))
    
    story.append(terms_table)
    story.append(Spacer(1, 20))
    
    # Financial Covenants
    story.append(Paragraph("FINANCIAL COVENANTS", heading_style))
    
    for covenant in loan_terms["covenants"]:
        story.append(Paragraph(f"• {covenant}", styles["Normal"]))
    
    story.append(Spacer(1, 30))
    
    # Disclaimer
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_LEFT
    )
    
    disclaimer_text = """
<b>IMPORTANT DISCLAIMER:</b><br/>
This term sheet is indicative only and does not constitute a commitment to lend. Final terms are subject to 
satisfactory completion of due diligence, credit approval, documentation, and fulfillment of conditions precedent. 
This document is confidential and intended solely for the use of the addressee. AURA AI system recommendations 
are for guidance purposes and all credit decisions require human oversight and approval.
"""
    
    story.append(Paragraph(disclaimer_text, disclaimer_style))
    
    # Footer
    story.append(Spacer(1, 20))
    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    story.append(Paragraph("Generated by AURA - AI Unified Risk & Loan Origination Assistant", footer_style))
    story.append(Paragraph(f"Document generated on {datetime.now().strftime('%B %d, %Y')}", footer_style))
    
    # Build PDF
    pdf.build(story)
    buffer.seek(0)
    
    return buffer