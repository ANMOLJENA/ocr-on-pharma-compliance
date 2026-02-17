# Requirements Document: Ollama OCR Migration

## Introduction

This document specifies the requirements for replacing Tesseract OCR with Ollama in the OCR Compliance System. Ollama is a local LLM framework that can run vision models, providing an alternative to Tesseract for optical character recognition. The migration maintains multilingual OCR capabilities, offline processing, and seamless integration with existing compliance validation workflows while providing improved accuracy and flexibility through vision language models.

## Glossary

- **Ollama**: A local LLM framework that can run vision models for OCR and other tasks
- **Vision Model**: A machine learning model capable of understanding and extracting text from images
- **Tesseract OCR**: Current local OCR engine using traditional computer vision techniques
- **Fallback Mechanism**: A backup OCR method used when the primary method is unavailable
- **Multilingual OCR**: The ability to extract text from documents in multiple languages (40+ languages)
- **Offline Processing**: OCR processing that occurs locally without requiring cloud services
- **Model Download**: The process of downloading and caching vision models for local use
- **Model Inference**: The process of running a vision model to extract text from images
- **Confidence Score**: A numerical value (0-1) indicating the reliability of extracted text
- **Pharmaceutical Data Extraction**: Identifying and extracting drug names, batch numbers, expiry dates, and manufacturer information
- **API Compatibility**: The ability to maintain existing API endpoints without breaking changes
- **Performance Baseline**: The expected processing time and accuracy metrics for OCR operations
- **Graceful Degradation**: The system's ability to continue functioning with reduced capabilities when components fail

## Requirements

### Requirement 1: Integrate Ollama Vision Model for OCR

**User Story:** As a system administrator, I want to integrate Ollama vision models for OCR processing, so that the system can leverage advanced vision language models for text extraction.

#### Acceptance Criteria

1. WHEN the OCR service is initialized, THE OCRService SHALL detect if Ollama is available at the configured endpoint
2. WHEN Ollama is available, THE OCRService SHALL use Ollama vision models for text extraction instead of Tesseract
3. WHEN an image is provided for OCR, THE OCRService SHALL send it to Ollama for processing via the Ollama API
4. WHEN Ollama returns extracted text, THE OCRService SHALL parse the response and return structured results
5. WHEN Ollama processing completes, THE OCRService SHALL calculate a confidence score based on model output
6. WHEN Ollama is unavailable, THE OCRService SHALL fall back to Tesseract OCR automatically
7. WHEN Ollama returns an error, THE OCRService SHALL log the error and attempt fallback to Tesseract

### Requirement 2: Support Multilingual OCR with Ollama

**User Story:** As a pharmaceutical compliance officer, I want Ollama to support 40+ languages for OCR, so that documents in multiple languages can be processed accurately.

#### Acceptance Criteria

1. THE OllamaOCRService SHALL support all European languages: English, French, German, Spanish, Italian, Portuguese, Russian, Dutch, Swedish, Polish, Turkish, Greek, Hebrew, Thai
2. THE OllamaOCRService SHALL support all Asian languages: Chinese, Japanese, Korean
3. THE OllamaOCRService SHALL support all Indian languages: Hindi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Marathi, Bengali, Punjabi, Urdu
4. THE OllamaOCRService SHALL support Estonian (ET)
5. WHEN text is extracted in a non-English language, THE OllamaOCRService SHALL preserve the original language text
6. WHEN language detection is needed, THE OllamaOCRService SHALL use the existing LanguageDetectionService to identify the document language
7. WHEN a language is not supported by Ollama, THE OllamaOCRService SHALL return an error indicating unsupported language

### Requirement 3: Handle PDF Processing with Ollama

**User Story:** As a user, I want PDF documents to be processed with Ollama, so that multi-page pharmaceutical documents can be extracted accurately.

#### Acceptance Criteria

