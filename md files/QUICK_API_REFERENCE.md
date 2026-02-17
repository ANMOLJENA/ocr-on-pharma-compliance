# Quick API Reference Card

## Start Backend
```bash
cd backend
python app.py
```

---

## Health Check
```bash
curl -X GET "http://localhost:5000/health"
```

---

## All GET Endpoints

| Endpoint | URL | Purpose |
|----------|-----|---------|
| Health | `GET http://localhost:5000/health` | Check backend status |
| Documents | `GET http://localhost:5000/api/ocr/documents` | List all documents |
| Result | `GET http://localhost:5000/api/ocr/results/1` | Get OCR result by ID |
| Languages | `GET http://localhost:5000/api/ocr/multilingual/languages` | Get supported languages |
| Dashboard | `GET http://localhost:5000/api/analytics/dashboard` | Dashboard stats |
| Accuracy | `GET http://localhost:5000/api/analytics/accuracy` | Accuracy metrics |
| Trends | `GET http://localhost:5000/api/analytics/compliance-trends` | Compliance trends |
| Errors | `GET http://localhost:5000/api/analytics/error-analysis` | Error analysis |
| Controlled | `GET http://localhost:5000/api/analytics/controlled-substances` | Controlled substances |

---

## Quick Test Commands

```bash
# Health
curl -X GET "http://localhost:5000/health"

# Documents
curl -X GET "http://localhost:5000/api/ocr/documents"

# Analytics
curl -X GET "http://localhost:5000/api/analytics/dashboard"
curl -X GET "http://localhost:5000/api/analytics/accuracy"
curl -X GET "http://localhost:5000/api/analytics/compliance-trends"
curl -X GET "http://localhost:5000/api/analytics/error-analysis"
curl -X GET "http://localhost:5000/api/analytics/controlled-substances"

# Languages
curl -X GET "http://localhost:5000/api/ocr/multilingual/languages"

# Get Result (replace 1 with actual ID)
curl -X GET "http://localhost:5000/api/ocr/results/1"
```

---

## Postman Setup

1. Import: `backend/postman_collection.json`
2. Create environment: `OCR Compliance`
3. Add variable: `base_url = http://localhost:5000/api`
4. Select environment and test

---

## Expected Responses

All GET endpoints should return:
- **Status Code:** 200
- **Format:** JSON
- **Structure:** `{"success": true, "data": {...}}`

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Start backend: `cd backend && python app.py` |
| 404 error | Check URL spelling and endpoint path |
| Empty data | Normal if no documents uploaded yet |
| 500 error | Check backend console for error logs |

---

## Documentation Files

- `API_TESTING_GUIDE.md` - Main guide
- `backend/API_DOCUMENTATION.md` - Full API reference
- `backend/POSTMAN_QUICK_START.md` - Postman setup
- `backend/CURL_COMMANDS.md` - cURL examples
- `backend/postman_collection.json` - Postman collection

---

## Base URLs

- Backend: `http://localhost:5000`
- API: `http://localhost:5000/api`
- Health: `http://localhost:5000/health`

---

## Key Endpoints for Frontend Testing

If frontend breaks, test these:

```bash
# 1. Backend alive?
curl -X GET "http://localhost:5000/health"

# 2. Analytics working?
curl -X GET "http://localhost:5000/api/analytics/dashboard"

# 3. OCR working?
curl -X GET "http://localhost:5000/api/ocr/documents"
```

If all return 200 with JSON, backend is fine.
