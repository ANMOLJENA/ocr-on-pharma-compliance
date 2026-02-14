from langdetect import detect, detect_langs, LangDetectException
from interfaces import LanguageDetectionServiceInterface
from typing import Dict, Any

# Mapping of language codes to language names
LANGUAGE_NAMES = {
    'af': 'Afrikaans',
    'ar': 'Arabic',
    'bg': 'Bulgarian',
    'bn': 'Bengali',
    'ca': 'Catalan',
    'cs': 'Czech',
    'cy': 'Welsh',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'es': 'Spanish',
    'et': 'Estonian',
    'fa': 'Persian',
    'fi': 'Finnish',
    'fr': 'French',
    'gu': 'Gujarati',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hr': 'Croatian',
    'hu': 'Hungarian',
    'id': 'Indonesian',
    'it': 'Italian',
    'ja': 'Japanese',
    'kn': 'Kannada',
    'ko': 'Korean',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'mk': 'Macedonian',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'ne': 'Nepali',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'pa': 'Punjabi',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'sq': 'Albanian',
    'sv': 'Swedish',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tl': 'Tagalog',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
    'zh': 'Chinese',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
}


class LanguageDetectionService(LanguageDetectionServiceInterface):
    """
    Language detection service using langdetect library.
    
    Detects the language of given text and returns language code, name, and confidence.
    """
    
    @staticmethod
    def detect_language(text: str) -> Dict[str, Any]:
        """
        Detect the language of the given text.
        
        Args:
            text: Text to detect language for
            
        Returns:
            Dictionary with 'success', 'language_code', 'language_name', 'confidence', and 'error' keys
        """
        try:
            if not text or text.strip() == '':
                return {
                    'success': False,
                    'language_code': None,
                    'language_name': None,
                    'confidence': 0.0,
                    'error': 'Empty text provided'
                }
            
            # Get all language probabilities
            lang_probs = detect_langs(text)
            
            if not lang_probs:
                return {
                    'success': False,
                    'language_code': None,
                    'language_name': None,
                    'confidence': 0.0,
                    'error': 'Could not detect language'
                }
            
            # Get the most probable language
            best_match = lang_probs[0]
            language_code = best_match.lang
            confidence = best_match.prob
            
            # Get language name from mapping
            language_name = LANGUAGE_NAMES.get(language_code, language_code)
            
            return {
                'success': True,
                'language_code': language_code,
                'language_name': language_name,
                'confidence': confidence,
                'error': None
            }
        except LangDetectException as e:
            return {
                'success': False,
                'language_code': None,
                'language_name': None,
                'confidence': 0.0,
                'error': f'Language detection failed: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'language_code': None,
                'language_name': None,
                'confidence': 0.0,
                'error': f'Language detection error: {str(e)}'
            }
    
    @staticmethod
    def detect_language_from_pages(texts: list) -> Dict[str, Any]:
        """
        Detect the language from multiple text segments (e.g., PDF pages).
        Uses the combined text from all pages for more accurate detection.
        
        Args:
            texts: List of text segments to detect language for
            
        Returns:
            Dictionary with 'success', 'language_code', 'language_name', 'confidence', and 'error' keys
        """
        try:
            if not texts or all(not t or t.strip() == '' for t in texts):
                return {
                    'success': False,
                    'language_code': None,
                    'language_name': None,
                    'confidence': 0.0,
                    'error': 'No text provided'
                }
            
            # Combine all non-empty texts
            combined_text = ' '.join([t for t in texts if t and t.strip() != ''])
            
            if not combined_text or combined_text.strip() == '':
                return {
                    'success': False,
                    'language_code': None,
                    'language_name': None,
                    'confidence': 0.0,
                    'error': 'No valid text to detect'
                }
            
            # Use the single text detection on combined text
            return LanguageDetectionService.detect_language(combined_text)
        except Exception as e:
            return {
                'success': False,
                'language_code': None,
                'language_name': None,
                'confidence': 0.0,
                'error': f'Multi-page language detection failed: {str(e)}'
            }
