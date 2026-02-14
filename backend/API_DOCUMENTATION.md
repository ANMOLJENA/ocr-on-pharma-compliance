# OCR Compliance System - API Documentation

## Base URL
```
http://localhost:5000/api
```

## Health Check

### Check Backend Status
**GET** `/health`

**URL:** `http://localhost:5000/health`

**Response:**
```json
{
  "status": "healthy",
  "message": "OCR Compliance API is running"
}
```

---

## OCR Operations

### 1. Upload and Process Document (Multilingual)
**POST** `/ocr/multilingual/upload`

**URL:** `http://localhost:5000/api/ocr/multilingual/upload`

**Method:** POST (Form Data)

**Body:**
- `file` (file): Image (PNG, JPG, TIFF) or PDF document

**Response:**
```json
{
  "success": true,
  "document_id": 1,
  "ocr_result_id": 1,
  "detected_language": "French",
  "original_language": "French",
  "translated": true,
  "original_text": "Original French text...",
  "translated_text": "Translated English text...",
  "data": {
    "id": 1,
    "document_id": 1,
    "extracted_text": "Translated English text...",
    "confidence_score": 0.95,
    "processing_time": 2.34,
    "processed_date": "2026-01-28T10:30:00",
    "drug_name": "Aspirin",
    "batch_number": "BATCH123",
    "expiry_date": "2026-12-31",
    "manufacturer": "Pharma Corp",
    "controlled_substance": false
  }
}
```

---

### 2. Get OCR Result by ID
**GET** `/ocr/results/{result_id}`

**URL:** `http://localhost:5000/api/ocr/results/1`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "document_id": 1,
    "extracted_text": "Extracted text content...",
    "confidence_score": 0.95,
    "processing_time": 2.34,
    "processed_date": "2026-01-28T10:30:00",
    "drug_name": "Aspirin",
    "batch_number": "BATCH123",
    "expiry_date": "2026-12-31",
    "manufacturer": "Pharma Corp",
    "controlled_substance": false
  }
}
```

---

### 3. List All Documents
**GET** `/ocr/documents`

**URL:** `http://localhost:5000/api/ocr/documents`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "filename": "pharma_label.png",
      "file_type": "png",
      "file_size": 245678,
      "upload_date": "2026-01-28T10:30:00",
      "status": "completed"
    },
    {
      "id": 2,
      "filename": "prescription_label.pdf",
      "file_type": "pdf",
      "file_size": 512345,
      "upload_date": "2026-01-28T11:00:00",
      "status": "completed"
    }
  ]
}
```

---

### 4. Get Supported Languages
**GET** `/ocr/multilingual/languages`

**URL:** `http://localhost:5000/api/ocr/multilingual/languages`

**Response:**
```json
{
  "success": true,
  "supported_languages": {
    "eng": "English",
    "fra": "French",
    "deu": "German",
    "spa": "Spanish",
    "ita": "Italian",
    "por": "Portuguese",
    "rus": "Russian",
    "jpn": "Japanese",
    "kor": "Korean",
    "zho": "Chinese",
    "ara": "Arabic",
    "hin": "Hindi",
    "ben": "Bengali",
    "nld": "Dutch",
    "swe": "Swedish",
    "pol": "Polish",
    "tur": "Turkish",
    "gre": "Greek",
    "heb": "Hebrew",
    "tha": "Thai"
  }
}
```

---

## Analytics Operations

### 1. Get Dashboard Statistics
**GET** `/analytics/dashboard`

**URL:** `http://localhost:5000/api/analytics/dashboard`

**Response:**
```json
{
  "success": true,
  "data": {
    "total_documents": 42,
    "status_breakdown": {
      "completed": 40,
      "processing": 1,
      "failed": 1
    },
    "average_confidence": 0.94,
    "compliance": {
      "total_checks": 120,
      "passed": 115,
      "failed": 5,
      "pass_rate": 0.958
    },
    "total_errors": 8,
    "recent_activity": 5
  }
}
```

---

### 2. Get Accuracy Metrics
**GET** `/analytics/accuracy`

**URL:** `http://localhost:5000/api/analytics/accuracy`

**Response:**
```json
{
  "success": true,
  "data": {
    "confidence_distribution": [
      {
        "range": "90-100%",
        "count": 35
      },
      {
        "range": "80-90%",
        "count": 5
      },
      {
        "range": "70-80%",
        "count": 2
      }
    ],
    "average_processing_time": 2.45
  }
}
```

