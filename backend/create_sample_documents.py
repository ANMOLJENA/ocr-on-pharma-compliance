#!/usr/bin/env python3
"""
Create sample pharmaceutical documents for testing OCR system
"""

from PIL import Image, ImageDraw, ImageFont
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import datetime

def create_sample_images():
    """Create sample pharmaceutical label images"""
    
    # Create samples directory
    samples_dir = "samples"
    if not os.path.exists(samples_dir):
        os.makedirs(samples_dir)
    
    # Sample 1: Standard pharmaceutical label
    img1 = Image.new('RGB', (600, 400), color='white')
    draw1 = ImageDraw.Draw(img1)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_medium = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw border
    draw1.rectangle([10, 10, 590, 390], outline='black', width=2)
    
    # Sample 1 content
    draw1.text((20, 30), "PHARMACEUTICAL LABEL", fill='black', font=font_large)
    draw1.text((20, 70), "Drug Name: ACETAMINOPHEN 500mg", fill='black', font=font_medium)
    draw1.text((20, 100), "Batch Number: BN-2024-001234", fill='black', font=font_medium)
    draw1.text((20, 130), "Expiry Date: 12/12/2025", fill='black', font=font_medium)
    draw1.text((20, 160), "Manufacturer: PharmaCorpInc.", fill='black', font=font_medium)
    draw1.text((20, 200), "NDC: 12345-678-90", fill='black', font=font_small)
    draw1.text((20, 230), "Lot: L2024001", fill='black', font=font_small)
    draw1.text((20, 260), "Qty: 30 tablets", fill='black', font=font_small)
    draw1.text((20, 320), "CONTROLLED SUBSTANCE", fill='red', font=font_medium)
    draw1.text((20, 350), "Schedule II", fill='red', font=font_small)
    
    img1.save(f"{samples_dir}/pharma_label_1.png")
    print("✓ Created: pharma_label_1.png")
    
    # Sample 2: Prescription bottle label
    img2 = Image.new('RGB', (500, 600), color='white')
    draw2 = ImageDraw.Draw(img2)
    
    # Draw border
    draw2.rectangle([10, 10, 490, 590], outline='blue', width=3)
    
    # Sample 2 content
    draw2.text((20, 30), "RX PRESCRIPTION", fill='blue', font=font_large)
    draw2.text((20, 80), "Patient: John Doe", fill='black', font=font_medium)
    draw2.text((20, 110), "Drug: LISINOPRIL 10mg", fill='black', font=font_medium)
    draw2.text((20, 140), "Batch: LN-2024-567890", fill='black', font=font_medium)
    draw2.text((20, 170), "Exp Date: 06/15/2026", fill='black', font=font_medium)
    draw2.text((20, 200), "Mfg: HeartMed Pharmaceuticals", fill='black', font=font_medium)
    draw2.text((20, 240), "Directions:", fill='black', font=font_medium)
    draw2.text((20, 270), "Take 1 tablet daily", fill='black', font=font_small)
    draw2.text((20, 300), "Qty: 90 tablets", fill='black', font=font_small)
    draw2.text((20, 330), "Refills: 2", fill='black', font=font_small)
    draw2.text((20, 370), "Pharmacy: MediCare Pharmacy", fill='black', font=font_small)
    draw2.text((20, 400), "Phone: (555) 123-4567", fill='black', font=font_small)
    draw2.text((20, 450), "Date Filled: 01/15/2025", fill='black', font=font_small)
    draw2.text((20, 500), "RPh: Dr. Sarah Johnson", fill='black', font=font_small)
    
    img2.save(f"{samples_dir}/prescription_label_2.png")
    print("✓ Created: prescription_label_2.png")
    
    # Sample 3: Insulin vial label (controlled substance)
    img3 = Image.new('RGB', (400, 300), color='lightblue')
    draw3 = ImageDraw.Draw(img3)
    
    # Draw border
    draw3.rectangle([5, 5, 395, 295], outline='darkblue', width=2)
    
    # Sample 3 content
    draw3.text((15, 20), "INSULIN VIAL", fill='darkblue', font=font_large)
    draw3.text((15, 60), "NOVOLOG 100 units/mL", fill='black', font=font_medium)
    draw3.text((15, 90), "Batch: INS-2024-789012", fill='black', font=font_medium)
    draw3.text((15, 120), "Exp: 08/30/2025", fill='black', font=font_medium)
    draw3.text((15, 150), "Mfg: Novo Nordisk", fill='black', font=font_medium)
    draw3.text((15, 180), "10mL vial", fill='black', font=font_small)
    draw3.text((15, 210), "Store in refrigerator", fill='red', font=font_small)
    draw3.text((15, 240), "PRESCRIPTION ONLY", fill='red', font=font_small)
    
    img3.save(f"{samples_dir}/insulin_label_3.png")
    print("✓ Created: insulin_label_3.png")

