# Implementation Plan: Ollama OCR Migration

## Overview

This implementation plan breaks down the Ollama OCR migration into discrete coding tasks. The approach follows a layered strategy: first establishing the Ollama service infrastructure, then implementing fallback mechanisms, followed by integration with existing systems, and finally comprehensive testing. Each task builds on previous work with no orphaned code.

## Tasks

- [x] 1. Set up Ollama OCR service infrastructure
  - [x] 1.1 Create OllamaOCRService class with basic structure
    - Create `backend/services/ollama_ocr_service.py`
    - Define OllamaOCRService class with __init__, process_image, process_pdf methods
    - Implement Ollama API client initialization
    - _Requirements: 1.1, 5.1_
  
  - [x] 1.2 Write property test for Ollama availability detection
    - **Property 1: OCR Engine Fallback Mechanism**
    - **Validates: Requirements 1.1, 4.1**
  
  - [x] 1.3 Implement Ollama endpoint configuration
    - Read OLLAMA_ENDPOINT, OLLAMA_MODEL, OLLAMA_TIMEOUT from environment
    - Create configuration in `backend/config.py`
    - Implement model availability verification
    - _Requirements: 5.1, 5.2_
  
  - [x] 1.4 Write property test for configuration reading
    - **Property 5: Confidence Score Validity**
    - **Validates: Requirements 5.1**

- [x] 2. Implement Ollama image processing
  - [x] 2.1 Implement image preprocessing for Ollama
    - Reuse existing preprocessing logic from OCRService
    - Convert images to format compatible with Ollama API
    - Handle image encoding (base64 or binary)
    - _Requirements: 9.1, 9.2, 9.3_
  
  - [x] 2.2 Write property test for image preprocessing
    - **Property 9: Offline Processing Capability**
    - **Validates: Requirements 9.1, 9.2**
  
  - [x] 2.3 Implement Ollama API communication
    - Create _send_to_ollama method to send images to Ollama endpoint
    - Handle HTTP requests with timeout (default 30 seconds)
    - Parse Ollama responses
    - _Requirements: 1.3, 1.4_
  
  - [x] 2.4 Write property test for Ollama API communication
    - **Property 2: API Response Format Consistency**
    - **Validates: Requirements 1.3, 1.4**
  
  - [x] 2.5 Implement confidence score calculation for Ollama
    - Extract confidence from Ollama response
    - Calculate confidence score (0-1 range)
    - Ensure score validity
    - _Requirements: 1.5, 6.1_
  
  - [x] 2.6 Write property test for confidence score calculation
    - **Property 6: Confidence Score Validity**
    - **Validates: Requirements 1.5**

- [x] 3. Implement PDF processing with Ollama
  - [x] 3.1 Implement PDF to image conversion
    - Reuse existing pdf2image logic
    - Convert each PDF page to image
    - Handle large PDFs (100+ pages) with sequential processing
    - _Requirements: 3.1, 3.4_
  
  - [x] 3.2 Write property test for PDF page processing
    - **Property 5: PDF Multi-Page Processing**
    - **Validates: Requirements 3.1, 3.2, 3.3_
  
  - [x] 3.3 Implement multi-page result combination
    - Process each page with Ollama
    - Combine results with page break markers
    - Calculate average confidence across pages
    - _Requirements: 3.2, 3.3, 3.5_
  
  - [x] 3.4 Write property test for PDF result combination
    - **Property 5: PDF Multi-Page Processing**
    - **Validates: Requirements 3.3, 3.5**
  
  - [x] 3.5 Implement PDF error handling
    - Handle PDF conversion failures
    - Handle page processing failures
    - Return error with page details
    - _Requirements: 3.6_

