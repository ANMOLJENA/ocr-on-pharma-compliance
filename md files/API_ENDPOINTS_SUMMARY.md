# API Endpoints Summary - Complete Reference

## 📋 Overview

Complete list of all GET endpoints available in the OCR Compliance System API for testing in Postman or cURL.

---

## 🚀 Quick Start

### Start Backend
```bash
cd backend
python app.py
```

### Test Health
```bash
curl -X GET "http://localhost:5000/health"
```

---

## 📚 Documentation Files

| File | Location | Purpose |
|------|----------|---------|
| **API_TESTING_GUIDE.md** | Root | Main testing guide |
| **QUICK_API_REFERENCE.md** | Root | Quick reference card |
| **API_DOCUMENTATION.md** | backend/ | Full API reference |
| **POSTMAN_QUICK_START.md** | backend/ | Postman setup guide |
| **CURL_COMMANDS.md** | backend/ | cURL examples |
| **postman_collection.json** | backend/ | Ready-to-import collection |

---

## 🔗 All GET Endpoints

### 1. Health Check
```
GET http://localhost:5000/health
```
**Purpose:** Verify backend is running
**Response:** `{"status": "healthy", "message": "..."}`

---

### 2. OCR - List Documents
```
GET http://localhost:5000/api/ocr/documents
```
**Purpose:** Get all uploaded documents
**Response:** Array of documents with IDs, filenames, status

---

### 3. OCR - Get Result by ID
```
GET http://localhost:5000/api/ocr/results/{id}
```
**Example:** `GET http://localhost:5000/api/ocr/results/1`
**Purpose:** Get specific OCR result
**Response:** OCR data with extracted text, confidence, drug info

---

### 4. OCR - Get Supported Languages
```
GET http://localhost:5000/api/ocr/multilingual/languages
```
**Purpose:** Get all 20+ supported languages
**Response:** Dictionary of language codes and names

---

### 5. Analytics - Dashboard
```
GET http://localhost:5000/api/analytics/dashboard
```
**Purpose:** Get overall dashboard statistics
**Response:** Total documents, compliance rate, errors, activity

---

### 6. Analytics - Accuracy Metrics
```
GET http://localhost:5000/api/analytics/accuracy
```
**Purpose:** Get OCR accuracy metrics
**Response:** Confidence distribution, average processing time

---

### 7. Analytics - Compliance Trends
```
GET http://localhost:5000/api/analytics/compliance-trends
```
**Purpose:** Get compliance trends over time
**Response:** Daily breakdown of passed/failed/warning checks

---

### 8. Analytics - Error Analysis
```
GET http://localhost:5000/api/analytics/error-analysis
```
**Purpose:** Get error analysis
**Response:** Error types, common fields with errors

---

### 9. Analytics - Controlled Substances
```
GET http://localhost:5000/api/analytics/controlled-substances
```
**Purpose:** Get controlled substances statistics
**Response:** Total controlled, total documents, percentage

---

## 🧪 Testing Workflow

### Step 1: Verify Backend
```bash
curl -X GET "http://localhost:5000/health"
```
✅ Should return: `{"status": "healthy", ...}`

### Step 2: Test Analytics (No data needed)
```bash
curl -X GET "http://localhost:5000/api/analytics/dashboard"
curl -X GET "http://localhost:5000/api/analytics/accuracy"
curl -X GET "http://localhost:5000/api/analytics/compliance-trends"
curl -X GET "http://localhost:5000/api/analytics/error-analysis"
curl -X GET "http://localhost:5000/api/analytics/controlled-substances"
```
✅ All should return 200 with JSON data

### Step 3: List Documents
```bash
curl -X GET "http://localhost:5000/api/ocr/documents"
```
✅ Returns array of documents (may be empty)

### Step 4: Get Languages
```bash
curl -X GET "http://localhost:5000/api/ocr/multilingual/languages"
```
✅ Returns 20+ supported languages

### Step 5: Get Specific Result (if documents exist)
```bash
# Replace 1 with actual ID from step 3
curl -X GET "http://localhost:5000/api/ocr/results/1"
```
✅ Returns OCR result data

---

## 📊 Response Examples

### Health Check
```json
{
  "status": "healthy",
  "message": "OCR Compliance API is running"
}
```

### Documents List
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