---

### 3. Get Compliance Trends
**GET** `/analytics/compliance-trends`

**URL:** `http://localhost:5000/api/analytics/compliance-trends`

**Response:**
```json
{
  "success": true,
  "data": {
    "2026-01-28": {
      "passed": 15,
      "failed": 2,
      "warning": 1
    },
    "2026-01-27": {
      "passed": 12,
      "failed": 1,
      "warning": 2
    }
  }
}
```

---

### 4. Get Error Analysis
**GET** `/analytics/error-analysis`

**URL:** `http://localhost:5000/api/analytics/error-analysis`

**Response:**
```json
{
  "success": true,
  "data": {
    "error_types": [
      {
        "type": "missing_field",
        "count": 3
      },
      {
        "type": "invalid_format",
        "count": 2
      },
      {
        "type": "ocr_confidence_low",
        "count": 3
      }
    ],
    "common_fields": [
      {
        "field": "expiry_date",
        "count": 4
      },
      {
        "field": "batch_number",
        "count": 2
      },
      {
        "field": "manufacturer",
        "count": 2
      }
    ]
  }
}
```

---

### 5. Get Controlled Substances Statistics
**GET** `/analytics/controlled-substances`

**URL:** `http://localhost:5000/api/analytics/controlled-substances`

**Response:**
```json
{
  "success": true,
  "data": {
    "total_controlled": 5,
    "total_documents": 42,
    "percentage": 11.9
  }
}
```

---

## Postman Collection Quick Reference

### Import into Postman

1. **Create a new collection** called "OCR Compliance API"
2. **Add these requests:**

#### Health Check
- **Name:** Health Check
- **Method:** GET
- **URL:** `{{base_url}}/health`

#### OCR - List Documents
- **Name:** List All Documents
- **Method:** GET
- **URL:** `{{base_url}}/ocr/documents`

#### OCR - Get Result
- **Name:** Get OCR Result
- **Method:** GET
- **URL:** `{{base_url}}/ocr/results/1`

#### OCR - Supported Languages
- **Name:** Get Supported Languages
- **Method:** GET
- **URL:** `{{base_url}}/ocr/multilingual/languages`

#### Analytics - Dashboard
- **Name:** Get Dashboard Stats
- **Method:** GET
- **URL:** `{{base_url}}/analytics/dashboard`

#### Analytics - Accuracy
- **Name:** Get Accuracy Metrics
- **Method:** GET
- **URL:** `{{base_url}}/analytics/accuracy`

#### Analytics - Trends
- **Name:** Get Compliance Trends
- **Method:** GET
- **URL:** `{{base_url}}/analytics/compliance-trends`

#### Analytics - Errors
- **Name:** Get Error Analysis
- **Method:** GET
- **URL:** `{{base_url}}/analytics/error-analysis`

#### Analytics - Controlled Substances
- **Name:** Get Controlled Substances Stats
- **Method:** GET
- **URL:** `{{base_url}}/analytics/controlled-substances`

### Set Environment Variable

In Postman, create an environment variable:
- **Variable Name:** `base_url`
- **Value:** `http://localhost:5000/api`

---

## Error Responses

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Server Error
```json
{
  "error": "Internal server error message"
}
```

### 400 Bad Request
```json
{
  "error": "Invalid request parameters"
}
```

---

## Testing Steps

1. **Start Backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Verify Health:**
   - GET `http://localhost:5000/health`
   - Should return `{"status": "healthy", ...}`

3. **Test Analytics (No data required):**
   - GET `http://localhost:5000/api/analytics/dashboard`
   - GET `http://localhost:5000/api/analytics/accuracy`
   - GET `http://localhost:5000/api/analytics/compliance-trends`
   - GET `http://localhost:5000/api/analytics/error-analysis`
   - GET `http://localhost:5000/api/analytics/controlled-substances`

4. **Test OCR (After uploading documents):**
   - GET `http://localhost:5000/api/ocr/documents` (list all)
   - GET `http://localhost:5000/api/ocr/results/1` (get specific result)
   - GET `http://localhost:5000/api/ocr/multilingual/languages` (supported languages)

---

## Notes

- All timestamps are in ISO 8601 format
- Confidence scores are decimal values (0-1)
- Processing times are in seconds
- File sizes are in bytes
- All GET endpoints return JSON responses
- No authentication required (for development)
