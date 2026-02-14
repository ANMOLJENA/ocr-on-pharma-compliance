# Design Document: Multilingual Translation Integration

## Overview

This design document specifies the architecture and implementation approach for integrating an improved multilingual translation system into the OCR Compliance System. The system will replace TextBlob with MyMemory API, add language detection capabilities, and expand language support to 40+ languages including Indian languages and Estonian.

The design follows a layered architecture pattern consistent with the existing system:
- **Service Layer**: Translation and Language Detection services handle business logic
- **API Layer**: Updated OCR routes expose language functionality
- **Data Layer**: Database schema extended to store language metadata
- **Frontend Layer**: UI components updated to display language information

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  - Language selector dropdown                               │
│  - Language detection display                               │
│  - Original/translated text viewer                          │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────────┐
│                  API Layer (Flask)                           │
│  - /ocr/multilingual/upload                                 │
│  - /ocr/multilingual/languages                              │
│  - /ocr/multilingual/detect-language                        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Service Layer (Python)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ TranslationService                                   │   │
│  │ - translate_to_english(text, source_lang)           │   │
│  │ - _smart_chunk_text(text)                           │   │
│  │ - _translate_chunk(chunk, source_lang)              │   │
│  │ - translate_pages(texts, source_lang)               │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ LanguageDetectionService                             │   │
│  │ - detect_language(text)                              │   │
│  │ - detect_language_from_pages(texts)                  │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ MultilingualOCRService (Updated)                     │   │
│  │ - process_image_multilingual(image_path)             │   │
│  │ - process_pdf_multilingual(pdf_path)                 │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│              External Services                               │
│  - MyMemory Translation API                                 │
│  - langdetect Library                                       │
│  - Tesseract OCR                                            │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Document Upload**: User uploads a document (image or PDF)
2. **Language Detection**: System detects language using langdetect
3. **OCR Processing**: Tesseract extracts text in detected language
4. **Translation**: If not English, text is translated using MyMemory API with smart chunking
5. **Storage**: Original and translated text stored in database with language metadata
6. **Response**: API returns detected language, translation status, and both text versions

## Components and Interfaces

### 1. TranslationService

**Purpose**: Handles translation of text to English using MyMemory API with smart chunking.

**Key Methods**:

```python
class TranslationService:
    # Constants
    MYMEMORY_API = "https://api.mymemory.translated.net/get"
    CHUNK_SIZE = 450  # Respects MyMemory's 500 char limit
    CHUNK_OVERLAP = 50
    
    LANGUAGE_CODES = {
        # European languages
        'en': 'en', 'fr': 'fr', 'de': 'de', 'es': 'es',
        'ar': 'ar', 'pt': 'pt', 'it': 'it', 'nl': 'nl', 'ru': 'ru',
        # Asian languages
        'zh': 'zh', 'ja': 'ja', 'ko': 'ko',
        # Indian languages
        'hi': 'hi', 'ta': 'ta', 'te': 'te', 'kn': 'kn',
        'ml': 'ml', 'gu': 'gu', 'mr': 'mr', 'bn': 'bn',
        'pa': 'pa', 'ur': 'ur',
        # Additional languages
        'et': 'et',  # Estonian
    }
    
    @staticmethod
    def translate_to_english(text: str, source_language: str) -> dict
    @staticmethod
    def translate_pages(texts: list, source_language: str) -> dict
    @staticmethod
    def _smart_chunk_text(text: str, chunk_size: int, overlap: int) -> list
    @staticmethod
    def _translate_chunk(text: str, source_language: str) -> dict
```

**Behavior**:
- Splits text on sentence boundaries to maintain context
- Respects MyMemory's 500-character limit with 50-character overlap
- Returns structured responses with success/error information
- Handles timeouts and connection errors gracefully
- Returns original text if already English

### 2. LanguageDetectionService

**Purpose**: Detects the language of text using langdetect library.

**Key Methods**:

```python
class LanguageDetectionService:
    LANGUAGE_NAMES = {
        'en': 'English', 'fr': 'French', 'de': 'German',
        'hi': 'Hindi', 'ta': 'Tamil', 'te': 'Telugu',
        'et': 'Estonian', ...
    }
    
    @staticmethod
    def detect_language(text: str) -> dict
    @staticmethod
    def detect_language_from_pages(texts: list) -> dict
```