### OCR Result
```json
{
  "success": true,
  "data": {
    "id": 1,
    "document_id": 1,
    "extracted_text": "...",
    "confidence_score": 0.95,
    "processing_time": 2.34,
    "drug_name": "Aspirin",
    "batch_number": "BATCH123",
    "expiry_date": "2026-12-31",
    "manufacturer": "Pharma Corp",
    "controlled_substance": false
  }
}
```

### Dashboard Stats
```json
{
  "success": true,
  "data": {
    "total_documents": 42,
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

### Supported Languages
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

## 🛠️ Using Postman

### Import Collection
1. Open Postman
2. Click **Import**
3. Select `backend/postman_collection.json`
4. Click **Import**

### Set Environment
1. Create new environment: `OCR Compliance`
2. Add variable: `base_url = http://localhost:5000/api`
3. Select environment from dropdown

### Test Endpoints
1. Start backend: `cd backend && python app.py`
2. Click any request
3. Click **Send**
4. View response

---

## 💻 Using cURL

### Basic Commands
```bash
# Health
curl -X GET "http://localhost:5000/health"

# Documents
curl -X GET "http://localhost:5000/api/ocr/documents"

# Analytics
curl -X GET "http://localhost:5000/api/analytics/dashboard"

# Pretty print (requires jq)
curl -X GET "http://localhost:5000/api/ocr/documents" | jq .
```

### Save Response
```bash
curl -X GET "http://localhost:5000/api/ocr/documents" > response.json
```

### Check Status Code
```bash
curl -s -o /dev/null -w "%{http_code}" "http://localhost:5000/api/ocr/documents"
```

---

## ✅ Testing Checklist

- [ ] Backend running on port 5000
- [ ] Health check returns 200
- [ ] All analytics endpoints return 200
- [ ] Documents list endpoint works
- [ ] Can get specific result by ID
- [ ] Languages endpoint returns 20+ languages
- [ ] All responses are valid JSON
- [ ] No 500 errors in responses
- [ ] Response times reasonable (< 5 seconds)

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Cannot GET /health" | Backend not running: `cd backend && python app.py` |
| "Connection refused" | Port 5000 in use or backend crashed |
| Empty analytics data | Normal if no documents processed yet |
| Result ID not found | Use correct ID from `/ocr/documents` |
| 500 error | Check backend console for error logs |
| Timeout | Backend processing taking too long |

---

## 🎯 Frontend Testing

If frontend breaks, verify backend with these:

```bash
# 1. Is backend alive?
curl -X GET "http://localhost:5000/health"

# 2. Are analytics working?
curl -X GET "http://localhost:5000/api/analytics/dashboard"

# 3. Is OCR working?
curl -X GET "http://localhost:5000/api/ocr/documents"
```

**If all return 200 with JSON:** Backend is working fine ✅

---

## 📍 Base URLs

| Service | URL |
|---------|-----|
| Backend | `http://localhost:5000` |
| API | `http://localhost:5000/api` |
| Health | `http://localhost:5000/health` |

---

## 📝 Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success ✅ |
| 400 | Bad Request ❌ |
| 404 | Not Found ❌ |
| 500 | Server Error ❌ |

All GET endpoints should return **200** if successful.

---

## 🚀 Next Steps

1. **Read:** `API_TESTING_GUIDE.md`
2. **Import:** `backend/postman_collection.json`
3. **Test:** All endpoints
4. **Verify:** All return 200 status
5. **Debug:** Check backend logs if any fail

---

## 📞 Support

For detailed information:
- Full API docs: `backend/API_DOCUMENTATION.md`
- Postman setup: `backend/POSTMAN_QUICK_START.md`
- cURL examples: `backend/CURL_COMMANDS.md`
- Quick reference: `QUICK_API_REFERENCE.md`

---

## ⚡ One-Liner Tests

```bash
# Test all endpoints
for endpoint in health "api/ocr/documents" "api/ocr/multilingual/languages" "api/analytics/dashboard" "api/analytics/accuracy" "api/analytics/compliance-trends" "api/analytics/error-analysis" "api/analytics/controlled-substances"; do echo "Testing $endpoint..."; curl -s -o /dev/null -w "Status: %{http_code}\n" "http://localhost:5000/$endpoint"; done
```

---

**Last Updated:** January 28, 2026
**API Version:** 1.0
**Status:** Production Ready ✅
