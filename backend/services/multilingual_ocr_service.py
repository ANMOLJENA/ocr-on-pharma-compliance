"""
Multilingual OCR Service - Detects language and translates to English
"""

import re
from typing import Dict, Any, Tuple
from .ocr_service import TesseractOCRService
import pytesseract

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

try:
    from google.cloud import translate_v2
    GOOGLE_TRANSLATE_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False

try:
    import langdetect
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

try:
    from deep_translator import GoogleTranslator
    DEEP_TRANSLATOR_AVAILABLE = True
except ImportError:
    DEEP_TRANSLATOR_AVAILABLE = False


class MultilingualOCRService(TesseractOCRService):
    """
    OCR Service with multilingual support
    Automatically detects language and translates to English
    """
    
    # Tesseract language codes mapping
    LANGUAGE_CODES = {
        'eng': 'English',
        'fra': 'French',
        'deu': 'German',
        'spa': 'Spanish',
        'ita': 'Italian',
        'por': 'Portuguese',
        'rus': 'Russian',
        'jpn': 'Japanese',
        'kor': 'Korean',
        'zho': 'Chinese',
        'ara': 'Arabic',
        'hin': 'Hindi',
        'ben': 'Bengali',
        'nld': 'Dutch',
        'swe': 'Swedish',
        'pol': 'Polish',
        'tur': 'Turkish',
        'gre': 'Greek',
        'heb': 'Hebrew',
        'tha': 'Thai',
    }
    
    def __init__(self, tesseract_cmd: str = None, translation_service: str = 'textblob'):
        """
        Initialize Multilingual OCR Service
        
        Args:
            tesseract_cmd: Path to tesseract executable
            translation_service: 'textblob' or 'google' for translation
        """
        super().__init__(tesseract_cmd, lang='eng')
        self.translation_service = translation_service
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
            # First, try to detect language from image
            detected_lang = self._detect_language_from_image(image_path)
            print(f"[MULTILINGUAL] Detected language: {detected_lang}")
            
            # Process image with detected language
            result = self._process_with_language(image_path, detected_lang)
            print(f"[MULTILINGUAL] Extracted text length: {len(result.get('extracted_text', ''))}")
            
            # Translate to English if not already English
            if detected_lang != 'eng':
                result['original_language'] = self.LANGUAGE_CODES.get(detected_lang, detected_lang)
                result['original_text'] = result['extracted_text']
                
                # Translate text
                print(f"[MULTILINGUAL] Translating from {detected_lang} to English...")
                translated_text = self._translate_to_english(result['extracted_text'])
                print(f"[MULTILINGUAL] Translation complete. Translated text length: {len(translated_text)}")
                
                result['extracted_text'] = translated_text
                result['translated'] = True
            else:
                result['original_language'] = 'English'
                result['translated'] = False
            
            result['detected_language'] = self.LANGUAGE_CODES.get(detected_lang, detected_lang)
            print(f"[MULTILINGUAL] Final result - Translated: {result.get('translated')}, Language: {result.get('detected_language')}")
            
            return result
            
        except Exception as e:
            print(f"[MULTILINGUAL] Error: {str(e)}")
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
            
            # Detect language from extracted text
            detected_lang = self._detect_language_from_text(result['extracted_text'])
            
            # Translate if not English
            if detected_lang != 'eng':
                result['original_language'] = self.LANGUAGE_CODES.get(detected_lang, detected_lang)
                result['original_text'] = result['extracted_text']
                
                translated_text = self._translate_to_english(result['extracted_text'])
                result['extracted_text'] = translated_text
                result['translated'] = True
            else:
                result['original_language'] = 'English'
                result['translated'] = False
            
            result['detected_language'] = self.LANGUAGE_CODES.get(detected_lang, detected_lang)
            
            return result
            
        except Exception as e:
            raise Exception(f"Multilingual PDF processing failed: {str(e)}")
    
    def _detect_language_from_image(self, image_path: str) -> str:
        """
        Detect language from image using OCR
        
        Args:
            image_path: Path to image file
            
        Returns:
            Language code (e.g., 'eng', 'fra', 'deu')
        """
        try:
            # Try all available languages
            preprocessed = self._preprocess_image(image_path)
            
            best_lang = 'eng'
            best_confidence = 0
            
            # Test common languages
            test_langs = ['eng', 'fra', 'deu', 'spa', 'ita', 'por', 'rus', 'jpn', 'kor', 'zho']
            
            for lang in test_langs:
                try:
                    config = f'--oem 3 --psm 6 -l {lang}'
                    text = pytesseract.image_to_string(preprocessed, config=config)
                    
                    if text.strip():
                        # Calculate confidence for this language
                        confidence = self._calculate_language_confidence(text, lang)
                        
                        if confidence > best_confidence:
                            best_confidence = confidence
                            best_lang = lang
                except:
                    continue
            
            self.detected_language = best_lang
            return best_lang
            
        except Exception as e:
            print(f"Language detection from image failed: {e}")
            return 'eng'  # Default to English
    
    def _detect_language_from_text(self, text: str) -> str:
        """
        Detect language from text
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code
        """
        try:
            if LANGDETECT_AVAILABLE:
                detected = langdetect.detect(text)
                # Convert langdetect codes to Tesseract codes
                lang_mapping = {
                    'en': 'eng', 'fr': 'fra', 'de': 'deu', 'es': 'spa',
                    'it': 'ita', 'pt': 'por', 'ru': 'rus', 'ja': 'jpn',
                    'ko': 'kor', 'zh-cn': 'zho', 'zh-tw': 'zho', 'ar': 'ara',
                    'hi': 'hin', 'bn': 'ben', 'nl': 'nld', 'sv': 'swe',
                    'pl': 'pol', 'tr': 'tur', 'el': 'gre', 'he': 'heb',
                    'th': 'tha'
                }
                return lang_mapping.get(detected, 'eng')
            
            # Fallback: use TextBlob if available
            if TEXTBLOB_AVAILABLE:
                blob = TextBlob(text)
                detected = blob.detect_language()
                lang_mapping = {
                    'en': 'eng', 'fr': 'fra', 'de': 'deu', 'es': 'spa',
                    'it': 'ita', 'pt': 'por', 'ru': 'rus', 'ja': 'jpn',
                    'ko': 'kor', 'zh': 'zho', 'ar': 'ara', 'hi': 'hin',
                    'bn': 'ben', 'nl': 'nld', 'sv': 'swe', 'pl': 'pol',
                    'tr': 'tur', 'el': 'gre', 'he': 'heb', 'th': 'tha'
                }
                return lang_mapping.get(detected, 'eng')
            
            return 'eng'  # Default to English
            
        except Exception as e:
            print(f"Language detection from text failed: {e}")
            return 'eng'
    
    def _calculate_language_confidence(self, text: str, lang: str) -> float:
        """
        Calculate confidence score for detected language
        
        Args:
            text: Extracted text
            lang: Language code
            
        Returns:
            Confidence score (0-1)
        """
        if not text.strip():
            return 0
        
        # Simple heuristic: longer text = higher confidence
        text_length = len(text.strip())
        word_count = len(text.split())
        
        # Normalize by typical document size
        confidence = min(word_count / 100, 1.0)
        
        return confidence
    
    def _process_with_language(self, image_path: str, lang: str) -> Dict[str, Any]:
        """
        Process image with specific language
        
        Args:
            image_path: Path to image file
            lang: Language code
            
        Returns:
            OCR results
        """
        # Temporarily set language
        original_lang = self.lang
        self.lang = lang
        self.config = f'--oem 3 --psm 6 -l {lang}'
        
        try:
            result = self.process_image(image_path)
            return result
        finally:
            # Restore original language
            self.lang = original_lang
            self.config = f'--oem 3 --psm 6 -l {original_lang}'
    
    def _translate_to_english(self, text: str) -> str:
        """
        Translate text to English
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text in English
        """
        if not text.strip():
            return text
        
        try:
            if self.translation_service == 'google' and GOOGLE_TRANSLATE_AVAILABLE:
                return self._translate_google(text)
            elif DEEP_TRANSLATOR_AVAILABLE:
                return self._translate_deep_translator(text)
            elif TEXTBLOB_AVAILABLE:
                return self._translate_textblob(text)
            else:
                print("Warning: No translation service available. Returning original text.")
                return text
                
        except Exception as e:
            print(f"Translation failed: {e}. Returning original text.")
            return text
    
    def _translate_textblob(self, text: str) -> str:
        """
        Translate using TextBlob
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text
        """
        try:
            # Use TextBlob for translation
            blob = TextBlob(text)
            translated = blob.translate(from_lang='auto', to_lang='en')
            result = str(translated)
            
            # If translation returned empty or same as original, return original
            if not result or result.strip() == text.strip():
                print("Translation returned empty or same as original, using original text")
                return text
            
            return result
            
        except Exception as e:
            print(f"TextBlob translation failed: {e}")
            # Return original text if translation fails
            return text
    
    def _translate_google(self, text: str) -> str:
        """
        Translate using Google Cloud Translation
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text
        """
        try:
            # This requires Google Cloud credentials
            # Implementation depends on your setup
            client = translate_v2.Client()
            result = client.translate_text(text, target_language='en')
            return result['translatedText']
        except Exception as e:
            print(f"Google translation failed: {e}")
            return text
    
    def _translate_deep_translator(self, text: str) -> str:
        """
        Translate using Deep Translator (GoogleTranslator)
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text
        """
        try:
            from deep_translator import GoogleTranslator
            
            # Split text into chunks (Google Translator has limits)
            max_chars = 4500
            chunks = []
            current_chunk = ""
            
            for line in text.split('\n'):
                if len(current_chunk) + len(line) + 1 > max_chars:
                    if current_chunk:
                        chunks.append(current_chunk)
                    current_chunk = line
                else:
                    current_chunk += '\n' + line if current_chunk else line
            
            if current_chunk:
                chunks.append(current_chunk)
            
            # Translate each chunk
            translated_chunks = []
            for chunk in chunks:
                try:
                    translator = GoogleTranslator(source_language='auto', target_language='en')
                    translated = translator.translate(chunk)
                    translated_chunks.append(translated)
                except Exception as e:
                    print(f"Deep translator chunk failed: {e}")
                    translated_chunks.append(chunk)
            
            return '\n'.join(translated_chunks)
            
        except Exception as e:
            print(f"Deep translator translation failed: {e}")
            return text
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get list of supported languages
        
        Returns:
            Dictionary of language codes and names
        """
        return self.LANGUAGE_CODES.copy()
