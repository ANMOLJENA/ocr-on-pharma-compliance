# 🚀 Quick Reference Card

## One-Page Guide to Your OCR Compliance System

---

## 📦 What You Have

✅ **Frontend**: React + TypeScript + Vite (Port 8082)
✅ **Backend**: Flask + Tesseract OCR (Port 5000)
✅ **Database**: SQLite with 6 tables
✅ **Features**: OCR, Compliance, Error Detection, Analytics

---

## ⚡ Quick Start Commands

### Frontend (Already Running)
```bash
npm run dev              # Start dev server
npm run build            # Build for production
npm run lint             # Check code quality
```

### Backend (3 Commands)
```bash
cd backend
pip install -r requirements.txt    # Install dependencies
python setup.py                    # Setup database
python app.py                      # Start server
```

**Or use shortcuts:**
- Windows: `backend\start_server.bat`
- Linux/Mac: `backend/start_server.sh`

---

## 🔧 Tesseract Installation

### Windows
Download: https://github.com/UB-Mannheim/tesseract/wiki
Install to: `C:\Program Files\Tesseract-OCR`

### Linux
```bash
sudo apt install tesseract-ocr
```

### macOS
```bash
brew install tesseract
```

### Verify
```bash
tesseract --version
python backend/test_tesseract.py
```

---

## 🔌 API Endpoints (Port 5000)

### Upload & Process
```bash
POST /api/ocr/upload
curl -X POST -F "file=@image.jpg" http://localhost:5000/api/ocr/upload
```

### Get Results
```bash
GET /api/ocr/results/<id>
curl http://localhost:5000/api/ocr/results/1
```

### Validate Compliance
```bash
POST /api/ocr/results/<id>/validate
curl -X POST http://localhost:5000/api/ocr/results/1/validate
```

### Dashboard Stats
```bash
GET /api/analytics/dashboard
curl http://localhost:5000/api/analytics/dashboard
```

---

## 📊 Database Tables

1. **documents** - Uploaded files
2. **ocr_results** - Extracted text + pharma data
3. **compliance_checks** - Validation results
4. **error_detections** - Detected errors
5. **compliance_rules** - Validation rules
6. **audit_logs** - Activity log

---

## 🎯 Key Files

### Backend
```
backend/
├── app.py                    # Main Flask app
├── services/ocr_service.py   # Tesseract OCR
├── models/database.py        # Database schema
├── routes/ocr_routes.py      # API endpoints
├── test_tesseract.py         # Test script
└── .env                      # Configuration
```

### Frontend
```
src/
├── App.tsx                   # Main component
├── pages/                    # Page components
├── components/               # UI components
└── main.tsx                  # Entry point
```

---

## ⚙️ Configuration (.env)

```env
# Backend configuration
OCR_SERVICE=tesseract
TESSERACT_CMD=C:/Program Files/Tesseract-OCR/tesseract.exe
DATABASE_URI=sqlite:///ocr_compliance.db
UPLOAD_FOLDER=uploads
```

---

## 🧪 Testing

### Test Tesseract Setup
```bash
cd backend
python test_tesseract.py
```

### Test API
```bash
curl http://localhost:5000/health
```

### Run Examples
```bash
cd backend
python example_usage.py
```

---

## 🎨 OCR Configuration

Edit `backend/services/ocr_service.py`:

```python
# Basic (default)
self.config = '--oem 3 --psm 6'

# Better accuracy
self.config = '--oem 1 --psm 6 -c preserve_interword_spaces=1'

# Numbers only
self.config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
```

---

## 📈 Extracted Data

From pharmaceutical documents:
- ✅ Drug name
- ✅ Batch number
- ✅ Expiry date
- ✅ Manufacturer
- ✅ Controlled substance status
- ✅ Full text with confidence score

---

## 🔍 Compliance Checks

Default rules:
1. Drug name required
2. Batch number format
3. Expiry date required
4. Manufacturer info
5. Controlled substance marking
6. Dosage information
7. Storage instructions

---

## 🐛 Common Issues

### "tesseract not found"
```bash
# Set in .env
TESSERACT_CMD=C:/Program Files/Tesseract-OCR/tesseract.exe
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Database error"
```bash
rm ocr_compliance.db
python setup.py
```

### Low accuracy
- Use 300+ DPI images
- Good lighting
- PNG/TIFF format
- Adjust PSM mode

---

## 📚 Documentation

- **Complete Guide**: `BACKEND_COMPLETE.md`
- **Project Summary**: `PROJECT_SUMMARY.md`
- **API Docs**: `backend/README.md`
- **Quick Start**: `backend/QUICKSTART.md`
- **Tesseract Setup**: `backend/TESSERACT_SETUP.md`

---

## 🚦 Startup Checklist

- [ ] Tesseract installed
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Database setup (`python setup.py`)
- [ ] Test passed (`python test_tesseract.py`)
- [ ] Backend running (`python app.py`)
- [ ] Frontend running (`npm run dev`)
- [ ] Upload test document
- [ ] Check results

---

## 🎯 URLs

- **Frontend**: http://localhost:8082
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **API Base**: http://localhost:5000/api

---

## 💡 Pro Tips

1. **Better OCR**: Use high-res images (300+ DPI)
2. **Faster Processing**: Reduce image size first
3. **Custom Rules**: Add via `/api/rules/` endpoint
4. **Batch Process**: Use `example_usage.py` as template
5. **Monitor**: Check `/api/analytics/dashboard`

---

## 🆘 Need Help?

1. Run test script: `python test_tesseract.py`
2. Check logs in terminal
3. Review documentation files
4. Test with sample images first

---

## ✅ Success Indicators

✓ `tesseract --version` works
✓ `python test_tesseract.py` passes
✓ Backend starts without errors
✓ Frontend loads at localhost:8082
✓ Can upload and process images
✓ OCR results appear with confidence scores

---

**You're ready to process pharmaceutical documents! 🎉**

Start both servers and upload your first document!