- [x] 4. Implement fallback mechanism
  - [x] 4.1 Enhance OCRService factory with Ollama detection
    - Modify OCRService.__init__ to detect Ollama availability
    - Implement _is_ollama_available method
    - Create _get_ocr_service method to route to appropriate service
    - _Requirements: 1.1, 1.2, 4.1_
  
  - [x] 4.2 Write property test for Ollama availability detection
    - **Property 1: OCR Engine Fallback Mechanism**
    - **Validates: Requirements 1.1, 1.2, 4.1**
  
  - [x] 4.3 Implement fallback logic with timeout handling
    - Implement _execute_with_fallback method
    - Handle Ollama timeout (default 30 seconds)
    - Catch Ollama connection errors
    - Fall back to Tesseract on any error
    - _Requirements: 4.1, 4.2, 4.3_
  
  - [x] 4.4 Write property test for fallback mechanism
    - **Property 1: OCR Engine Fallback Mechanism**
    - **Validates: Requirements 4.1, 4.2, 4.3**
  
  - [x] 4.5 Implement engine tracking in results
    - Add ocr_engine field to OCRResult
    - Track which engine was used (ollama or tesseract)
    - Track fallback_used flag
    - _Requirements: 4.5, 8.3_
  
  - [x] 4.6 Write property test for engine tracking
    - **Property 8: Backward Compatibility Preservation**
    - **Validates: Requirements 4.5, 8.3**

- [x] 5. Implement pharmaceutical data extraction
  - [x] 5.1 Reuse pharmaceutical data extraction logic
    - Extract _extract_pharmaceutical_data method from OCRService
    - Apply same logic to Ollama results
    - Extract drug name, batch number, expiry date, manufacturer
    - _Requirements: 6.1, 6.2_
  
  - [x] 5.2 Write property test for pharmaceutical data extraction
    - **Property 3: Pharmaceutical Data Extraction Preservation**
    - **Validates: Requirements 6.1, 6.2**
  
  - [x] 5.3 Implement controlled substance detection
    - Detect controlled substance mentions in text
    - Flag controlled_substance field appropriately
    - _Requirements: 6.3_
  
  - [x] 5.4 Write property test for controlled substance detection
    - **Property 3: Pharmaceutical Data Extraction Preservation**
    - **Validates: Requirements 6.3**
  
  - [x] 5.5 Implement graceful handling of missing fields
    - Return null values for fields not found
    - Return raw text when extraction fails
    - _Requirements: 6.4, 6.6_

- [x] 6. Implement multilingual support
  - [x] 6.1 Define supported languages list
    - Create language configuration with 40+ languages
    - Include European, Asian, and Indian languages
    - Include Estonian
    - _Requirements: 2.1, 2.2, 2.3, 2.4_
  
  - [x] 6.2 Write property test for language support
    - **Property 4: Multilingual Text Extraction**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4**
  
  - [x] 6.3 Implement language preservation
    - Ensure non-English text is preserved
    - Handle Unicode characters correctly
    - _Requirements: 2.5_
  
  - [x] 6.4 Write property test for language preservation
    - **Property 4: Multilingual Text Extraction**
    - **Validates: Requirements 2.5**
  
  - [x] 6.5 Integrate with LanguageDetectionService
    - Call LanguageDetectionService when needed
    - Use detected language for processing
    - _Requirements: 2.6_

- [x] 7. Update OCR routes for Ollama
  - [x] 7.1 Update /api/ocr/upload endpoint
    - Modify to use new OCRService with Ollama support
    - Maintain same response format
    - Include ocr_engine in response
    - _Requirements: 7.1, 7.4_
  
  - [x] 7.2 Write property test for /api/ocr/upload endpoint
    - **Property 2: API Response Format Consistency**
    - **Validates: Requirements 7.1, 7.4**
  
  - [x] 7.3 Update /api/ocr/process/<id> endpoint
    - Modify to use new OCRService with Ollama support
    - Maintain same response structure
    - _Requirements: 7.2_
  
  - [x] 7.4 Update /api/ocr/multilingual/upload endpoint
    - Ensure multilingual support works with Ollama
    - Return language information
    - _Requirements: 7.3_
  
  - [x] 7.5 Write property test for multilingual endpoint
    - **Property 2: API Response Format Consistency**
    - **Validates: Requirements 7.3**
  
  - [x] 7.6 Verify /api/ocr/multilingual/languages endpoint
    - Ensure language list includes all 40+ languages
    - _Requirements: 7.5_