**Behavior**:
- Uses langdetect for language detection
- Returns language code, name, and confidence score
- Combines multiple text segments for more accurate detection
- Maps language codes to human-readable names
- Handles empty text and detection failures gracefully

### 3. MultilingualOCRService (Updated)

**Purpose**: Orchestrates OCR processing with automatic language detection and translation.

**Key Updates**:
- Integrates TranslationService and LanguageDetectionService
- Stores language metadata in OCR results
- Maintains backward compatibility with existing methods
- Returns both original and translated text

**Key Methods**:

```python
class MultilingualOCRService(TesseractOCRService):
    def process_image_multilingual(self, image_path: str) -> dict
    def process_pdf_multilingual(self, pdf_path: str) -> dict
    def get_supported_languages(self) -> dict
```

### 4. Updated OCR Routes

**New Endpoints**:

```python
# Get supported languages
GET /api/ocr/multilingual/languages
Response: {
    'success': True,
    'supported_languages': {
        'en': 'English',
        'hi': 'Hindi',
        'ta': 'Tamil',
        ...
    }
}

# Detect language from file
POST /api/ocr/multilingual/detect-language
Request: multipart/form-data with 'file'
Response: {
    'success': True,
    'detected_language_code': 'hi',
    'detected_language': 'Hindi'
}

# Upload and process with language support
POST /api/ocr/multilingual/upload
Response: {
    'success': True,
    'document_id': 1,
    'ocr_result_id': 1,
    'detected_language': 'Hindi',
    'original_language': 'Hindi',
    'translated': True,
    'original_text': '...',
    'translated_text': '...',
    'data': {...}
}
```

### 5. Database Schema Updates

**OCRResult Model Extension**:

```python
class OCRResult(db.Model):
    # Existing fields...
    
    # New fields for language support
    metadata = db.Column(db.JSON, nullable=True)
    # Stores: {
    #   'detected_language': 'Hindi',
    #   'original_language': 'Hindi',
    #   'translated': True,
    #   'original_text': '...',
    #   'translated_text': '...'
    # }
```

### 6. Frontend Components (Updated)

**New/Updated Components**:

```typescript
// Language selector dropdown
<LanguageSelector 
  supportedLanguages={languages}
  onSelect={handleLanguageSelect}
/>

// Language detection display
<LanguageDetectionBadge 
  detectedLanguage={language}
  confidence={confidence}
/>

// Original/translated text viewer
<BilingualTextViewer
  originalText={originalText}
  translatedText={translatedText}
  originalLanguage={originalLanguage}
/>
```

## Data Models

### Language Support Mapping

```python
SUPPORTED_LANGUAGES = {
    # European Languages (14)
    'en': 'English',
    'fr': 'French',
    'de': 'German',
    'es': 'Spanish',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'pl': 'Polish',
    'tr': 'Turkish',
    'el': 'Greek',
    'he': 'Hebrew',
    'th': 'Thai',
    
    # Asian Languages (3)
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    
    # Indian Languages (10)
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'gu': 'Gujarati',
    'mr': 'Marathi',
    'bn': 'Bengali',
    'pa': 'Punjabi',
    'ur': 'Urdu',
    
    # Additional Languages (1)
    'et': 'Estonian',
}
```

### Translation Response Structure

```python
{
    'success': bool,
    'translated_text': str,
    'error': Optional[str],
    'source_language': str,
    'target_language': str,
    'chunks_count': int,
    'processing_time_ms': float
}
```

### Language Detection Response Structure

```python
{
    'success': bool,
    'language_code': str,
    'language_name': str,
    'confidence': float,  # 0.0 to 1.0
    'error': Optional[str]
}
```

## Error Handling

### Translation Errors

1. **Empty Text**: Return error "Empty text provided"
2. **Unsupported Language**: Return error "Unsupported language: {lang}"
3. **API Timeout**: Return error "Translation request timeout"
4. **Connection Error**: Return error "Cannot connect to translation service"
5. **Invalid Response**: Return error "Translation returned empty result"
6. **Fallback**: Return original text if translation fails

### Language Detection Errors

1. **Empty Text**: Return error "Empty text provided"
2. **Detection Failed**: Return error "Could not detect language"
3. **Invalid Input**: Return error "Language detection error: {details}"

