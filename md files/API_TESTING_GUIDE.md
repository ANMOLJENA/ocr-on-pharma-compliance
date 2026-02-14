# API Testing Guide - OCR Compliance System

## Overview
This guide provides all the information you need to test the OCR Compliance API using Postman, cURL, or any HTTP client.

## Files Created

1. **`backend/API_DOCUMENTATION.md`** - Complete API reference with all endpoints
2. **`backend/postman_collection.json`** - Ready-to-import Postman collection
3. **`backend/POSTMAN_QUICK_START.md`** - Step-by-step Postman setup guide
4. **`backend/CURL_COMMANDS.md`** - cURL commands for testing from terminal

---

## Quick Start

### Option 1: Using Postman (Recommended)

1. **Import Collection:**
   - Open Postman
   - Click Import → Upload Files
   - Select `backend/postman_collection.json`
   - Click Import

2. **Set Environment:**
   - Create new environment: `OCR Compliance`
   - Add variable: `base_url = http://localhost:5000/api`
   - Select environment from dropdown

3. **Test Endpoints:**
   - Start backend: `cd backend && python app.py`
   - Click any request and hit Send
   - View response in Postman

### Option 2: Using cURL

```bash
# Health check
curl -X GET "http://localhost:5000/health"

# List documents
curl -X GET "http://localhost:5000/api/ocr/documents"

# Get analytics
curl -X GET "http://localhost:5000/api/analytics/dashboard"
```

---

## All Available GET Endpoints

### Health & Status
- `GET /health` - Check backend status

### OCR Operations
- `GET /ocr/documents` - List all documents
- `GET /ocr/results/{id}` - Get specific OCR result
- `GET /ocr/multilingual/languages` - Get supported languages

### Analytics
- `GET /analytics/dashboard` - Dashboard statistics
- `GET /analytics/accuracy` - Accuracy metrics
- `GET /analytics/compliance-trends` - Compliance trends
- `GET /analytics/error-analysis` - Error analysis
- `GET /analytics/controlled-substances` - Controlled substances stats

---

## Testing Workflow

### Step 1: Verify Backend
```bash
curl -X GET "http://localhost:5000/health"
```
Expected: `{"status": "healthy", ...}`

### Step 2: Test Analytics (No data needed)
```bash
curl -X GET "http://localhost:5000/api/analytics/dashboard"
curl -X GET "http://localhost:5000/api/analytics/accuracy"
curl -X GET "http://localhost:5000/api/analytics/compliance-trends"
curl -X GET "http://localhost:5000/api/analytics/error-analysis"
curl -X GET "http://localhost:5000/api/analytics/controlled-substances"
```

### Step 3: List Documents
```bash
curl -X GET "http://localhost:5000/api/ocr/documents"
```
Returns all uploaded documents with their IDs

### Step 4: Get Specific Result
```bash
# Replace 1 with actual result ID from step 3
curl -X GET "http://localhost:5000/api/ocr/results/1"
```

### Step 5: Check Languages
```bash
curl -X GET "http://localhost:5000/api/ocr/multilingual/languages"
```

---

## Response Examples

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

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Cannot GET /health" | Backend not running: `cd backend && python app.py` |
| "Connection refused" | Port 5000 in use or backend crashed |
| Empty analytics data | Normal if no documents processed yet |
| Result ID not found | Use correct ID from `/ocr/documents` |
| CORS errors | Frontend and backend on different ports (expected) |

---

## Testing Checklist

- [ ] Backend running on port 5000
- [ ] Health check returns 200 status
- [ ] All analytics endpoints return data
- [ ] Documents list endpoint works
- [ ] Can get specific result by ID
- [ ] Languages endpoint returns 20+ languages
- [ ] All responses are valid JSON
- [ ] No 500 errors in responses

---

## Frontend Testing

If frontend breaks, use these endpoints to verify backend is working:

1. **Test Health:**
   ```bash
   curl -X GET "http://localhost:5000/health"
   ```

2. **Test Analytics:**
   ```bash
   curl -X GET "http://localhost:5000/api/analytics/dashboard"
   ```

3. **Test OCR:**
   ```bash
   curl -X GET "http://localhost:5000/api/ocr/documents"
   ```

If all return 200 with valid JSON, backend is working fine.

---

## Postman Tips

1. **Use Variables:** Replace URLs with `{{base_url}}`
2. **Save Responses:** Click "Save Response" to compare
3. **Run Collections:** Use "Run Collection" to test all at once
4. **Check Status Codes:** All GET requests should return 200
5. **View Headers:** Click "Headers" tab to see response headers
6. **Pretty Print:** Responses auto-format in Postman

---

## cURL Tips

1. **Pretty Print:** Use `| jq .` to format JSON
2. **Save Response:** Use `> filename.json` to save
3. **Check Status:** Use `-w "%{http_code}"` to see status code
4. **Measure Time:** Use `-w "Time: %{time_total}s"` for timing
5. **Verbose Mode:** Use `-v` to see all details

---

## Next Steps

1. **Import Postman Collection** (recommended)
2. **Set Environment Variable**
3. **Test All Endpoints**
4. **Verify Responses Match Documentation**
5. **If All Pass:** Frontend should work
6. **If Any Fail:** Check backend logs

---

## Support

For detailed information, see:
- `backend/API_DOCUMENTATION.md` - Full API reference
- `backend/POSTMAN_QUICK_START.md` - Postman setup
- `backend/CURL_COMMANDS.md` - cURL examples
- `backend/postman_collection.json` - Ready-to-import collection

---

## Base URLs

- **Backend:** `http://localhost:5000`
- **API:** `http://localhost:5000/api`
- **Health:** `http://localhost:5000/health`

---

## Status Codes

- **200** - Success
- **400** - Bad Request
- **404** - Not Found
- **500** - Server Error

All GET endpoints should return 200 if successful.
