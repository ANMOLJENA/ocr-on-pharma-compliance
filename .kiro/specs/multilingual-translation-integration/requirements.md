# Requirements Document: Multilingual Translation Integration

## Introduction

This document specifies the requirements for integrating an improved multilingual translation system into the OCR Compliance System. The current system uses TextBlob for translation, which has limited reliability and language support. The integration will replace TextBlob with the MyMemory API approach from the "ocr lang" project, add language detection capabilities, and expand language support to include Indian languages and Estonian.

## Glossary

- **MyMemory API**: A free translation API service that provides reliable translation without requiring API keys
- **Language Detection**: The process of automatically identifying the language of a given text
- **Smart Text Chunking**: Intelligent splitting of text on sentence boundaries to maintain translation context
- **Language Code**: ISO 639-1 or ISO 639-3 standard codes representing languages (e.g., 'en', 'hi', 'et')
- **Translation Service**: Backend service responsible for translating text between languages
- **Language Detection Service**: Backend service responsible for identifying the language of text
- **OCR Result**: The extracted text and metadata from optical character recognition processing
- **Backward Compatibility**: The ability of the new system to work with existing OCR workflows without breaking changes
- **Indian Languages**: Hindi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Marathi, Bengali, Punjabi, Urdu
- **European Languages**: English, French, German, Spanish, Italian, Portuguese, Russian, Dutch, Swedish, Polish, Turkish, Greek, Hebrew, Thai
- **Asian Languages**: Chinese, Japanese, Korean
- **Estonian**: Baltic language (ET language code)

## Requirements

### Requirement 1: Replace TextBlob with MyMemory API

**User Story:** As a system administrator, I want to replace the unreliable TextBlob translation with MyMemory API, so that translations are more accurate and reliable.

#### Acceptance Criteria

