#!/usr/bin/env python
"""
Test script for multilingual OCR functionality
"""

import os
import sys
from services.multilingual_ocr_service import MultilingualOCRService

def test_multilingual_ocr():
    """Test multilingual OCR with sample files"""
    
    service = MultilingualOCRService()
    
    # Test with French sample
    french_sample = 'samples/pharma_label_french.png'
    
    if not os.path.exists(french_sample):
        print(f"[TEST] Sample file not found: {french_sample}")
        return
    
    print("[TEST] Testing multilingual OCR with French sample...")
    print(f"[TEST] File: {french_sample}")
    
    try:
        result = service.process_image_multilingual(french_sample)
        
        print("\n[TEST] ===== RESULT =====")
        print(f"[TEST] Detected Language: {result.get('detected_language')}")
        print(f"[TEST] Original Language: {result.get('original_language')}")
        print(f"[TEST] Translated: {result.get('translated')}")
        print(f"[TEST] Confidence: {result.get('confidence_score')}")
        
        print("\n[TEST] ===== ORIGINAL TEXT =====")
        original = result.get('original_text', result.get('extracted_text'))
        print(original[:500] if original else "No text")
        
        if result.get('translated'):
            print("\n[TEST] ===== TRANSLATED TEXT =====")
            translated = result.get('extracted_text')
            print(translated[:500] if translated else "No translation")
        
        print("\n[TEST] ===== SUCCESS =====")
        print("[TEST] Multilingual OCR test completed successfully!")
        
    except Exception as e:
        print(f"\n[TEST] ===== ERROR =====")
        print(f"[TEST] Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_multilingual_ocr()