def create_sample_pdf():
    """Create a sample PDF with pharmaceutical information"""
    
    samples_dir = "samples"
    if not os.path.exists(samples_dir):
        os.makedirs(samples_dir)
    
    pdf_path = f"{samples_dir}/pharma_document.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "PHARMACEUTICAL BATCH RECORD")
    
    # Document info
    c.setFont("Helvetica", 12)
    y_pos = height - 100
    
    lines = [
        "Document ID: PBR-2024-001",
        "Date: January 15, 2025",
        "",
        "PRODUCT INFORMATION:",
        "Drug Name: METFORMIN HCl 500mg Tablets",
        "Batch Number: MET-2024-445566",
        "Manufacturing Date: 01/10/2025",
        "Expiry Date: 01/10/2027",
        "Manufacturer: DiabetesCare Pharmaceuticals Inc.",
        "",
        "BATCH DETAILS:",
        "Lot Size: 100,000 tablets",
        "Equipment Used: Tablet Press TP-500",
        "Operator: Jane Smith",
        "QC Analyst: Dr. Michael Brown",
        "",
        "QUALITY CONTROL RESULTS:",
        "Assay: 99.2% (Specification: 95.0-105.0%)",
        "Dissolution: Compliant",
        "Uniformity: Passed",
        "Microbial Limits: Passed",
        "",
        "CONTROLLED SUBSTANCE INFORMATION:",
        "DEA Schedule: Not Controlled",
        "Storage Requirements: Store at 20-25°C",
        "",
        "APPROVAL:",
        "QA Manager: Dr. Lisa Wilson",
        "Date Approved: 01/15/2025",
        "Electronic Signature: LW-20250115-001"
    ]
    
    for line in lines:
        if line.startswith("PRODUCT INFORMATION:") or line.startswith("BATCH DETAILS:") or line.startswith("QUALITY CONTROL") or line.startswith("CONTROLLED SUBSTANCE") or line.startswith("APPROVAL:"):
            c.setFont("Helvetica-Bold", 12)
        else:
            c.setFont("Helvetica", 11)
        
        c.drawString(50, y_pos, line)
        y_pos -= 20
        
        if y_pos < 50:  # Start new page if needed
            c.showPage()
            y_pos = height - 50
    
    c.save()
    print("✓ Created: pharma_document.pdf")

def create_challenging_sample():
    """Create a sample with potential OCR challenges"""
    
    samples_dir = "samples"
    if not os.path.exists(samples_dir):
        os.makedirs(samples_dir)
    
    # Sample with common OCR errors
    img4 = Image.new('RGB', (550, 350), color='lightyellow')
    draw4 = ImageDraw.Draw(img4)
    
    try:
        font_medium = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw border
    draw4.rectangle([10, 10, 540, 340], outline='orange', width=2)
    
    # Content with potential OCR challenges (similar characters)
    draw4.text((20, 30), "CHALLENGING OCR SAMPLE", fill='darkorange', font=font_medium)
    draw4.text((20, 70), "Drug: 0XYCODONE 5mg (O vs 0)", fill='black', font=font_medium)
    draw4.text((20, 100), "Batch: 8N-2024-001l23 (B vs 8, I vs l)", fill='black', font=font_medium)
    draw4.text((20, 130), "Exp: 0l/l5/2025 (0 vs O, 1 vs l)", fill='black', font=font_medium)
    draw4.text((20, 160), "Mfg: PainReIief Corp (l vs I)", fill='black', font=font_medium)
    draw4.text((20, 200), "Lot: G0O8l23 (G vs 6, O vs 0)", fill='black', font=font_small)
    draw4.text((20, 230), "NDC: 5432l-678-9O (l vs 1, O vs 0)", fill='black', font=font_small)
    draw4.text((20, 270), "CONTROLLED SUBSTANCE", fill='red', font=font_medium)
    draw4.text((20, 300), "Schedule Il (I vs l)", fill='red', font=font_small)
    
    img4.save(f"{samples_dir}/challenging_ocr_4.png")
    print("✓ Created: challenging_ocr_4.png")

if __name__ == "__main__":
    print("Creating sample pharmaceutical documents...")
    print("=" * 50)
    
    try:
        create_sample_images()
        create_sample_pdf()
        create_challenging_sample()
        
        print("=" * 50)
        print("✅ All sample documents created successfully!")
        print("\nSample files created in 'samples/' directory:")
        print("- pharma_label_1.png (Standard pharmaceutical label)")
        print("- prescription_label_2.png (Prescription bottle label)")
        print("- insulin_label_3.png (Insulin vial label)")
        print("- pharma_document.pdf (Batch record PDF)")
        print("- challenging_ocr_4.png (OCR challenge test)")
        print("\nYou can now upload these files to test your OCR system!")
        
    except Exception as e:
        print(f"❌ Error creating samples: {e}")
        print("Make sure you have PIL (Pillow) and reportlab installed:")
        print("pip install Pillow reportlab")