- [x] 8. Implement performance monitoring
  - [x] 8.1 Add performance metrics tracking
    - Record processing time for each document
    - Track average processing time per page
    - Store metrics in database
    - _Requirements: 8.1, 8.2, 8.4_
  
  - [x] 8.2 Write property test for performance tracking
    - **Property 8: Backward Compatibility Preservation**
    - **Validates: Requirements 8.1, 8.2, 8.4**
  
  - [x] 8.3 Implement performance threshold monitoring
    - Log warnings when processing time exceeds thresholds
    - Track performance degradation
    - _Requirements: 8.5_
  
  - [x] 8.4 Create performance statistics endpoint
    - Add /api/ocr/stats endpoint
    - Return performance statistics
    - _Requirements: 8.6_

- [x] 9. Implement error handling and logging
  - [x] 9.1 Implement comprehensive error handling
    - Handle Ollama connection errors
    - Handle Ollama timeout errors
    - Handle invalid Ollama responses
    - Handle both engines unavailable
    - _Requirements: 10.1, 10.2, 10.3, 10.4_
  
  - [x] 9.2 Write property test for error handling
    - **Property 8: Backward Compatibility Preservation**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.4**
  
  - [x] 9.3 Implement detailed logging
    - Log all Ollama connection attempts
    - Log fallback events with reason
    - Log errors with full context
    - Create `backend/logs/ocr_service.log`
    - _Requirements: 10.5, 10.6_
  
  - [x] 9.4 Write property test for logging
    - **Property 8: Backward Compatibility Preservation**
    - **Validates: Requirements 10.5, 10.6**

- [x] 10. Implement offline mode support
  - [x] 10.1 Add offline mode configuration
    - Add OFFLINE_MODE environment variable
    - Prevent cloud service usage in offline mode
    - _Requirements: 11.3, 11.4_
  
  - [x] 10.2 Implement offline processing
    - Process documents with Ollama and Tesseract only
    - Store results locally
    - _Requirements: 11.1, 11.2, 11.5_
  
  - [x] 10.3 Write property test for offline operation
    - **Property 7: Offline Processing Capability**
    - **Validates: Requirements 11.1, 11.2, 11.5**
  
  - [x] 10.4 Implement offline mode persistence
    - Ensure system stays in offline mode
    - Don't auto-switch to cloud services
    - _Requirements: 11.6_

- [x] 11. Update database schema
  - [x] 11.1 Add Ollama-specific fields to OCRResult
    - Add ocr_engine column (String)
    - Add model_name column (String)
    - Add fallback_used column (Boolean)
    - Add metadata column (JSON)
    - _Requirements: 8.3_
  
  - [x] 11.2 Create database migration
    - Create migration script for new columns
    - Ensure backward compatibility
    - _Requirements: 12.2_

- [x] 12. Implement model management
  - [x] 12.1 Implement model availability verification
    - Check if configured model exists in Ollama
    - Implement _verify_model_available method
    - _Requirements: 5.2_
  
  - [x] 12.2 Implement automatic model download
    - Attempt to download model if not available
    - Implement _download_model method
    - Handle download failures
    - _Requirements: 5.3, 5.4_
  
  - [x] 12.3 Write property test for model management
    - **Property 5: Confidence Score Validity**
    - **Validates: Requirements 5.2, 5.3, 5.4**
  
  - [x] 12.4 Implement model hot-swap capability
    - Allow switching models via configuration
    - Don't require service restart
    - _Requirements: 5.5, 5.6_

- [x] 13. Checkpoint - Ensure all core functionality works
  - Verify Ollama service initializes correctly
  - Verify fallback to Tesseract works
  - Verify API endpoints return correct format
  - Verify database storage works
  - Ensure all tests pass

