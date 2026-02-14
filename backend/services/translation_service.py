import requests
import time
import hashlib
from interfaces import TranslationServiceInterface

class TranslationService(TranslationServiceInterface):
    
    # Use MyMemory Translation API (free, no API key needed)
    MYMEMORY_API = "https://api.mymemory.translated.net/get"
    
    # Chunking parameters (matching the logic from your code)
    CHUNK_SIZE = 200  # Reduced from 450 to be more conservative and avoid rate limiting
    CHUNK_OVERLAP = 20  # Reduced from 50 to match smaller chunks
    
    # Retry configuration for rate limiting
    MAX_RETRIES = 2
    RETRY_DELAY = 1  # seconds, will exponentially increase
    
    # Simple translation cache to avoid repeated API calls
    _translation_cache = {}
    
    # Language code mappings (including Indian languages)
    LANGUAGE_CODES = {
        # European languages (14)
        'en': 'en',  # English
        'fr': 'fr',  # French
        'de': 'de',  # German
        'es': 'es',  # Spanish
        'it': 'it',  # Italian
        'pt': 'pt',  # Portuguese
        'ru': 'ru',  # Russian
        'nl': 'nl',  # Dutch
        'sv': 'sv',  # Swedish
        'pl': 'pl',  # Polish
        'tr': 'tr',  # Turkish
        'el': 'el',  # Greek
        'he': 'he',  # Hebrew
        'th': 'th',  # Thai
        
        # Asian languages (3)
        'zh': 'zh',  # Chinese
        'ja': 'ja',  # Japanese
        'ko': 'ko',  # Korean
        
        # Indian languages (10)
        'hi': 'hi',  # Hindi
        'ta': 'ta',  # Tamil
        'te': 'te',  # Telugu
        'kn': 'kn',  # Kannada
        'ml': 'ml',  # Malayalam
        'gu': 'gu',  # Gujarati
        'mr': 'mr',  # Marathi
        'bn': 'bn',  # Bengali
        'pa': 'pa',  # Punjabi
        'ur': 'ur',  # Urdu
        
        # Additional languages (1)
        'et': 'et',  # Estonian
        
        # Note: Arabic (ar) was in the original but not in requirements
        # Keeping it for backward compatibility
        'ar': 'ar',  # Arabic
    }
    
    @staticmethod
    def _recursive_split(text: str, separators: list, chunk_size: int, overlap: int) -> list:
        """
        Recursively split text using a list of separators, trying each in order.
        Similar to RecursiveCharacterTextSplitter from langchain.
        
        Args:
            text: Text to split
            separators: List of separators to try in order
            chunk_size: Target chunk size
            overlap: Overlap between chunks (not used in this implementation)
            
        Returns:
            List of text chunks
        """
        good_splits = []
        separator = separators[-1]
        
        # Try each separator in order
        for _s in separators:
            if _s == "":
                separator = _s
                break
            if _s in text:
                separator = _s
                break
        
        # Split by the separator
        if separator:
            splits = text.split(separator)
        else:
            splits = list(text)
        
        # Filter out empty splits and rejoin with separator
        good_splits = []
        for s in splits:
            if s.strip():
                good_splits.append(s)
        
        # Now merge splits that are too small and split those that are too large
        merged_text = []
        
        for s in good_splits:
            if len(s) < chunk_size:
                merged_text.append(s)
            else:
                # This split is too large, need to split it further
                if merged_text:
                    # First, merge what we have
                    merged_string = separator.join(merged_text)
                    if len(merged_string) > 0:
                        yield merged_string
                    merged_text = []
                
                # Now recursively split the large chunk
                if separator and separator != "":
                    # Try next separator
                    next_separators = separators[separators.index(separator) + 1:]
                    if next_separators:
                        for sub_chunk in TranslationService._recursive_split(s, next_separators, chunk_size, overlap):
                            yield sub_chunk
                    else:
                        # No more separators, just yield as is
                        yield s
                else:
                    yield s
        
        # Merge remaining
        if merged_text:
            merged_string = separator.join(merged_text)
            if len(merged_string) > 0:
                yield merged_string
    
    @staticmethod
    def _smart_chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list:
        """
        Split text into chunks intelligently using recursive splitting.
        Tries to split on sentence boundaries first, then words, then characters.
        
        Args:
            text: Text to chunk
            chunk_size: Target size for each chunk
            overlap: Number of characters to overlap between chunks (NOT USED - kept for compatibility)
            
        Returns:
            List of text chunks
        """
        if not text or text.strip() == '':
            return []
        
        # Use recursive splitting with multiple separators
        # Try in order: sentences, newlines, spaces, then characters
        separators = [
            "\n\n",      # Paragraph breaks
            "\n",        # Line breaks
            ". ",        # Sentence ends
            "! ",        # Exclamation ends
            "? ",        # Question ends
            " ",         # Word boundaries
            ""           # Character level (last resort)
        ]
        
        chunks = list(TranslationService._recursive_split(text, separators, chunk_size, 0))
        
        # Don't add overlap - it causes duplication in the final output
        return chunks
    
    @staticmethod
    def _translate_chunk(text: str, source_language: str) -> dict:
        """
        Translate a single chunk of text using MyMemory API with retry logic and caching.
        Falls back to returning original text if API is unavailable.
        
        Args:
            text: Text chunk to translate
            source_language: Source language code
            
        Returns:
            Dictionary with translated text or error
        """
        try:
            if not text or text.strip() == '':
                return {
                    'success': True,
                    'translated_text': '',
                    'error': None
                }
            
            source_lang = source_language.lower()
            
            # Check cache first
            cache_key = hashlib.md5(f"{text}|{source_lang}".encode()).hexdigest()
            if cache_key in TranslationService._translation_cache:
                print(f"[TRANS] Cache hit for chunk")
                return TranslationService._translation_cache[cache_key]
            
            # Prepare request
            params = {
                'q': text,
                'langpair': f'{source_lang}|en'
            }
            
            # Retry logic for rate limiting
            last_error = None
            for attempt in range(TranslationService.MAX_RETRIES):
                try:
                    # Make request to MyMemory API
                    response = requests.get(
                        TranslationService.MYMEMORY_API,
                        params=params,
                        timeout=10
                    )
                    
                    # Handle rate limiting (429) with retry
                    if response.status_code == 429:
                        if attempt < TranslationService.MAX_RETRIES - 1:
                            wait_time = TranslationService.RETRY_DELAY * (2 ** attempt)
                            print(f"[TRANS] Rate limited (429). Retrying in {wait_time}s (attempt {attempt + 1}/{TranslationService.MAX_RETRIES})")
                            time.sleep(wait_time)
                            continue
                        else:
                            last_error = 'Translation service rate limited (too many requests)'
                            break
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result.get('responseStatus') == 200:
                            translated_text = result.get('responseData', {}).get('translatedText', '')
                            
                            if translated_text:
                                success_result = {
                                    'success': True,
                                    'translated_text': translated_text,
                                    'error': None
                                }
                                # Cache successful translation
                                TranslationService._translation_cache[cache_key] = success_result
                                return success_result
                            else:
                                last_error = 'Translation returned empty result'
                                break
                        else:
                            last_error = result.get('responseDetails', 'Unknown error')
                            break
                    else:
                        last_error = f'HTTP error: {response.status_code}'
                        break
                        
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                    if attempt < TranslationService.MAX_RETRIES - 1:
                        wait_time = TranslationService.RETRY_DELAY * (2 ** attempt)
                        print(f"[TRANS] Connection error. Retrying in {wait_time}s (attempt {attempt + 1}/{TranslationService.MAX_RETRIES})")
                        time.sleep(wait_time)
                        continue
                    else:
                        last_error = f'Connection failed: {str(e)}'
                        break
            
            # Fallback: return original text if API fails
            print(f"[TRANS] API failed ({last_error}). Using fallback: returning original text")
            fallback_result = {
                'success': True,
                'translated_text': text,  # Return original text as fallback
                'error': f'API unavailable, using original text: {last_error}'
            }
            # Cache fallback result
            TranslationService._translation_cache[cache_key] = fallback_result
            return fallback_result
            
        except Exception as e:
            print(f"[TRANS] Unexpected error: {str(e)}")
            return {
                'success': False,
                'error': f'Translation failed: {str(e)}',
                'translated_text': ''
            }
    
    @staticmethod
    def translate_to_english(text: str, source_language: str) -> dict:
        """
        Translate text to English using MyMemory Translation API with smart chunking.
        Intelligently splits text on sentence boundaries to maintain context.
        
        Args:
            text: Text to translate
            source_language: Source language code (e.g., 'es', 'fr')
            
        Returns:
            Dictionary with translated text or error
        """
        try:
            # Check for empty text first
            if not text or text.strip() == '':
                return {
                    'success': False,
                    'error': 'Empty text provided',
                    'translated_text': ''
                }
            
            # If already English, return original text
            if source_language.lower() == 'en':
                return {
                    'success': True,
                    'translated_text': text,
                    'error': None
                }
            
            source_lang = source_language.lower()
            
            print(f"[TRANS] Translating from {source_lang} to English using MyMemory API")
            print(f"[TRANS] Text length: {len(text)} characters")
            
            # Split text into chunks using smart sentence-based chunking
            chunks = TranslationService._smart_chunk_text(text)
            print(f"[TRANS] Split into {len(chunks)} chunk(s) using smart sentence-based chunking")
            
            translated_chunks = []
            
            for i, chunk in enumerate(chunks, 1):
                chunk_size = len(chunk)
                print(f"[TRANS] Translating chunk {i}/{len(chunks)} ({chunk_size} characters)...")
                
                result = TranslationService._translate_chunk(chunk, source_lang)
                
                if not result['success']:
                    print(f"[TRANS] Chunk {i} translation failed: {result['error']}")
                    return result
                
                translated_chunks.append(result['translated_text'])
            
            # Combine translated chunks
            # Remove extra spaces from overlapping regions
            translated_text = ' '.join(translated_chunks)
            # Clean up multiple spaces
            translated_text = ' '.join(translated_text.split())
            
            print(f"[TRANS] Translation successful: {len(translated_text)} characters")
            return {
                'success': True,
                'translated_text': translated_text,
                'error': None
            }
            
        except Exception as e:
            print(f"[TRANS] Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f'Translation failed: {str(e)}',
                'translated_text': ''
            }

    @staticmethod
    def translate_pages(texts: list, source_language: str) -> dict:
        """
        Translate multiple text segments (e.g., PDF pages).
        
        Args:
            texts: List of text segments to translate
            source_language: Source language code
            
        Returns:
            Dictionary with translated texts
        """
        try:
            translated_texts = []
            
            for text in texts:
                result = TranslationService.translate_to_english(text, source_language)
                if result['success']:
                    translated_texts.append(result['translated_text'])
                else:
                    translated_texts.append('')
            
            return {
                'success': True,
                'translated_texts': translated_texts,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Multi-page translation failed: {str(e)}',
                'translated_texts': []
            }