### API Errors

1. **File Not Provided**: Return 400 "No file provided"
2. **Invalid File Type**: Return 400 "Invalid file type"
3. **Processing Failed**: Return 500 with error details
4. **Database Error**: Return 500 with error details

## Testing Strategy

### Unit Tests

**TranslationService Tests**:
- Test translation of text in each supported language
- Test smart chunking with various text lengths
- Test chunk overlap preservation
- Test error handling for API failures
- Test timeout handling
- Test empty text handling
- Test already-English text

**LanguageDetectionService Tests**:
- Test language detection for each supported language
- Test confidence score calculation
- Test multi-page language detection
- Test empty text handling
- Test language name mapping

**MultilingualOCRService Tests**:
- Test image processing with language detection
- Test PDF processing with language detection
- Test translation integration
- Test metadata storage
- Test backward compatibility

**API Route Tests**:
- Test /multilingual/languages endpoint
- Test /multilingual/detect-language endpoint
- Test /multilingual/upload endpoint
- Test /multilingual/process endpoint
- Test error responses

### Property-Based Tests

Property-based tests will be defined in the Correctness Properties section below.

### Integration Tests

- Test end-to-end document upload with language detection and translation
- Test compliance checks with translated text
- Test error detection with translated text
- Test analytics with multilingual documents
- Test backward compatibility with existing workflows

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property-Based Testing Overview

Property-based testing validates software correctness by testing universal properties across many generated inputs. Each property is a formal specification that should hold for all valid inputs.

**Core Principles**:
1. **Universal Quantification**: Every property must contain an explicit "for all" statement
2. **Requirements Traceability**: Each property must reference the requirements it validates
3. **Executable Specifications**: Properties must be implementable as automated tests
4. **Comprehensive Coverage**: Properties should cover all testable acceptance criteria

### Correctness Properties

**Property 1: MyMemory API Configuration**