- [x] 14. Write comprehensive integration tests
  - [x] 14.1 Test end-to-end OCR with Ollama
    - Upload image → Process with Ollama → Verify results
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  
  - [x] 14.2 Test end-to-end OCR with Tesseract fallback
    - Simulate Ollama unavailable → Verify Tesseract used
    - _Requirements: 4.1, 4.2, 4.3_
  
  - [x] 14.3 Test PDF processing
    - Upload multi-page PDF → Verify all pages processed
    - _Requirements: 3.1, 3.2, 3.3_
  
  - [x] 14.4 Test multilingual support
    - Upload documents in multiple languages
    - Verify text preserved correctly
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  
  - [x] 14.5 Test pharmaceutical data extraction
    - Verify drug names, batch numbers extracted
    - Verify controlled substances flagged
    - _Requirements: 6.1, 6.2, 6.3_
  
  - [x] 14.6 Test API compatibility
    - Verify existing endpoints work
    - Verify response format unchanged
    - _Requirements: 7.1, 7.2, 7.3, 7.4_
  
  - [x] 14.7 Test error handling
    - Test with invalid images
    - Test with corrupted PDFs
    - Test with both engines unavailable
    - _Requirements: 10.1, 10.2, 10.3, 10.4_
  
  - [x] 14.8 Test offline operation
    - Verify processing works without internet
    - Verify cloud services not used
    - _Requirements: 11.1, 11.2, 11.3_

- [x] 15. Write unit tests for OllamaOCRService
  - [x] 15.1 Test image preprocessing
    - Test grayscale conversion
    - Test denoising
    - Test thresholding
    - _Requirements: 9.1, 9.2_
  
  - [x] 15.2 Test Ollama API communication
    - Mock Ollama responses
    - Test response parsing
    - Test error handling
    - _Requirements: 1.3, 1.4_
  
  - [x] 15.3 Test confidence score calculation
    - Test score range (0-1)
    - Test calculation logic
    - _Requirements: 1.5_
  
  - [x] 15.4 Test pharmaceutical data extraction
    - Test field extraction
    - Test controlled substance detection
    - _Requirements: 6.1, 6.2, 6.3_
  
  - [x] 15.5 Test PDF processing
    - Test page conversion
    - Test result combination
    - Test average confidence calculation
    - _Requirements: 3.1, 3.2, 3.3, 3.5_

- [x] 16. Write unit tests for OCRService factory
  - [x] 16.1 Test Ollama availability detection
    - Test when Ollama is available
    - Test when Ollama is unavailable
    - _Requirements: 1.1_
  
  - [x] 16.2 Test service routing
    - Test routing to OllamaOCRService
    - Test routing to TesseractOCRService
    - _Requirements: 1.2_
  
  - [x] 16.3 Test fallback logic
    - Test fallback on timeout
    - Test fallback on error
    - Test fallback when both unavailable
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  
  - [x] 16.4 Test engine tracking
    - Test ocr_engine field set correctly
    - Test fallback_used flag set correctly
    - _Requirements: 4.5_

- [x] 17. Final checkpoint - Ensure all tests pass
  - Run all unit tests
  - Run all integration tests
  - Run all property-based tests
  - Verify no regressions in existing functionality
  - Ensure all requirements covered

- [x] 18. Documentation and deployment preparation
  - [x] 18.1 Create deployment guide
    - Document Ollama installation steps
    - Document model download steps
    - Document configuration steps
    - _Requirements: 5.1, 5.2_
  
  - [x] 18.2 Create configuration documentation
    - Document environment variables
    - Document config file format
    - Document model selection
    - _Requirements: 5.1, 5.5_
  
  - [x] 18.3 Create troubleshooting guide
    - Document common errors
    - Document fallback behavior
    - Document logging locations
    - _Requirements: 10.5, 10.6_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property-based tests use Hypothesis framework with minimum 100 iterations
- All tests should pass before proceeding to next phase
- Fallback mechanism is critical - test thoroughly
- Multilingual support must be verified with actual language samples
- Performance metrics should be monitored during testing
- Database migrations should be tested on both SQLite and PostgreSQL

