# Design Document: Ollama OCR Migration

## Overview

This design document outlines the architecture for replacing Tesseract OCR with Ollama in the OCR Compliance System. The migration introduces a new `OllamaOCRService` that leverages Ollama's vision models for text extraction while maintaining backward compatibility through a fallback mechanism to Tesseract. The system maintains multilingual support (40+ languages), offline processing capabilities, and seamless integration with existing compliance validation workflows.

### Key Design Decisions

1. **Layered Architecture**: Introduce `OllamaOCRService` as a new implementation while keeping `TesseractOCRService` as fallback
2. **Fallback Strategy**: Automatic fallback to Tesseract when Ollama is unavailable or times out
3. **Configuration-Driven**: Model selection and Ollama endpoint configurable via environment variables
4. **Minimal API Changes**: Maintain existing API contracts to ensure frontend compatibility
5. **Metadata Tracking**: Record which OCR engine was used for analytics and debugging

## Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                         │
│              /api/ocr/upload, /api/ocr/process              │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   OCR Routes (Flask)                        │
│         Handles file upload, validation, routing            │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              OCRService (Factory/Orchestrator)              │
│  - Detects Ollama availability                             │
│  - Routes to OllamaOCRService or TesseractOCRService       │
│  - Implements fallback logic                               │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
┌───────▼──────────────┐      ┌──────────▼──────────────┐
│ OllamaOCRService     │      │ TesseractOCRService     │
│ - Vision models      │      │ - Traditional OCR       │
│ - Multilingual       │      │ - Fallback option       │
│ - PDF handling       │      │ - Reliable baseline     │
└───────┬──────────────┘      └──────────┬──────────────┘
        │                                 │
        │ HTTP/REST                       │ Direct
        │                                 │
┌───────▼──────────────┐      ┌──────────▼──────────────┐
│   Ollama Server      │      │   Tesseract Binary     │
│  (Local LLM)         │      │   (System Binary)      │
└──────────────────────┘      └───────────────────────┘
```

### Component Interaction Flow

```
Document Upload
    │
    ▼
OCR Routes (upload endpoint)
    │
    ├─ File validation
    ├─ File storage
    ├─ Database record creation
    │
    ▼
OCRService.process_image() or process_pdf()
    │
    ├─ Check Ollama availability
    │
    ├─ YES: Use OllamaOCRService
    │   ├─ Image preprocessing
    │   ├─ Send to Ollama API
    │   ├─ Parse response
    │   ├─ Calculate confidence
    │   └─ Extract pharmaceutical data
    │
    ├─ NO or TIMEOUT: Fall back to TesseractOCRService
    │   ├─ Image preprocessing
    │   ├─ Run Tesseract
    │   ├─ Calculate confidence
    │   └─ Extract pharmaceutical data
    │
    ▼
Return Results
    ├─ extracted_text
    ├─ confidence_score
    ├─ processing_time
    ├─ ocr_engine (ollama or tesseract)
    ├─ pharmaceutical_data
    └─ metadata
```

## Components and Interfaces

### 1. OllamaOCRService

**Purpose**: Implements OCR using Ollama vision models

**Key Methods**:

```python
class OllamaOCRService:
    def __init__(self, ollama_endpoint: str, model_name: str, timeout: int = 30)
    def process_image(self, image_path: str) -> Dict[str, Any]
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]
    def _send_to_ollama(self, image_data: bytes) -> str
    def _verify_model_available(self) -> bool
    def _download_model(self) -> bool
    def _preprocess_image(self, image_path: str) -> bytes
    def _calculate_confidence(self, ollama_response: str) -> float
    def _extract_pharmaceutical_data(self, text: str) -> Dict[str, Any]
```

**Responsibilities**:
- Convert images to format compatible with Ollama
- Send images to Ollama API endpoint
- Parse Ollama responses
- Calculate confidence scores
- Extract pharmaceutical data
- Handle errors and timeouts

### 2. Enhanced OCRService (Factory Pattern)

**Purpose**: Routes OCR requests to appropriate service (Ollama or Tesseract)

**Key Methods**:

```python
class OCRService:
    def __init__(self, tesseract_cmd=None, use_ollama=True, ollama_endpoint=None, ollama_model=None)
    def process_image(self, image_path: str) -> Dict[str, Any]
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]
    def _is_ollama_available(self) -> bool
    def _get_ocr_service(self) -> Union[OllamaOCRService, TesseractOCRService]
    def _execute_with_fallback(self, primary_fn, fallback_fn) -> Dict[str, Any]