1. WHEN the translation service is initialized, THE Translation_Service SHALL use MyMemory API instead of TextBlob
2. WHEN text is provided for translation, THE Translation_Service SHALL send requests to the MyMemory API endpoint (https://api.mymemory.translated.net/get)
3. WHEN the MyMemory API returns a successful response, THE Translation_Service SHALL extract and return the translated text
4. WHEN the MyMemory API returns an error response, THE Translation_Service SHALL return a structured error with descriptive message
5. WHEN the MyMemory API is unreachable, THE Translation_Service SHALL handle the connection error gracefully and return an error response
6. WHEN a translation request times out, THE Translation_Service SHALL return a timeout error after 30 seconds

### Requirement 2: Implement Smart Text Chunking

**User Story:** As a developer, I want smart text chunking for translations, so that long documents maintain context and translate accurately.

#### Acceptance Criteria

1. WHEN text exceeds 450 characters, THE Translation_Service SHALL split it into chunks respecting the 500-character MyMemory limit
2. WHEN splitting text, THE Translation_Service SHALL prioritize splitting on sentence boundaries (periods, exclamation marks, question marks)
3. WHEN chunks are created, THE Translation_Service SHALL maintain a 50-character overlap between consecutive chunks to preserve context
4. WHEN a single sentence exceeds the chunk size, THE Translation_Service SHALL include it as a complete chunk without further splitting
5. WHEN multiple chunks are translated, THE Translation_Service SHALL combine them intelligently, removing duplicate overlapping text
6. WHEN text is empty or contains only whitespace, THE Translation_Service SHALL return an empty result without attempting translation

### Requirement 3: Add Language Detection Service

**User Story:** As a system user, I want automatic language detection, so that the system can identify the language of documents without manual input.

#### Acceptance Criteria

1. WHEN text is provided, THE Language_Detection_Service SHALL detect the language using langdetect library
2. WHEN language detection succeeds, THE Language_Detection_Service SHALL return language code, language name, and confidence score
3. WHEN text is empty, THE Language_Detection_Service SHALL return an error indicating no text was provided
4. WHEN language detection fails, THE Language_Detection_Service SHALL return an error with descriptive message
5. WHEN multiple text segments are provided (e.g., PDF pages), THE Language_Detection_Service SHALL combine them and detect the overall language
6. WHEN language is detected, THE Language_Detection_Service SHALL map language codes to human-readable language names

### Requirement 4: Expand Language Support to 40+ Languages

**User Story:** As a pharmaceutical compliance officer, I want support for Indian languages and Estonian, so that the system can process documents in more regions.

#### Acceptance Criteria

1. THE Translation_Service SHALL support all European languages: English, French, German, Spanish, Italian, Portuguese, Russian, Dutch, Swedish, Polish, Turkish, Greek, Hebrew, Thai
2. THE Translation_Service SHALL support all Asian languages: Chinese, Japanese, Korean
3. THE Translation_Service SHALL support all Indian languages: Hindi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Marathi, Bengali, Punjabi, Urdu
4. THE Translation_Service SHALL support Estonian (ET)
5. WHEN a language is requested, THE Translation_Service SHALL map language names to correct ISO 639-1 codes for MyMemory API
6. WHEN a language is not supported, THE Translation_Service SHALL return an error indicating unsupported language
7. THE Language_Detection_Service SHALL recognize all 40+ supported languages and return appropriate language codes

### Requirement 5: Update API Endpoints for Language Support

**User Story:** As a frontend developer, I want updated API endpoints that expose language information, so that I can display supported languages and language detection results.

#### Acceptance Criteria

1. WHEN the frontend requests supported languages, THE OCR_API SHALL return a list of all 40+ supported languages with codes and names
2. WHEN a document is processed, THE OCR_API SHALL return the detected language in the response
3. WHEN a document is processed, THE OCR_API SHALL return whether translation occurred and the original language
4. WHEN the frontend requests language detection, THE OCR_API SHALL provide an endpoint to detect language from uploaded files
5. WHEN translation occurs, THE OCR_API SHALL store both original and translated text in the database
6. THE OCR_API SHALL maintain backward compatibility with existing endpoints that do not use language features

### Requirement 6: Update Frontend Language Display

**User Story:** As a user, I want to see all supported languages in the UI, so that I understand what languages the system can process.

#### Acceptance Criteria

1. WHEN the dashboard loads, THE Frontend SHALL fetch and display all 40+ supported languages
2. WHEN a document is uploaded, THE Frontend SHALL display the detected language
3. WHEN a document is translated, THE Frontend SHALL show both original and translated text
4. WHEN viewing OCR results, THE Frontend SHALL indicate whether translation occurred
5. WHEN language detection fails, THE Frontend SHALL display an appropriate error message
6. THE Frontend SHALL maintain the current UI layout while adding language information

### Requirement 7: Ensure Backward Compatibility

**User Story:** As a system maintainer, I want the new translation system to work with existing workflows, so that no existing functionality breaks.

#### Acceptance Criteria

1. WHEN existing OCR endpoints are called without language parameters, THE System SHALL process documents as before
2. WHEN existing database queries are executed, THE System SHALL return results without errors
3. WHEN existing compliance checks are performed, THE System SHALL work with both translated and non-translated text
4. WHEN existing error detection runs, THE System SHALL function correctly with the new translation service
5. WHEN existing analytics are generated, THE System SHALL include data from both old and new processing workflows
6. THE System SHALL not require changes to existing client code that does not use language features

### Requirement 8: Handle Translation Errors Gracefully

**User Story:** As a system operator, I want robust error handling for translation failures, so that the system continues functioning even when translation fails.

#### Acceptance Criteria

1. WHEN translation fails, THE System SHALL return the original text instead of failing the entire OCR process
2. WHEN MyMemory API is unavailable, THE System SHALL log the error and continue with original text
3. WHEN a language is unsupported, THE System SHALL return an error indicating the unsupported language
4. WHEN text is malformed, THE System SHALL handle it gracefully without crashing
5. WHEN multiple translation attempts fail, THE System SHALL return a descriptive error message
6. WHEN errors occur, THE System SHALL log them with sufficient detail for debugging

## Testing Requirements

- Test translation with all 40+ supported languages
- Test language detection accuracy with mixed-language documents
- Test smart chunking with documents exceeding 5000 characters
- Test backward compatibility with existing OCR workflows
- Test error handling when MyMemory API is unavailable
- Test translation of pharmaceutical-specific terminology
- Test performance with large documents (PDFs with 100+ pages)
- Test concurrent translation requests
- Verify all supported languages are properly mapped
- Test edge cases: empty text, single character, very long sentences
