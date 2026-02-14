# cURL Commands for API Testing

## Setup
```bash
# Set base URL variable
BASE_URL="http://localhost:5000"
API_URL="http://localhost:5000/api"
```

---

## Health Check

### Check Backend Status
```bash
curl -X GET "$BASE_URL/health"
```

**Expected Response:**
```json
{"status": "healthy", "message": "OCR Compliance API is running"}
```

---

## OCR Operations

### 1. List All Documents
```bash
curl -X GET "$API_URL/ocr/documents"
```

**Expected Response:**
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
    }
  ]
}
```

---

### 2. Get OCR Result by ID
```bash
# Replace 1 with actual result ID
curl -X GET "$API_URL/ocr/results/1"
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "document_id": 1,
    "extracted_text": "...",
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

### 3. Get Supported Languages
```bash
curl -X GET "$API_URL/ocr/multilingual/languages"
```

**Expected Response:**
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

### 4. Upload Document (Multilingual)
```bash
# Replace /path/to/file with actual file path
curl -X POST "$API_URL/ocr/multilingual/upload" \
  -F "file=@/path/to/file.png"
```

**Example with actual file:**
```bash
curl -X POST "$API_URL/ocr/multilingual/upload" \
  -F "file=@backend/samples/pharma_label_french.png"
```

**Expected Response:**
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

## Analytics Operations

### 1. Get Dashboard Statistics
```bash
curl -X GET "$API_URL/analytics/dashboard"
```

**Expected Response:**
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
```bash
curl -X GET "$API_URL/analytics/accuracy"
```

**Expected Response:**
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
```bash
curl -X GET "$API_URL/analytics/compliance-trends"
```

**Expected Response:**
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
```bash
curl -X GET "$API_URL/analytics/error-analysis"
```

**Expected Response:**
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
```bash
curl -X GET "$API_URL/analytics/controlled-substances"
```

**Expected Response:**
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

## Batch Testing Script

### Test All Endpoints
```bash
#!/bin/bash

BASE_URL="http://localhost:5000"
API_URL="http://localhost:5000/api"

echo "=== Testing OCR Compliance API ==="
echo ""

echo "1. Health Check"
curl -X GET "$BASE_URL/health" | jq .
echo ""

echo "2. List Documents"
curl -X GET "$API_URL/ocr/documents" | jq .
echo ""

echo "3. Get Supported Languages"
curl -X GET "$API_URL/ocr/multilingual/languages" | jq .
echo ""

echo "4. Dashboard Statistics"
curl -X GET "$API_URL/analytics/dashboard" | jq .
echo ""

echo "5. Accuracy Metrics"
curl -X GET "$API_URL/analytics/accuracy" | jq .
echo ""

echo "6. Compliance Trends"
curl -X GET "$API_URL/analytics/compliance-trends" | jq .
echo ""

echo "7. Error Analysis"
curl -X GET "$API_URL/analytics/error-analysis" | jq .
echo ""

echo "8. Controlled Substances"
curl -X GET "$API_URL/analytics/controlled-substances" | jq .
echo ""

echo "=== All tests completed ==="
```

### Save and Run
```bash
# Save as test_api.sh
chmod +x test_api.sh
./test_api.sh
```

---

## Pretty Print JSON

### Using jq (recommended)
```bash
curl -X GET "$API_URL/ocr/documents" | jq .
```

### Using Python
```bash
curl -X GET "$API_URL/ocr/documents" | python -m json.tool
```

### Using grep and sed
```bash
curl -X GET "$API_URL/ocr/documents" | sed 's/,/,\n/g'
```

---

## Save Response to File

```bash
# Save to file
curl -X GET "$API_URL/ocr/documents" > response.json

# Pretty print and save
curl -X GET "$API_URL/ocr/documents" | jq . > response_pretty.json

# Save with timestamp
curl -X GET "$API_URL/ocr/documents" > response_$(date +%s).json
```

---

## Check Response Status Code

```bash
# Get only status code
curl -s -o /dev/null -w "%{http_code}" "$API_URL/ocr/documents"

# Get status code and response
curl -i "$API_URL/ocr/documents"

# Get headers only
curl -I "$API_URL/ocr/documents"
```

---

## Measure Response Time

```bash
# Time the request
curl -w "Time: %{time_total}s\n" -o /dev/null -s "$API_URL/ocr/documents"

# Detailed timing
curl -w "
  Time to connect: %{time_connect}s
  Time to first byte: %{time_starttransfer}s
  Total time: %{time_total}s
" -o /dev/null -s "$API_URL/ocr/documents"
```

---

## Troubleshooting

### Connection Refused
```bash
# Check if backend is running
curl -X GET "$BASE_URL/health"

# If fails, start backend
cd backend
python app.py
```

### Invalid JSON Response
```bash
# Check raw response
curl -v "$API_URL/ocr/documents"

# Check headers
curl -i "$API_URL/ocr/documents"
```

### Timeout
```bash
# Increase timeout
curl --max-time 30 "$API_URL/ocr/documents"
```

---

## Quick Reference

| Endpoint | Command |
|----------|---------|
| Health | `curl -X GET "$BASE_URL/health"` |
| Documents | `curl -X GET "$API_URL/ocr/documents"` |
| Result | `curl -X GET "$API_URL/ocr/results/1"` |
| Languages | `curl -X GET "$API_URL/ocr/multilingual/languages"` |
| Dashboard | `curl -X GET "$API_URL/analytics/dashboard"` |
| Accuracy | `curl -X GET "$API_URL/analytics/accuracy"` |
| Trends | `curl -X GET "$API_URL/analytics/compliance-trends"` |
| Errors | `curl -X GET "$API_URL/analytics/error-analysis"` |
| Controlled | `curl -X GET "$API_URL/analytics/controlled-substances"` |