```

**Responsibilities**:
- Detect Ollama availability
- Route to appropriate OCR service
- Implement fallback logic
- Track which engine was used
- Maintain consistent API

### 3. Configuration Management

**Environment Variables**:
```
OLLAMA_ENABLED=true
OLLAMA_ENDPOINT=http://localhost:11434
OLLAMA_MODEL=llava:latest
OLLAMA_TIMEOUT=30
TESSERACT_CMD=/usr/bin/tesseract
TESSERACT_FALLBACK=true
```

**Configuration File** (`backend/config.py`):
```python
OCR_CONFIG = {
    'ollama': {
        'enabled': os.getenv('OLLAMA_ENABLED', 'true').lower() == 'true',
        'endpoint': os.getenv('OLLAMA_ENDPOINT', 'http://localhost:11434'),
        'model': os.getenv('OLLAMA_MODEL', 'llava:latest'),
        'timeout': int(os.getenv('OLLAMA_TIMEOUT', '30')),
    },
    'tesseract': {
        'cmd': os.getenv('TESSERACT_CMD'),
        'fallback_enabled': os.getenv('TESSERACT_FALLBACK', 'true').lower() == 'true',
    }
}
```

## Data Models

### OCRResult Enhancement

**New Fields**:
```python
class OCRResult(db.Model):
    # Existing fields
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    extracted_text = db.Column(db.Text)
    confidence_score = db.Column(db.Float)
    processing_time = db.Column(db.Float)
    
    # New fields for Ollama migration
    ocr_engine = db.Column(db.String(50), default='tesseract')  # 'ollama' or 'tesseract'
    model_name = db.Column(db.String(100))  # e.g., 'llava:latest'
    fallback_used = db.Column(db.Boolean, default=False)
    
    # Metadata for tracking
    metadata = db.Column(db.JSON, default={})  # Stores additional info
```

**Metadata Structure**:
```json
{
    "ocr_engine": "ollama",
    "model_name": "llava:latest",
    "fallback_used": false,
    "preprocessing_applied": true,
    "ollama_response_time": 2.5,
    "confidence_calculation_method": "model_output"
}
```

## Error Handling

### Error Scenarios and Responses

| Scenario | Primary Action | Fallback Action | Response |
|----------|---|---|---|
| Ollama unavailable | Skip Ollama | Use Tesseract | Success with `ocr_engine: tesseract` |
| Ollama timeout | Retry once | Use Tesseract | Success with `ocr_engine: tesseract` |
| Ollama error | Log error | Use Tesseract | Success with `ocr_engine: tesseract` |
| Model not found | Download model | Use Tesseract | Success or error if both fail |
| Tesseract unavailable | Error | N/A | Error: "No OCR engines available" |
| Invalid image | Log error | Try fallback | Error or fallback result |
| PDF conversion fails | Log error | Try fallback | Error or fallback result |

### Error Handling Code Pattern

```python
def process_image(self, image_path: str) -> Dict[str, Any]:
    try:
        if self._is_ollama_available():
            return self._process_with_ollama(image_path)
    except OllamaTimeoutError:
        logger.warning(f"Ollama timeout, falling back to Tesseract")
        return self._process_with_tesseract(image_path, fallback=True)
    except OllamaConnectionError:
        logger.warning(f"Ollama unavailable, falling back to Tesseract")
        return self._process_with_tesseract(image_path, fallback=True)
    except Exception as e:
        logger.error(f"Ollama error: {e}, falling back to Tesseract")
        return self._process_with_tesseract(image_path, fallback=True)
    
    # If Ollama not enabled, use Tesseract
    return self._process_with_tesseract(image_path)
