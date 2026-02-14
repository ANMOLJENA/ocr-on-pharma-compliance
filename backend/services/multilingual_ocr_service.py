"""
Multilingual OCR Service - Detects language and translates to English
"""

import re
from typing import Dict, Any, Tuple
from .ocr_service import TesseractOCRService
from .translation_service import TranslationService
from .language_detection_service import LanguageDetectionService
import pytesseract


class MultilingualOCRService(TesseractOCRService):
    """
    OCR Service with multilingual support
    Automatically detects language and translates to English
    """
    
    # Language code mappings for display
    LANGUAGE_NAMES = {
        'en': 'English',
        'fr': 'French',
        'de': 'German',
        'es': 'Spanish',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'bn': 'Bengali',
        'nl': 'Dutch',
        'sv': 'Swedish',
        'pl': 'Polish',
        'tr': 'Turkish',
        'el': 'Greek',
        'he': 'Hebrew',
        'th': 'Thai',
        'ta': 'Tamil',
        'te': 'Telugu',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'gu': 'Gujarati',
        'mr': 'Marathi',
        'pa': 'Punjabi',
        'ur': 'Urdu',
        'et': 'Estonian',
    }
    
    def __init__(self, tesseract_cmd: str = None):
        """
        Initialize Multilingual OCR Service
        
        Args:
            tesseract_cmd: Path to tesseract executable
        """
        super().__init__(tesseract_cmd, lang='eng')
        self.detected_language = None
        self.original_text = None
        self.translated_text = None
    
    def process_image_multilingual(self, image_path: str) -> Dict[str, Any]:
        """
        Process image with automatic language detection and translation
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with OCR results in English
        """
        try:
            # Process image with English first to get text
            result = self.process_image(image_path)
            extracted_text = result.get('extracted_text', '')
            
            print(f"[MULTILINGUAL] Extracted text length: {len(extracted_text)}")
            print(f"[MULTILINGUAL] Extracted text (first 100 chars): {extracted_text[:100]}")
            
            # Detect language from extracted text
            lang_detection = LanguageDetectionService.detect_language(extracted_text)
            print(f"[MULTILINGUAL] Language detection result: {lang_detection}")
            
            if lang_detection['success']:
                detected_lang_code = lang_detection['language_code']
                detected_lang_name = lang_detection['language_name']
                confidence = lang_detection['confidence']
                
                print(f"[MULTILINGUAL] Detected language: {detected_lang_name} ({detected_lang_code}) - Confidence: {confidence}")
                
                # Translate to English if not already English
                if detected_lang_code.lower() != 'en':
                    result['original_language'] = detected_lang_name
                    result['original_text'] = extracted_text
                    result['detected_language'] = detected_lang_name
                    result['detected_language_code'] = detected_lang_code
                    result['confidence'] = confidence
                    
                    # Translate text using MyMemory API
                    print(f"[MULTILINGUAL] Translating from {detected_lang_code} to English...")
                    print(f"[MULTILINGUAL] Text to translate: {extracted_text[:100]}...")
                    
                    translation_result = TranslationService.translate_to_english(extracted_text, detected_lang_code)
                    
                    print(f"[MULTILINGUAL] Translation result: {translation_result}")
                    
                    if translation_result['success']:
                        result['extracted_text'] = translation_result['translated_text']
                        result['translated'] = True
                        print(f"[MULTILINGUAL] Translation complete. Translated text length: {len(translation_result['translated_text'])}")
                        print(f"[MULTILINGUAL] Translated text (first 100 chars): {translation_result['translated_text'][:100]}")
                    else:
                        print(f"[MULTILINGUAL] Translation failed: {translation_result['error']}")
                        result['translated'] = False
                        result['translation_error'] = translation_result['error']
                else:
                    result['original_language'] = 'English'
                    result['detected_language'] = 'English'
                    result['detected_language_code'] = 'en'
                    result['confidence'] = confidence
                    result['translated'] = False
            else:
                print(f"[MULTILINGUAL] Language detection failed: {lang_detection['error']}")
                result['detected_language'] = 'Unknown'
                result['translated'] = False
                result['detection_error'] = lang_detection['error']
            
            print(f"[MULTILINGUAL] Final result - Translated: {result.get('translated')}, Language: {result.get('detected_language')}")
            
            return result
            
        except Exception as e:
            print(f"[MULTILINGUAL] Error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Multilingual OCR processing failed: {str(e)}")
    
    def process_pdf_multilingual(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process PDF with automatic language detection and translation
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with OCR results in English
        """
        try:
            # Process PDF normally first
            result = self.process_pdf(pdf_path)
            extracted_text = result.get('extracted_text', '')
            
            # Detect language from extracted text
            lang_detection = LanguageDetectionService.detect_language(extracted_text)
            
            if lang_detection['success']:
                detected_lang_code = lang_detection['language_code']
                detected_lang_name = lang_detection['language_name']
                confidence = lang_detection['confidence']
                
                # Translate if not English
                if detected_lang_code.lower() != 'en':
                    result['original_language'] = detected_lang_name
                    result['original_text'] = extracted_text
                    result['detected_language'] = detected_lang_name
                    result['detected_language_code'] = detected_lang_code
                    result['confidence'] = confidence
                    
                    translation_result = TranslationService.translate_to_english(extracted_text, detected_lang_code)
                    
                    if translation_result['success']:
                        result['extracted_text'] = translation_result['translated_text']
                        result['translated'] = True
                    else:
                        result['translated'] = False
                        result['translation_error'] = translation_result['error']
                else:
                    result['original_language'] = 'English'
                    result['detected_language'] = 'English'
                    result['detected_language_code'] = 'en'
                    result['confidence'] = confidence
                    result['translated'] = False
            else:
                result['detected_language'] = 'Unknown'
                result['translated'] = False
                result['detection_error'] = lang_detection['error']
            
            return result
            
        except Exception as e:
            raise Exception(f"Multilingual PDF processing failed: {str(e)}")
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get list of supported languages
        
        Returns:
            Dictionary of language codes and names
        """
        return self.LANGUAGE_NAMES.copy()
