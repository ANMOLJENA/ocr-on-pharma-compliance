# OCR Compliance System - Backend

Flask-based backend API for pharmaceutical OCR compliance checking system.

## Features

- **OCR Processing**: Extract text from pharmaceutical documents (images and PDFs)
- **Compliance Validation**: Validate extracted data against regulatory rules
- **Error Detection**: Detect and suggest corrections for OCR errors
- **Analytics**: Track accuracy, compliance rates, and error patterns
- **Database**: SQLite database for storing documents, results, and compliance data

## Project Structure

```
backend/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── models/
│   └── database.py                 # Database models
├── services/
│   ├── ocr_service.py             # OCR processing logic
│   ├── compliance_service.py      # Compliance validation
│   └── error_detection_service.py # Error detection
├── routes/
│   ├── ocr_routes.py              # OCR API endpoints
│   ├── analytics_routes.py        # Analytics endpoints
│   └── rules_routes.py            # Rules management endpoints
└── uploads/                        # Uploaded files directory
```

## Database Schema

### Tables

1. **documents** - Uploaded document metadata
2. **ocr_results** - OCR extraction results
3. **compliance_checks** - Compliance validation results
4. **error_detections** - Detected errors and suggestions
5. **compliance_rules** - Configurable compliance rules
6. **audit_logs** - Audit trail for all operations

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your settings:
- Choose OCR service (tesseract, azure, google, aws)
- Add API keys if using cloud services
- Configure database path

### 3. Initialize Database

```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### 4. Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### OCR Operations

- `POST /api/ocr/upload` - Upload and process document
- `POST /api/ocr/process/<document_id>` - Reprocess document
- `GET /api/ocr/results/<result_id>` - Get OCR result
- `POST /api/ocr/results/<result_id>/validate` - Validate compliance
- `GET /api/ocr/results/<result_id>/errors` - Detect errors
- `GET /api/ocr/documents` - List all documents
- `DELETE /api/ocr/documents/<document_id>` - Delete document

### Analytics

- `GET /api/analytics/dashboard` - Dashboard statistics
- `GET /api/analytics/accuracy` - Accuracy metrics
- `GET /api/analytics/compliance-trends` - Compliance trends
- `GET /api/analytics/error-analysis` - Error analysis
- `GET /api/analytics/controlled-substances` - Controlled substances stats

### Rules Management

- `GET /api/rules/` - List all rules
- `GET /api/rules/<rule_id>` - Get specific rule
- `POST /api/rules/` - Create new rule
- `PUT /api/rules/<rule_id>` - Update rule
- `DELETE /api/rules/<rule_id>` - Delete rule
- `POST /api/rules/<rule_id>/toggle` - Toggle rule status

## OCR Service Integration

### Option 1: Tesseract OCR (Free, Local)

1. Install Tesseract:
   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt-get install tesseract-ocr`
   - Mac: `brew install tesseract`

2. Update `.env`:
   ```
   OCR_SERVICE=tesseract
   TESSERACT_CMD=C:/Program Files/Tesseract-OCR/tesseract.exe
   ```

3. Update `services/ocr_service.py` to use TesseractOCRService

### Option 2: Azure Computer Vision (Cloud)

1. Create Azure Computer Vision resource
2. Get endpoint and API key
3. Update `.env`:
   ```
   OCR_SERVICE=azure
   AZURE_VISION_ENDPOINT=your-endpoint
   AZURE_VISION_KEY=your-key
   ```

4. Install: `pip install azure-cognitiveservices-vision-computervision`
5. Update `services/ocr_service.py` to use AzureOCRService

### Option 3: Google Cloud Vision (Cloud)

1. Create Google Cloud project and enable Vision API
2. Download credentials JSON
3. Update `.env`:
   ```
   OCR_SERVICE=google
   GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
   ```

4. Install: `pip install google-cloud-vision`
5. Update `services/ocr_service.py` to use GoogleOCRService

### Option 4: AWS Textract (Cloud)

1. Configure AWS credentials
2. Update `.env`:
   ```
   OCR_SERVICE=aws
   AWS_ACCESS_KEY_ID=your-key
   AWS_SECRET_ACCESS_KEY=your-secret
   ```

3. Install: `pip install boto3`
4. Implement AWS Textract in `services/ocr_service.py`

## Implementing Your OCR Model

To integrate your custom OCR model:

1. Open `backend/services/ocr_service.py`
2. Modify the `OCRService` class methods:
   - `process_image()` - Add your image OCR logic
   - `process_pdf()` - Add your PDF OCR logic
3. Update `_extract_pharmaceutical_data()` to extract relevant fields
4. Adjust confidence scoring based on your model's output

Example:
```python
def process_image(self, image_path: str) -> Dict[str, Any]:
    # Your OCR model code here
    from your_model import YourOCRModel
    
    model = YourOCRModel()
    result = model.extract_text(image_path)
    
    return {
        'extracted_text': result.text,
        'confidence_score': result.confidence,
        'processing_time': result.time,
        **self._extract_pharmaceutical_data(result.text)
    }
```

## Testing

Test the API with curl or Postman:

```bash
# Upload document
curl -X POST -F "file=@document.jpg" http://localhost:5000/api/ocr/upload

# Get dashboard stats
curl http://localhost:5000/api/analytics/dashboard

# Health check
curl http://localhost:5000/health
```

## Production Deployment

1. Use PostgreSQL instead of SQLite
2. Set `FLASK_ENV=production`
3. Use a production WSGI server (gunicorn, uWSGI)
4. Enable HTTPS
5. Set strong SECRET_KEY
6. Configure proper CORS settings
7. Set up logging and monitoring

## Next Steps

1. Choose and configure your OCR service
2. Customize compliance rules in `services/compliance_service.py`
3. Add authentication/authorization
4. Implement rate limiting
5. Add comprehensive logging
6. Write unit tests
7. Set up CI/CD pipeline
