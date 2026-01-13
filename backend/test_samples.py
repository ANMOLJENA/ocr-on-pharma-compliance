#!/usr/bin/env python3
"""
Test the OCR system with sample documents
"""

import requests
import os
import json

def test_ocr_with_samples():
    """Test OCR API with sample documents"""
    
    api_url = "http://localhost:5000"
    samples_dir = "samples"
    
    if not os.path.exists(samples_dir):
        print("❌ Samples directory not found. Run create_sample_documents.py first.")
        return
    
    # Test files
    test_files = [
        "pharma_label_1.png",
        "prescription_label_2.png", 
        "insulin_label_3.png",
        "challenging_ocr_4.png",
        "pharma_document.pdf"
    ]
    
    print("Testing OCR API with sample documents...")
    print("=" * 60)
    
    for filename in test_files:
        filepath = os.path.join(samples_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {filename}")
            continue
            
        print(f"\n📄 Testing: {filename}")
        print("-" * 40)
        
        try:
            # Upload file to OCR API
            with open(filepath, 'rb') as f:
                files = {'file': (filename, f, 'application/octet-stream')}
                data = {'ocr_engine': 'tesseract'}
                
                response = requests.post(
                    f"{api_url}/api/ocr/process",
                    files=files,
                    data=data,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                
                print("✅ OCR Processing successful!")
                print(f"📊 Accuracy: {result.get('accuracy', 'N/A')}%")
                print(f"🔍 Extracted Text Preview:")
                
                # Show first 200 characters of extracted text
                extracted_text = result.get('extracted_text', '')
                preview = extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text
                print(f"   {preview}")
                
                # Show compliance results
                compliance = result.get('compliance_results', {})
                if compliance:
                    print(f"📋 Compliance Check:")
                    for field, found in compliance.items():
                        status = "✅" if found else "❌"
                        print(f"   {status} {field.replace('_', ' ').title()}: {'Found' if found else 'Not Found'}")
                
                # Show error detections
                errors = result.get('error_detections', [])
                if errors:
                    print(f"🔧 Error Detections: {len(errors)} found")
                    for error in errors[:3]:  # Show first 3 errors
                        print(f"   • {error.get('error_type', 'Unknown')}: {error.get('suggestion', 'No suggestion')}")
                
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the Flask server is running on http://localhost:5000")
            break
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
    
    print("\n" + "=" * 60)
    print("✅ OCR testing complete!")
    print("\n💡 Tips:")
    print("- Upload these files through the web interface at http://localhost:8083")
    print("- Check the analytics dashboard for detailed results")
    print("- Try the challenging_ocr_4.png to test error detection")

if __name__ == "__main__":
    test_ocr_with_samples()