*For any* instance of TranslationService, the service should be configured to use the MyMemory API endpoint (https://api.mymemory.translated.net/get) instead of TextBlob.

**Validates: Requirements 1.1, 1.2**

**Property 2: Successful Translation Response Structure**

*For any* successful translation operation, the response should contain 'success': True, 'translated_text' with non-empty string, and 'error': None.

**Validates: Requirements 1.3, 5.2, 5.3**

**Property 3: Error Response Structure**

*For any* failed translation or language detection operation, the response should contain 'success': False, 'error' with descriptive message, and appropriate null/empty values for data fields.

**Validates: Requirements 1.4, 1.5, 1.6, 3.4, 8.3, 8.5**

**Property 4: Smart Chunking Preserves Content**

*For any* text that is split into chunks using smart sentence-based chunking, the concatenation of all chunks (with overlap removed) should equal the original text.

**Validates: Requirements 2.1, 2.2, 2.3, 2.5**

**Property 5: Chunk Size Respects Limits**

*For any* text chunk created by the smart chunking algorithm, the chunk size should not exceed 500 characters (MyMemory API limit).

**Validates: Requirements 2.1**

**Property 6: Overlap Between Chunks**

*For any* two consecutive chunks created by smart chunking, the end of the first chunk should overlap with the beginning of the second chunk by approximately 50 characters.

**Validates: Requirements 2.3**

**Property 7: Empty Text Handling**

*For any* empty string or whitespace-only string, both translation and language detection services should return an error response without crashing.

**Validates: Requirements 2.6, 3.3**

**Property 8: Language Detection Returns Valid Code**

*For any* text in a supported language, the language detection service should return a language_code that exists in the SUPPORTED_LANGUAGES mapping.

**Validates: Requirements 3.1, 3.2, 3.6, 4.7**

**Property 9: Language Detection Confidence Range**

*For any* text, the confidence score returned by language detection should be a number between 0.0 and 1.0 (inclusive).

**Validates: Requirements 3.2**

**Property 10: Multi-Page Language Detection Consistency**

*For any* multi-page document where all pages are in the same language, the language detection service should return the same language code regardless of which pages are combined.

**Validates: Requirements 3.5**

**Property 11: Supported Languages Completeness**

*For any* language code in the SUPPORTED_LANGUAGES mapping, the translation service should be able to translate text from that language to English without returning an unsupported language error.

**Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5, 4.6**

**Property 12: API Endpoint Response Structure**

*For any* successful API call to /ocr/multilingual/upload or /ocr/multilingual/process, the response should contain 'success': True, 'detected_language', 'original_language', 'translated' (boolean), and 'data' fields.

**Validates: Requirements 5.1, 5.2, 5.3, 5.5**

**Property 13: Supported Languages Endpoint Completeness**

*For any* call to /ocr/multilingual/languages endpoint, the response should contain all 40+ supported languages with both language codes and human-readable names.

**Validates: Requirements 5.1, 4.1, 4.2, 4.3, 4.4**

**Property 14: Backward Compatibility - Existing Endpoints**

*For any* document processed using existing OCR endpoints (without language parameters), the system should return results with the same structure and content as before the integration.

**Validates: Requirements 7.1, 7.2, 7.6**

**Property 15: Backward Compatibility - Compliance Checks**

*For any* OCR result (translated or not), compliance checks should execute successfully and return valid compliance scores.

**Validates: Requirements 7.3, 7.4, 7.5**

**Property 16: Graceful Degradation on Translation Failure**

*For any* translation failure (API unavailable, timeout, unsupported language), the system should return the original extracted text instead of failing the entire OCR process.

**Validates: Requirements 8.1, 8.2, 8.4**

**Property 17: Error Logging on Failures**

*For any* error that occurs during translation or language detection, the system should log the error with sufficient detail (error type, message, context) for debugging.

**Validates: Requirements 8.2, 8.6**

**Property 18: English Text Pass-Through**

*For any* text already in English, the translation service should return the original text without attempting translation to MyMemory API.

**Validates: Requirements 1.1**

**Property 19: Language Code Mapping Consistency**

*For any* language name in the LANGUAGE_NAMES mapping, the corresponding language code should be a valid ISO 639-1 code that MyMemory API recognizes.

**Validates: Requirements 4.5, 3.6**

**Property 20: Database Storage of Multilingual Data**

*For any* translated document, both the original text and translated text should be stored in the database metadata field and retrievable without data loss.

**Validates: Requirements 5.5**

## Implementation Notes

### Dependencies to Add

```
requests==2.32.5  # Already in requirements.txt
langdetect==1.0.9  # Already in requirements.txt
```

No new dependencies needed - both are already in the project.

### Configuration

**Environment Variables** (in `.env`):
```
# Translation service configuration
TRANSLATION_CHUNK_SIZE=450
TRANSLATION_CHUNK_OVERLAP=50
TRANSLATION_TIMEOUT=30
MYMEMORY_API_URL=https://api.mymemory.translated.net/get
```

### Performance Considerations

1. **Chunking Overhead**: Smart chunking adds minimal overhead (sentence boundary detection)
2. **API Calls**: Multiple chunks = multiple API calls, but overlap reduces redundancy
3. **Caching**: Consider caching translations for frequently translated documents
4. **Concurrency**: MyMemory API handles concurrent requests well
5. **Database**: JSON metadata field allows flexible storage without schema changes

### Security Considerations

1. **API Rate Limiting**: MyMemory API has rate limits; implement request queuing if needed
2. **Text Privacy**: Translations are sent to external API; ensure compliance with data policies
3. **Input Validation**: Validate file types and sizes before processing
4. **Error Messages**: Don't expose internal API details in error messages

## Migration Path

1. **Phase 1**: Deploy TranslationService and LanguageDetectionService alongside existing TextBlob
2. **Phase 2**: Update MultilingualOCRService to use new services
3. **Phase 3**: Update API routes to expose language information
4. **Phase 4**: Update frontend to display language information
5. **Phase 5**: Monitor and validate backward compatibility
6. **Phase 6**: Deprecate TextBlob (keep as fallback initially)

## Future Enhancements

1. **Translation Caching**: Cache translations to reduce API calls
2. **Batch Processing**: Support batch translation of multiple documents
3. **Custom Language Models**: Support for domain-specific pharmaceutical terminology
4. **Translation Quality Metrics**: Track translation quality and accuracy
5. **Offline Translation**: Support for offline translation using local models
6. **Language-Specific OCR**: Use language-specific Tesseract models for better accuracy
