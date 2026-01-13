"""
Example usage of the OCR Compliance System with Tesseract
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Example 1: Basic OCR Processing
def example_basic_ocr():
    """Example: Process a single image"""
    print("=" * 60)
    print("Example 1: Basic OCR Processing")
    print("=" * 60)
    
    from services.ocr_service import OCRService
    
    # Initialize OCR service
    ocr = OCRService()
    
    # Process an image
    image_path = 'uploads/sample_label.jpg'
    
    if not os.path.exists(image_path):
        print(f"⚠ Sample image not found: {image_path}")
        print("  Please upload an image to the uploads folder")
        return
    
    print(f"\nProcessing: {image_path}")
    result = ocr.process_image(image_path)
    
    print("\n--- OCR Results ---")
    print(f"Confidence Score: {result['confidence_score']:.2%}")
    print(f"Processing Time: {result['processing_time']:.2f}s")
    print(f"\nExtracted Text:")
    print("-" * 60)
    print(result['extracted_text'])
    print("-" * 60)
    
    print(f"\n--- Pharmaceutical Data ---")
    print(f"Drug Name: {result.get('drug_name', 'Not found')}")
    print(f"Batch Number: {result.get('batch_number', 'Not found')}")
    print(f"Expiry Date: {result.get('expiry_date', 'Not found')}")
    print(f"Manufacturer: {result.get('manufacturer', 'Not found')}")
    print(f"Controlled Substance: {result.get('controlled_substance', False)}")


# Example 2: PDF Processing
def example_pdf_processing():
    """Example: Process a PDF document"""
    print("\n" + "=" * 60)
    print("Example 2: PDF Processing")
    print("=" * 60)
    
    from services.ocr_service import OCRService
    
    ocr = OCRService()
    
    pdf_path = 'uploads/sample_document.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"⚠ Sample PDF not found: {pdf_path}")
        print("  Please upload a PDF to the uploads folder")
        return
    
    print(f"\nProcessing: {pdf_path}")
    result = ocr.process_pdf(pdf_path)
    
    print("\n--- PDF OCR Results ---")
    print(f"Confidence Score: {result['confidence_score']:.2%}")
    print(f"Processing Time: {result['processing_time']:.2f}s")
    print(f"\nExtracted Text (first 500 chars):")
    print("-" * 60)
    print(result['extracted_text'][:500])
    print("-" * 60)


# Example 3: Compliance Validation
def example_compliance_check():
    """Example: Validate OCR results for compliance"""
    print("\n" + "=" * 60)
    print("Example 3: Compliance Validation")
    print("=" * 60)
    
    from services.ocr_service import OCRService
    from services.compliance_service import ComplianceService
    
    ocr = OCRService()
    compliance = ComplianceService()
    
    # Mock OCR data for demonstration
    ocr_data = {
        'extracted_text': 'ACETAMINOPHEN 500mg\nBatch: BN-2024-001234\nExpiry: 12/2025',
        'drug_name': 'ACETAMINOPHEN 500mg',
        'batch_number': 'BN-2024-001234',
        'expiry_date': '12/2025',
        'manufacturer': 'PharmaCorp Inc.',
        'controlled_substance': False
    }
    
    print("\nValidating OCR data...")
    checks = compliance.validate_ocr_result(ocr_data)
    
    print("\n--- Compliance Checks ---")
    for check in checks:
        status_icon = "✓" if check['status'] == 'passed' else "✗"
        print(f"{status_icon} {check['rule_name']}")
        print(f"  Type: {check['check_type']}")
        print(f"  Status: {check['status']}")
        print(f"  Severity: {check['severity']}")
        print(f"  Message: {check['message']}")
        print()
    
    # Calculate compliance score
    score = compliance.calculate_compliance_score(checks)
    print(f"Overall Compliance Score: {score:.1f}%")


# Example 4: Error Detection
def example_error_detection():
    """Example: Detect errors in OCR results"""
    print("\n" + "=" * 60)
    print("Example 4: Error Detection")
    print("=" * 60)
    
    from services.error_detection_service import ErrorDetectionService
    
    error_service = ErrorDetectionService()
    
    # Mock OCR data with potential errors
    ocr_data = {
        'extracted_text': 'ACETAM1N0PHEN 500mg',  # OCR errors: 1 instead of I, 0 instead of O
        'drug_name': 'ACETAM1N0PHEN 500mg',
        'batch_number': 'BN-2O24-001234',  # O instead of 0
        'expiry_date': '12-2025',  # Wrong format
        'manufacturer': 'PharmaCorp',
        'controlled_substance': False
    }
    
    print("\nDetecting errors...")
    errors = error_service.detect_errors(ocr_data)
    
    print("\n--- Detected Errors ---")
    if errors:
        for i, error in enumerate(errors, 1):
            print(f"\nError {i}:")
            print(f"  Type: {error['error_type']}")
            print(f"  Field: {error['field_name']}")
            print(f"  Actual: {error['actual_value']}")
            print(f"  Expected: {error.get('expected_value', 'N/A')}")
            print(f"  Confidence: {error['confidence']:.2%}")
            print(f"  Suggestion: {error.get('suggestion', 'N/A')}")
    else:
        print("✓ No errors detected")
    
    # Get correction suggestions
    suggestions = error_service.suggest_corrections(errors)
    print(f"\n--- Correction Summary ---")
    print(f"Total Errors: {suggestions['total_errors']}")
    print(f"Critical Errors: {suggestions['critical_errors']}")
    
    if suggestions['corrections']:
        print("\nSuggested Corrections:")
        for correction in suggestions['corrections']:
            print(f"  • {correction['field']}: {correction['current']} → {correction['suggested']}")


# Example 5: Advanced Tesseract Features
def example_advanced_tesseract():
    """Example: Use advanced Tesseract features"""
    print("\n" + "=" * 60)
    print("Example 5: Advanced Tesseract Features")
    print("=" * 60)
    
    from services.ocr_service import TesseractOCRService
    
    # Initialize with custom language
    ocr = TesseractOCRService(lang='eng')
    
    image_path = 'uploads/sample_label.jpg'
    
    if not os.path.exists(image_path):
        print(f"⚠ Sample image not found: {image_path}")
        return
    
    print(f"\nProcessing with layout analysis: {image_path}")
    result = ocr.process_with_layout_analysis(image_path)
    
    print("\n--- Layout Analysis Results ---")
    print(f"Confidence Score: {result['confidence_score']:.2%}")
    
    if 'structured_data' in result:
        words = result['structured_data']['words']
        print(f"\nDetected {len(words)} words")
        
        # Show first 5 words with bounding boxes
        print("\nFirst 5 words with positions:")
        for i, word in enumerate(words[:5], 1):
            print(f"{i}. '{word['text']}' at ({word['bbox']['x']}, {word['bbox']['y']}) "
                  f"confidence: {word['confidence']}%")


# Example 6: Batch Processing
def example_batch_processing():
    """Example: Process multiple images"""
    print("\n" + "=" * 60)
    print("Example 6: Batch Processing")
    print("=" * 60)
    
    from services.ocr_service import OCRService
    import glob
    
    ocr = OCRService()
    
    # Find all images in uploads folder
    image_files = glob.glob('uploads/*.jpg') + glob.glob('uploads/*.png')
    
    if not image_files:
        print("⚠ No images found in uploads folder")
        return
    
    print(f"\nFound {len(image_files)} images to process")
    
    results = []
    for image_path in image_files:
        print(f"\nProcessing: {os.path.basename(image_path)}")
        try:
            result = ocr.process_image(image_path)
            results.append({
                'file': os.path.basename(image_path),
                'confidence': result['confidence_score'],
                'drug_name': result.get('drug_name', 'Not found')
            })
            print(f"  ✓ Confidence: {result['confidence_score']:.2%}")
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
    
    # Summary
    print("\n--- Batch Processing Summary ---")
    print(f"Total Processed: {len(results)}")
    if results:
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        print(f"Average Confidence: {avg_confidence:.2%}")
        
        print("\nResults:")
        for r in results:
            print(f"  • {r['file']}: {r['drug_name']} ({r['confidence']:.2%})")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("OCR COMPLIANCE SYSTEM - USAGE EXAMPLES")
    print("=" * 60)
    
    examples = [
        ("Basic OCR", example_basic_ocr),
        ("PDF Processing", example_pdf_processing),
        ("Compliance Check", example_compliance_check),
        ("Error Detection", example_error_detection),
        ("Advanced Tesseract", example_advanced_tesseract),
        ("Batch Processing", example_batch_processing)
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    print("\nRunning all examples...\n")
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n✗ Example '{name}' failed: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