```

## Testing Strategy

### Unit Testing

**OllamaOCRService Tests**:
- Test image preprocessing
- Test Ollama API communication
- Test response parsing
- Test confidence score calculation
- Test pharmaceutical data extraction
- Test error handling
- Test timeout handling
- Test model availability check

**OCRService Factory Tests**:
- Test Ollama availability detection
- Test fallback to Tesseract
- Test service routing
- Test API compatibility

**Integration Tests**:
- Test end-to-end OCR with Ollama
- Test end-to-end OCR with Tesseract fallback
- Test PDF processing
- Test multilingual support
- Test database storage
- Test API endpoints

### Property-Based Testing

**Property 1: OCR Engine Fallback**
- *For any* image, if Ollama is unavailable, the system should fall back to Tesseract and return valid results
- **Validates: Requirements 4, 10**

**Property 2: API Response Consistency**
- *For any* document processed with either Ollama or Tesseract, the API response should contain all required fields (extracted_text, confidence_score, processing_time)
- **Validates: Requirements 7**

**Property 3: Pharmaceutical Data Extraction**
- *For any* text extracted by Ollama, pharmaceutical data extraction should identify drug names, batch numbers, and expiry dates using the same patterns as Tesseract
- **Validates: Requirements 6**

**Property 4: Multilingual Support**
- *For any* supported language (40+ languages), Ollama should extract text without errors
- **Validates: Requirements 2**

**Property 5: PDF Processing Consistency**
- *For any* PDF document, processing with Ollama should return combined text from all pages with page break markers
- **Validates: Requirements 3**

**Property 6: Confidence Score Validity**
- *For any* OCR result, the confidence score should be between 0 and 1
- **Validates: Requirements 1**

**Property 7: Offline Operation**
- *For any* document processed with Ollama when internet is unavailable, the system should complete processing without attempting cloud services
- **Validates: Requirements 11**

**Property 8: Backward Compatibility**
- *For any* existing OCR workflow, the system should produce results with the same schema as before
- **Validates: Requirements 12**

### Edge Cases

- Empty images
- Corrupted PDF files
- Very large images (>10MB)
- PDFs with 100+ pages
- Images with no text
- Mixed language documents
- Low-quality scans
- Rotated images
- Images with watermarks

## Performance Considerations

### Baseline Metrics

| Metric | Tesseract | Ollama (Expected) | Target |
|--------|-----------|-------------------|--------|
| Single page processing | 1-2 seconds | 2-5 seconds | <10 seconds |
| PDF (10 pages) | 10-20 seconds | 20-50 seconds | <60 seconds |
| Memory per page | ~50MB | ~100-200MB | <500MB |
| Confidence accuracy | 70-80% | 80-90% | >85% |

### Optimization Strategies

1. **Batch Processing**: Process multiple pages in parallel (with memory limits)
2. **Model Caching**: Keep model in memory between requests
3. **Image Optimization**: Resize large images before sending to Ollama
4. **Async Processing**: Use async/await for I/O operations
5. **Connection Pooling**: Reuse HTTP connections to Ollama

## Deployment Considerations

### Prerequisites

1. **Ollama Installation**: System must have Ollama installed and running
2. **Vision Model**: Download required vision model (e.g., `ollama pull llava`)
3. **Tesseract Fallback**: Tesseract should be installed as fallback
4. **Environment Configuration**: Set environment variables for Ollama endpoint and model

### Deployment Steps

1. Install Ollama on the server
2. Download vision model: `ollama pull llava:latest`
3. Start Ollama service: `ollama serve`
4. Update backend configuration with Ollama endpoint
5. Deploy updated OCR service code
6. Test with sample documents
7. Monitor performance and fallback rates

### Rollback Plan

1. If Ollama causes issues, disable it: `OLLAMA_ENABLED=false`
2. System automatically falls back to Tesseract
3. No code changes required
4. No database migration needed

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property 1: OCR Engine Fallback Mechanism

*For any* image file and any Ollama unavailability scenario (timeout, connection error, model not found), the system should automatically fall back to Tesseract and return valid OCR results with the same response structure.

**Validates: Requirements 4, 10**

### Property 2: API Response Format Consistency

*For any* document processed with either Ollama or Tesseract, the API response should contain all required fields: `extracted_text`, `confidence_score`, `processing_time`, `ocr_engine`, and pharmaceutical data fields (`drug_name`, `batch_number`, `expiry_date`, `manufacturer`, `controlled_substance`).

**Validates: Requirements 7**

### Property 3: Pharmaceutical Data Extraction Preservation

*For any* text extracted by Ollama, applying the pharmaceutical data extraction logic should identify the same fields (drug name, batch number, expiry date, manufacturer) as when applied to Tesseract-extracted text with the same source document.

**Validates: Requirements 6**

### Property 4: Multilingual Text Extraction

*For any* supported language (40+ languages including European, Asian, and Indian languages), Ollama should extract text from images without errors and preserve the original language characters.

**Validates: Requirements 2**

### Property 5: PDF Multi-Page Processing

*For any* PDF document with multiple pages, processing with Ollama should return combined text from all pages with page break markers ("--- Page Break ---") separating pages, and the confidence score should be the average of all pages.

**Validates: Requirements 3**

### Property 6: Confidence Score Validity

*For any* OCR result from either Ollama or Tesseract, the confidence score should be a valid number between 0 and 1 (inclusive).

**Validates: Requirements 1**

### Property 7: Offline Processing Capability

*For any* document processed with Ollama when the system is in offline mode, the system should complete processing using only local resources without attempting to connect to cloud services or external APIs.

**Validates: Requirements 11**

### Property 8: Backward Compatibility Preservation

*For any* existing OCR workflow that does not explicitly use Ollama features, the system should produce results with the same database schema and API response structure as the previous Tesseract-only implementation.

**Validates: Requirements 12**

## Error Handling

### Error Categories

1. **Ollama Connection Errors**
   - Endpoint unreachable
   - Service not running
   - Network timeout
   - Action: Log and fallback to Tesseract

2. **Model Errors**
   - Model not found
   - Model download failed
   - Model inference error
   - Action: Log and fallback to Tesseract

3. **Image Processing Errors**
   - Invalid image format
   - Corrupted image data
   - Unsupported image type
   - Action: Log and return error or fallback

4. **PDF Processing Errors**
   - PDF conversion failed
   - Poppler not installed
   - Corrupted PDF
   - Action: Log and return error

5. **Data Extraction Errors**
   - Pharmaceutical data not found
   - Malformed response
   - Encoding issues
   - Action: Return partial results with null fields

### Logging Strategy

- Log all Ollama connection attempts and results
- Log fallback events with reason
- Log processing times for performance monitoring
- Log errors with full context for debugging
- Store logs in `backend/logs/ocr_service.log`

## Testing Strategy

### Unit Testing Approach

**Test Coverage**:
- OllamaOCRService: 80%+ coverage
- OCRService factory: 90%+ coverage
- Error handling: 100% coverage
- Fallback logic: 100% coverage

**Test Framework**: pytest with fixtures for mocking Ollama

**Mock Strategy**:
- Mock Ollama API responses
- Mock Tesseract for isolation
- Mock file I/O for speed
- Use real images for integration tests

### Property-Based Testing Configuration

**Framework**: Hypothesis (Python)

**Test Configuration**:
- Minimum 100 iterations per property test
- Generate random images, PDFs, and text
- Test with all 40+ supported languages
- Tag format: `Feature: ollama-ocr-migration, Property {number}: {property_text}`

**Example Property Test**:
```python
@given(image_data=st.binary(min_size=100, max_size=1000000))
def test_ocr_response_format_consistency(image_data):
    """Property: API response format consistency"""
    # Save image
    # Process with OCR
    # Verify response contains all required fields
    # Verify confidence_score is between 0 and 1
    pass
```

### Integration Testing

**Test Scenarios**:
1. Upload image → OCR with Ollama → Verify results
2. Upload image → Ollama unavailable → Fallback to Tesseract
3. Upload PDF → Process with Ollama → Verify all pages processed
4. Upload multilingual document → Verify language preserved
5. Verify pharmaceutical data extraction
6. Verify API endpoints return correct format
7. Verify database storage
8. Verify performance metrics collection

