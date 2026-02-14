# Postman Quick Start Guide

## Setup

### 1. Import Collection
1. Open Postman
2. Click **Import** (top left)
3. Select **Upload Files**
4. Choose `postman_collection.json` from the backend folder
5. Click **Import**

### 2. Set Environment Variable
1. Click **Environments** (left sidebar)
2. Click **Create New**
3. Name it: `OCR Compliance`
4. Add variable:
   - **Variable:** `base_url`
   - **Initial Value:** `http://localhost:5000/api`
   - **Current Value:** `http://localhost:5000/api`
5. Click **Save**
6. Select this environment from the dropdown (top right)

---

## Quick Test Sequence

### Step 1: Verify Backend is Running
```
GET http://localhost:5000/health
```
Expected: `{"status": "healthy", "message": "OCR Compliance API is running"}`

### Step 2: Check Analytics (No data needed)
```
GET {{base_url}}/analytics/dashboard
GET {{base_url}}/analytics/accuracy
GET {{base_url}}/analytics/compliance-trends
GET {{base_url}}/analytics/error-analysis
GET {{base_url}}/analytics/controlled-substances
```

### Step 3: List Documents
```
GET {{base_url}}/ocr/documents
```
Returns all uploaded documents

### Step 4: Get Supported Languages
```
GET {{base_url}}/ocr/multilingual/languages
```
Returns all 20+ supported languages

### Step 5: Get Specific Result (if documents exist)
```
GET {{base_url}}/ocr/results/1
```
Replace `1` with actual result ID from documents list

---

## All GET Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check backend status |
| `/ocr/documents` | GET | List all documents |
| `/ocr/results/{id}` | GET | Get specific OCR result |
| `/ocr/multilingual/languages` | GET | Get supported languages |
| `/analytics/dashboard` | GET | Dashboard statistics |
| `/analytics/accuracy` | GET | Accuracy metrics |
| `/analytics/compliance-trends` | GET | Compliance trends |
| `/analytics/error-analysis` | GET | Error analysis |
| `/analytics/controlled-substances` | GET | Controlled substances stats |

---

## Testing Without Frontend

### Scenario 1: Test Analytics Only
1. Start backend: `cd backend && python app.py`
2. In Postman, test all analytics endpoints
3. All should return data (even if empty)

### Scenario 2: Test with Sample Data
1. Upload a document via frontend OR use POST endpoint
2. Get document ID from `/ocr/documents`
3. Get result ID from documents list
4. Test `/ocr/results/{result_id}`

### Scenario 3: Full API Test
```bash
# Terminal 1: Start backend
cd backend
python app.py

# Terminal 2: Use Postman
# Test all endpoints in sequence
```

---

## Common Issues & Solutions

### Issue: "Cannot GET /health"
**Solution:** Backend not running
```bash
cd backend
python app.py
```

### Issue: "Connection refused"
**Solution:** Backend port not accessible
- Check if port 5000 is in use
- Restart backend: `python app.py`

### Issue: Empty analytics data
**Solution:** Normal if no documents processed yet
- Upload a document via frontend first
- Or use POST `/ocr/multilingual/upload` in Postman

### Issue: Result ID not found
**Solution:** Use correct ID from documents list
1. GET `/ocr/documents` to see all IDs
2. Use actual ID in `/ocr/results/{id}`

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
    }
  }
}
```

---

## Tips

1. **Use Variables:** Replace hardcoded URLs with `{{base_url}}`
2. **Save Responses:** Click "Save Response" to compare results
3. **Test Collections:** Use "Run Collection" to test all endpoints
4. **Check Status Codes:** All GET requests should return 200
5. **Monitor Logs:** Check backend console for detailed logs

---

## Troubleshooting Checklist

- [ ] Backend running on port 5000?
- [ ] Environment variable `base_url` set correctly?
- [ ] Using correct result/document IDs?
- [ ] All GET requests returning 200 status?
- [ ] Response data matches expected format?
- [ ] No CORS errors in browser console?

---

## Next Steps

1. Test all GET endpoints
2. If all pass, frontend should work
3. If any fail, check backend logs
4. Verify database has data
5. Check API response formats match frontend expectations
