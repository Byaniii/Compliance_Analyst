#!/usr/bin/env python3
"""
Generate mock compliance documents for testing
Creates PDFs for Low, Medium, and High risk scenarios
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from pathlib import Path

# Create output directories
base_dir = Path(__file__).parent / "mock_users"
base_dir.mkdir(exist_ok=True)

for risk_level in ['low_risk', 'medium_risk', 'high_risk']:
    (base_dir / risk_level).mkdir(exist_ok=True)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#1a73e8'), spaceAfter=12, alignment=1)
heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#333333'), spaceAfter=8)
normal_style = styles['Normal']

def create_low_risk_docs():
    """Generate Low Risk scenario documents"""
    print("Generating Low Risk documents...")
    
    # 1. Source of Funds
    doc = SimpleDocTemplate(str(base_dir / "low_risk" / "low_sof.pdf"), pagesize=letter)
    story = []
    
    story.append(Paragraph("DBS BANK SINGAPORE", title_style))
    story.append(Paragraph("PERSONAL ACCOUNT STATEMENT", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Account Holder:</b> Maria Santos", normal_style))
    story.append(Paragraph("<b>Account Number:</b> 123-456-789-0", normal_style))
    story.append(Paragraph("<b>Statement Period:</b> September 1 - November 30, 2024", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("<b>TRANSACTION HISTORY</b>", heading_style))
    
    data = [
        ['Date', 'Description', 'Amount (USD)'],
        ['Sep 15', 'Client Payment - TechStart', '$2,800.00'],
        ['Oct 10', 'Client Payment - WebCo', '$3,200.00'],
        ['Nov 05', 'Client Payment - DesignHub', '$3,000.00'],
        ['Nov 28', 'Client Payment - CodeFactory', '$2,900.00']
    ]
    
    t = Table(data, colWidths=[1.5*inch, 3*inch, 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(t)
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Current Balance:</b> $18,450.00", normal_style))
    story.append(Paragraph("<i>Regular freelance income from established Singapore clients</i>", normal_style))
    
    doc.build(story)
    print("✓ low_sof.pdf created")
    
    # 2. Proof of Identity
    doc = SimpleDocTemplate(str(base_dir / "low_risk" / "low_id.pdf"), pagesize=letter)
    story = []
    
    story.append(Paragraph("REPUBLIC OF THE PHILIPPINES", title_style))
    story.append(Paragraph("PASSPORT", heading_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("<b>Passport No:</b> P9876543", normal_style))
    story.append(Paragraph("<b>Surname:</b> SANTOS", normal_style))
    story.append(Paragraph("<b>Given Names:</b> MARIA ELENA", normal_style))
    story.append(Paragraph("<b>Nationality:</b> FILIPINO", normal_style))
    story.append(Paragraph("<b>Date of Birth:</b> 15 May 1995", normal_style))
    story.append(Paragraph("<b>Place of Birth:</b> Manila, Philippines", normal_style))
    story.append(Paragraph("<b>Sex:</b> F", normal_style))
    story.append(Paragraph("<b>Date of Issue:</b> 10 January 2022", normal_style))
    story.append(Paragraph("<b>Date of Expiry:</b> 10 January 2032", normal_style))
    story.append(Paragraph("<b>Issuing Authority:</b> DFA Manila", normal_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("<i>SAMPLE DOCUMENT FOR TESTING PURPOSES</i>", normal_style))
    
    doc.build(story)
    print("✓ low_id.pdf created")
    
    # 3. Proof of Residency
    doc = SimpleDocTemplate(str(base_dir / "low_risk" / "low_residency.pdf"), pagesize=letter)
    story = []
    
    story.append(Paragraph("MERALCO", title_style))
    story.append(Paragraph("Manila Electric Company - Customer Service Bill", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Account Name:</b> Maria Santos", normal_style))
    story.append(Paragraph("<b>Service Address:</b> 456 Makati Avenue, Makati City 1200, Metro Manila, Philippines", normal_style))
    story.append(Paragraph("<b>Account Number:</b> 1234-5678-9012", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Billing Period:</b> November 1-30, 2024", normal_style))
    story.append(Paragraph("<b>Bill Date:</b> December 1, 2024", normal_style))
    story.append(Paragraph("<b>Due Date:</b> December 15, 2024", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Consumption:</b> 300 kWh", normal_style))
    story.append(Paragraph("<b>TOTAL AMOUNT DUE:</b> ₱3,450.00", normal_style))
    
    doc.build(story)
    print("✓ low_residency.pdf created")
    
    # 4. Invoice
    doc = SimpleDocTemplate(str(base_dir / "low_risk" / "low_invoice.pdf"), pagesize=letter)
    story = []
    
    story.append(Paragraph("INVOICE", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>INVOICE NUMBER:</b> MS-2024-11-028", normal_style))
    story.append(Paragraph("<b>DATE:</b> November 28, 2024", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>FROM:</b>", heading_style))
    story.append(Paragraph("Maria Santos - Freelance Web Designer", normal_style))
    story.append(Paragraph("456 Makati Avenue, Makati City, Philippines", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>TO:</b>", heading_style))
    story.append(Paragraph("TechStart Pte Ltd", normal_style))
    story.append(Paragraph("Marina Bay Financial Centre, Singapore 018983", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("<b>DESCRIPTION:</b>", heading_style))
    story.append(Paragraph("E-commerce Website UI/UX Design and Development", normal_style))
    story.append(Paragraph("Project Period: November 1-25, 2024", normal_style))
    story.append(Paragraph("120 hours @ $25/hour", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>TOTAL: $3,000.00 USD</b>", heading_style))
    story.append(Paragraph("Payment Method: USDT via Ripe", normal_style))
    
    doc.build(story)
    print("✓ low_invoice.pdf created")

def create_medium_risk_docs():
    """Generate Medium Risk scenario documents"""
    print("\nGenerating Medium Risk documents...")
    
    # 1. Source of Funds
    doc = SimpleDocTemplate(str(base_dir / "medium_risk" / "medium_sof.pdf"), pagesize=letter)
    story = []
    
    story.append(Paragraph("VIETCOMBANK", title_style))
    story.append(Paragraph("Business Account Statement", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Account Name:</b> Saigon Trading Co., Ltd", normal_style))
    story.append(Paragraph("<b>Account Number:</b> VN-987-654-321", normal_style))
    story.append(Paragraph("<b>Period:</b> August - November 2024", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    data = [
        ['Date', 'Description', 'Amount (USD)'],
        ['Aug 15', 'Export Customer Payment', '$25,000.00'],
        ['Sep 10', 'Supplier Payment Jakarta', '-$18,500.00'],
        ['Oct 15', 'Supplier Payment Indonesia', '-$18,000.00'],
        ['Nov 05', 'Customer Trade Payment', '$28,000.00']
    ]
    
    t = Table(data, colWidths=[1.5*inch, 3*inch, 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(t)
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Balance:</b> $112,300.00", normal_style))
    story.append(Paragraph("<i>Import-Export Electronics - Established trade pattern</i>", normal_style))
    
    doc.build(story)
    print("✓ medium_sof.pdf created")
    
    # 2. Business Registration
    doc = SimpleDocTemplate(str(base_dir / "medium_risk" / "medium_business.pdf"), pagesize=letter)
    story = []
    
    story.append(Paragraph("SOCIALIST REPUBLIC OF VIETNAM", title_style))
    story.append(Paragraph("BUSINESS REGISTRATION CERTIFICATE", heading_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("<b>Enterprise Name:</b> Saigon Trading Co., Ltd", normal_style))
    story.append(Paragraph("<b>Registration Number:</b> 0123456789", normal_style))
    story.append(Paragraph("<b>Registration Date:</b> March 15, 2021", normal_style))
    story.append(Paragraph("<b>Enterprise Type:</b> Limited Liability Company", normal_style))
    story.append(Paragraph("<b>Head Office:</b> District 1, Ho Chi Minh City, Vietnam", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Business:</b> Import-Export Electronic Components", normal_style))
    story.append(Paragraph("<b>Legal Representative:</b> Nguyen Van Minh", normal_style))
    story.append(Paragraph("<b>Status:</b> ACTIVE - In Good Standing", normal_style))
    
    doc.build(story)
    print("✓ medium_business.pdf created")
    
    # 3. ID
    doc = SimpleDocTemplate(str(base_dir / "medium_risk" / "medium_id.pdf"), pagesize=letter)
    story = []
    
    story.append(Paragraph("VIETNAM CITIZEN ID CARD", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("<b>ID Number:</b> 079085001234", normal_style))
    story.append(Paragraph("<b>Full Name:</b> NGUYEN VAN MINH", normal_style))
    story.append(Paragraph("<b>Date of Birth:</b> 20/03/1985", normal_style))
    story.append(Paragraph("<b>Place of Residence:</b> District 1, Ho Chi Minh City", normal_style))
    story.append(Paragraph("<b>Issue Date:</b> 05/01/2020", normal_style))
    story.append(Paragraph("<b>Expiry Date:</b> 05/01/2040", normal_style))
    
    doc.build(story)
    print("✓ medium_id.pdf created")
    
    # 4. Invoice
    doc = SimpleDocTemplate(str(base_dir / "medium_risk" / "medium_invoice.pdf"), pagesize=letter)
    story = []
    
    story.append(Paragraph("PROFORMA INVOICE", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>INVOICE NO:</b> ST-2024-11-042", normal_style))
    story.append(Paragraph("<b>DATE:</b> November 25, 2024", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>FROM:</b> Jakarta Electronics Supply, Indonesia", normal_style))
    story.append(Paragraph("<b>TO:</b> Saigon Trading Co Ltd, Vietnam", normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    data = [
        ['Item', 'Qty', 'Unit Price', 'Total'],
        ['LED Display Modules', '500', '$28.00', '$14,000'],
        ['Circuit Boards Type-A', '200', '$20.00', '$4,000']
    ]
    
    t = Table(data, colWidths=[2.5*inch, 1*inch, 1.2*inch, 1.2*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(t)
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>TOTAL: $18,000.00 USD</b>", heading_style))
    story.append(Paragraph("Purpose: Import Electronic Components", normal_style))
    
    doc.build(story)
    print("✓ medium_invoice.pdf created")

def create_high_risk_docs():
    """Generate High Risk scenario documents"""
    print("\nGenerating High Risk documents...")
    
    # 1. Source of Funds with structuring
    doc = SimpleDocTemplate(str(base_dir / "high_risk" / "high_sof.pdf"), pagesize=letter)
    story = []
    
    story.append(Paragraph("FINANCIAL STATEMENT", title_style))
    story.append(Paragraph("Global Ventures Ltd - Cayman Islands", heading_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("<b>Recent Receipts - November 2024:</b>", heading_style))
    
    data = [
        ['Date', 'Description', 'Amount (USD)'],
        ['Nov 01', 'Wire Transfer - Source Unknown', '$9,900.00'],
        ['Nov 03', 'Wire Transfer - Source Unknown', '$9,800.00'],
        ['Nov 05', 'Cash Equivalent Deposit', '$9,700.00'],
        ['Nov 08', 'Wire Transfer - Source Unknown', '$9,900.00'],
        ['Nov 12', 'Transfer - Various Sources', '$9,850.00']
    ]
    
    t = Table(data, colWidths=[1.2*inch, 3*inch, 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.red),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(t)
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Total Accumulated:</b> $58,900.00", normal_style))
    story.append(Paragraph("<i>Note: Multiple transactions just under $10k threshold</i>", normal_style))
    
    doc.build(story)
    print("✓ high_sof.pdf created")
    
    # 2. Offshore Business Registration
    doc = SimpleDocTemplate(str(base_dir / "high_risk" / "high_business.pdf"), pagesize=letter)
    story = []
    
    story.append(Paragraph("CAYMAN ISLANDS", title_style))
    story.append(Paragraph("CERTIFICATE OF INCORPORATION", heading_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("<b>Company Name:</b> Global Ventures Ltd", normal_style))
    story.append(Paragraph("<b>Company Number:</b> 123456", normal_style))
    story.append(Paragraph("<b>Date of Incorporation:</b> May 15, 2024 (6 months ago)", normal_style))
    story.append(Paragraph("<b>Type:</b> Exempted Company", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>Registered Office:</b> PO Box 1234, George Town, Grand Cayman", normal_style))
    story.append(Paragraph("<b>Directors:</b> Nominee Director Services Ltd", normal_style))
    story.append(Paragraph("<b>Shareholders:</b> Bearer Shares (Not Disclosed)", normal_style))
    story.append(Paragraph("<b>Business Activity:</b> Investment Holdings and General Business", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<i>Offshore Jurisdiction - Anonymous Ownership</i>", normal_style))
    
    doc.build(story)
    print("✓ high_business.pdf created")
    
    # 3. Nigerian Passport
    doc = SimpleDocTemplate(str(base_dir / "high_risk" / "high_id.pdf"), pagesize=letter)
    story = []
    
    story.append(Paragraph("FEDERAL REPUBLIC OF NIGERIA", title_style))
    story.append(Paragraph("PASSPORT", heading_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("<b>Passport No:</b> A1234567", normal_style))
    story.append(Paragraph("<b>Surname:</b> OKONKWO", normal_style))
    story.append(Paragraph("<b>Given Names:</b> JOHN EMMANUEL", normal_style))
    story.append(Paragraph("<b>Nationality:</b> NIGERIAN", normal_style))
    story.append(Paragraph("<b>Date of Birth:</b> 10/08/1980", normal_style))
    story.append(Paragraph("<b>Date of Issue:</b> 15 September 2024 (Very Recent!)", normal_style))
    story.append(Paragraph("<b>Date of Expiry:</b> 15 September 2034", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<i>Director of Global Ventures Ltd (Cayman Islands)</i>", normal_style))
    
    doc.build(story)
    print("✓ high_id.pdf created")
    
    # 4. Vague Investment Agreement
    doc = SimpleDocTemplate(str(base_dir / "high_risk" / "high_investment.pdf"), pagesize=letter)
    story = []
    
    story.append(Paragraph("INVESTMENT AGREEMENT", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("<b>Date:</b> November 28, 2024", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<b>INVESTOR:</b>", heading_style))
    story.append(Paragraph("Global Ventures Ltd", normal_style))
    story.append(Paragraph("Cayman Islands", normal_style))
    story.append(Paragraph("Represented by: John Okonkwo, Director", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>TARGET:</b> Vietnam Property Holdings", normal_style))
    story.append(Paragraph("<b>Amount:</b> USD $35,000.00", normal_style))
    story.append(Paragraph("<b>Purpose:</b> Real estate development investment", normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>TERMS:</b>", heading_style))
    story.append(Paragraph("- Investment structure: To be determined", normal_style))
    story.append(Paragraph("- Returns: Subject to project performance", normal_style))
    story.append(Paragraph("- Specific details: Pending finalization", normal_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("<i>Preliminary Agreement - Vague Terms</i>", normal_style))
    
    doc.build(story)
    print("✓ high_investment.pdf created")

if __name__ == "__main__":
    print("=" * 60)
    print("  Generating Mock Compliance Documents")
    print("=" * 60)
    
    create_low_risk_docs()
    create_medium_risk_docs()
    create_high_risk_docs()
    
    print("\n" + "=" * 60)
    print("✅ Document generation complete!")
    print("=" * 60)
    print(f"\nDocuments saved to: {base_dir}")
    print("\nNext steps:")
    print("1. Review the generated PDFs")
    print("2. Go to http://localhost:8000")
    print("3. Fill form with data from scenario .md files")
    print("4. Upload corresponding PDFs")
    print("5. Submit and see results!")