1. WHEN a PDF is provided for OCR, THE OllamaOCRService SHALL convert PDF pages to images
2. WHEN PDF pages are converted, THE OllamaOCRService SHALL process each page independently with Ollama
3. WHEN multiple pages are processed, THE OllamaOCRService SHALL combine results with page break markers
4. WHEN a PDF has many pages (100+), THE OllamaOCRService SHALL process pages sequentially to manage memory
5. WHEN PDF processing completes, THE OllamaOCRService SHALL calculate average confidence across all pages
6. WHEN PDF processing fails, THE OllamaOCRService SHALL return an error with details about which page failed

### Requirement 4: Implement Fallback to Tesseract

**User Story:** As a system operator, I want automatic fallback to Tesseract when Ollama is unavailable, so that the system continues functioning even if Ollama fails.

#### Acceptance Criteria

1. WHEN Ollama is not running, THE OCRService SHALL automatically fall back to Tesseract
2. WHEN Ollama returns an error, THE OCRService SHALL log the error and retry with Tesseract
3. WHEN Ollama times out, THE OCRService SHALL fall back to Tesseract after a configurable timeout (default 30 seconds)
4. WHEN Tesseract is also unavailable, THE OCRService SHALL return an error indicating both engines are unavailable
5. WHEN fallback occurs, THE OCRService SHALL log which engine was used in the result metadata
6. WHEN fallback occurs, THE OCRService SHALL maintain the same API response format for consistency

### Requirement 5: Configure Ollama Model Selection

**User Story:** As a system administrator, I want to configure which Ollama vision model to use, so that I can optimize for accuracy or performance.

#### Acceptance Criteria

1. WHEN the OCR service is initialized, THE OCRService SHALL read the configured Ollama model name from environment variables or config file
2. WHEN a model is configured, THE OCRService SHALL verify the model is available in Ollama before processing
3. WHEN a model is not available, THE OCRService SHALL attempt to download it automatically
4. WHEN model download fails, THE OCRService SHALL return an error indicating the model could not be loaded
5. WHEN multiple models are available, THE OCRService SHALL allow switching models via configuration
6. WHEN a model is switched, THE OCRService SHALL not require service restart (hot-swap capability)

### Requirement 6: Maintain Pharmaceutical Data Extraction

**User Story:** As a compliance officer, I want pharmaceutical data extraction to work with Ollama, so that drug names, batch numbers, and expiry dates are still extracted correctly.

#### Acceptance Criteria

1. WHEN text is extracted by Ollama, THE OCRService SHALL apply the same pharmaceutical data extraction logic as Tesseract
2. WHEN pharmaceutical fields are identified, THE OCRService SHALL extract drug name, batch number, expiry date, and manufacturer
3. WHEN controlled substances are mentioned, THE OCRService SHALL flag them appropriately
4. WHEN extraction patterns are not found, THE OCRService SHALL return null values for missing fields
5. WHEN Ollama extraction quality is lower, THE OCRService SHALL still attempt pharmaceutical data extraction
6. WHEN pharmaceutical data extraction fails, THE OCRService SHALL return the raw extracted text without structured fields

### Requirement 7: Preserve API Compatibility

**User Story:** As a frontend developer, I want the OCR API to remain unchanged, so that existing client code continues to work.

#### Acceptance Criteria

1. WHEN the `/api/ocr/upload` endpoint is called, THE API SHALL process documents with Ollama while maintaining the same response format
2. WHEN the `/api/ocr/process/<id>` endpoint is called, THE API SHALL use Ollama while returning the same response structure
3. WHEN the `/api/ocr/multilingual/upload` endpoint is called, THE API SHALL work with Ollama and return language information
4. WHEN OCR results are retrieved, THE API SHALL include the same fields as before (extracted_text, confidence_score, processing_time, etc.)
5. WHEN the frontend requests supported languages, THE API SHALL return the same language list
6. WHEN existing database queries are executed, THE System SHALL return results without schema changes

### Requirement 8: Implement Performance Monitoring

**User Story:** As a system administrator, I want to monitor Ollama OCR performance, so that I can identify bottlenecks and optimize the system.

#### Acceptance Criteria

