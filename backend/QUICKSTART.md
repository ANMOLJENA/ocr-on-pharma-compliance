# Quick Start Guide

Get your OCR Compliance System backend running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Setup Script

```bash
python setup.py
```

This will:
- Create necessary directories
- Initialize the database
- Create default compliance rules
- Generate .env configuration file

### 5. Configure OCR Service (Optional)

Edit `.env` file to choose your OCR service:

**For Tesseract (Free, Local):**
```env
OCR_SERVICE=tesseract
TESSERACT_CMD=C:/Program Files/Tesseract-OCR/tesseract.exe
```

**For Azure Computer Vision:**
```env
OCR_SERVICE=azure
AZURE_VISION_ENDPOINT=your-endpoint
AZURE_VISION_KEY=your-api-key
```

### 6. Start the Server

```bash
python app.py
```

The API will be running at: **http://localhost:5000**

## Test the API

### Health Check

```bash
curl http://localhost:5000/health
```

### Upload a Document

```bash
curl -X POST -F "file=@your-document.jpg" http://localhost:5000/api/ocr/upload
```

### Get Dashboard Stats

```bash
curl http://localhost:5000/api/analytics/dashboard
```

## Connect to Frontend

Update your frontend API configuration to point to:
```
http://localhost:5000/api
```

## Troubleshooting

### Import Errors

If you get import errors, make sure you're in the backend directory and run:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%cd%  # Windows
```

### Database Errors

Delete the database and reinitialize:
```bash
rm ocr_compliance.db
python setup.py
```

### Port Already in Use

Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

## Next Steps

1. **Integrate OCR Model**: Edit `services/ocr_service.py` to add your OCR implementation
2. **Customize Rules**: Modify compliance rules in the database or via API
3. **Add Authentication**: Implement user authentication for production use
4. **Deploy**: Follow deployment guide for production setup

## API Documentation

Full API documentation available at: [README.md](README.md)

## Need Help?

- Check the main README.md for detailed documentation
- Review the code comments in each service file
- Test endpoints using Postman or curl