1. WHEN OCR processing completes, THE OCRService SHALL record processing time for each document
2. WHEN processing times are recorded, THE OCRService SHALL track average processing time per page
3. WHEN Ollama is used, THE OCRService SHALL record which engine was used (Ollama or Tesseract fallback)
4. WHEN performance metrics are collected, THE OCRService SHALL store them in the database for analytics
5. WHEN performance degrades, THE OCRService SHALL log warnings if processing time exceeds thresholds
6. WHEN metrics are queried, THE API SHALL provide endpoints to retrieve performance statistics

### Requirement 9: Handle Image Preprocessing for Ollama

**User Story:** As a developer, I want image preprocessing to work with Ollama, so that document quality is optimized for vision models.

#### Acceptance Criteria

1. WHEN an image is provided, THE OllamaOCRService SHALL apply preprocessing (grayscale conversion, denoising, thresholding)
2. WHEN preprocessing is applied, THE OllamaOCRService SHALL maintain the same preprocessing pipeline as Tesseract
3. WHEN preprocessing improves image quality, THE OllamaOCRService SHALL use the preprocessed image for Ollama
4. WHEN preprocessing fails, THE OllamaOCRService SHALL attempt to use the original image
5. WHEN image quality is very poor, THE OllamaOCRService SHALL log a warning about potential accuracy issues
6. WHEN preprocessing is complete, THE OllamaOCRService SHALL pass the image to Ollama in the correct format

### Requirement 10: Ensure Graceful Error Handling

**User Story:** As a system operator, I want robust error handling for Ollama failures, so that the system continues functioning even when errors occur.

#### Acceptance Criteria

1. WHEN Ollama connection fails, THE OCRService SHALL return a descriptive error message
2. WHEN Ollama times out, THE OCRService SHALL fall back to Tesseract after timeout
3. WHEN Ollama returns invalid output, THE OCRService SHALL log the error and attempt fallback
4. WHEN both Ollama and Tesseract fail, THE OCRService SHALL return an error with details about both failures
5. WHEN errors occur, THE OCRService SHALL log them with sufficient context for debugging
6. WHEN errors are logged, THE System SHALL not crash or hang

### Requirement 11: Support Offline Operation

**User Story:** As a user in a restricted environment, I want OCR to work completely offline, so that documents can be processed without internet access.

#### Acceptance Criteria

1. WHEN Ollama is running locally, THE OCRService SHALL process documents without requiring internet access
2. WHEN Tesseract is available as fallback, THE OCRService SHALL continue working offline if Ollama fails
3. WHEN cloud OCR services are configured, THE OCRService SHALL not attempt to use them if offline mode is enabled
4. WHEN offline mode is active, THE OCRService SHALL log that processing is occurring offline
5. WHEN offline processing completes, THE OCRService SHALL store results locally without cloud synchronization
6. WHEN internet becomes available, THE System SHALL not automatically switch to cloud services

### Requirement 12: Maintain Backward Compatibility with Existing Workflows

**User Story:** As a system maintainer, I want the Ollama migration to not break existing functionality, so that all current features continue to work.

#### Acceptance Criteria

1. WHEN existing OCR endpoints are called, THE System SHALL process documents with Ollama while maintaining the same behavior
2. WHEN existing database queries are executed, THE System SHALL return results without errors
3. WHEN existing compliance checks are performed, THE System SHALL work with Ollama-extracted text
4. WHEN existing error detection runs, THE System SHALL function correctly with Ollama results
5. WHEN existing analytics are generated, THE System SHALL include data from Ollama processing
6. WHEN existing client code is used, THE System SHALL not require any changes

## Testing Requirements

- Test Ollama OCR with all 40+ supported languages
- Test PDF processing with documents of varying page counts (1, 10, 50, 100+ pages)
- Test fallback to Tesseract when Ollama is unavailable
- Test fallback when Ollama times out
- Test pharmaceutical data extraction with Ollama results
- Test API compatibility with existing endpoints
- Test performance metrics collection and reporting
- Test image preprocessing with various image qualities
- Test error handling for invalid inputs
- Test offline operation without internet access
- Test concurrent OCR requests
- Test model switching without service restart
- Test memory usage with large documents
- Test confidence score calculation
- Verify all supported languages are properly handled
- Test edge cases: empty images, corrupted PDFs, very large files

