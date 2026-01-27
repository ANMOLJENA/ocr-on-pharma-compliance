# Multilingual OCR Support Guide

## Overview

The OCR Compliance System now supports automatic language detection and translation to English. This feature allows you to upload pharmaceutical documents in any supported language, and the system will automatically:

1. **Detect** the language of the document
2. **Extract** text using the appropriate OCR language model
3. **Translate** the extracted text to English
4. **Validate** compliance rules on the English translation

## Supported Languages

The system supports OCR in the following languages:

| Code | Language | Code | Language |
|------|----------|------|----------|
| eng | English | ara | Arabic |
| fra | French | hin | Hindi |
| deu | German | ben | Bengali |
| spa | Spanish | nld | Dutch |
| ita | Italian | swe | Swedish |
| por | Portuguese | pol | Polish |
| rus | Russian | tur | Turkish |
| jpn | Japanese | gre | Greek |
| kor | Korean | heb | Hebrew |
| zho | Chinese | tha | Thai |

## API Endpoints

### 1. Upload with Multilingual Support

**Endpoint:** `POST /api/ocr/multilingual/upload`

Upload a document and automatically detect language, extract text, and translate to English.

**Request:**
```bash
curl -X POST http://localhost:5000/api/ocr/multilingual/upload \
  -F "file=@pharma_label_french.png"
```

**Response:**
```json
{
  "success": true,
  "document_id": 1,
  "ocr_result_id": 1,
  "detected_language": "French",
  "original_language": "French",
  "translated": true,
  "data": {
    "extracted_text": "PHARMACEUTICAL LABEL\nDrug Name: ACETAMINOPHEN 500mg\n...",
    "confidence_score": 0.92,
    "processing_time": 2.34,
    "drug_name": "ACETAMINOPHEN 500mg",
    "batch_number": "BN-2024-001234",
    "expiry_date": "12/12/2025",
    "manufacturer": "PharmaCorpInc.",
    "controlled_substance": false
  }
}
```

### 2. Process Existing Document with Multilingual Support

**Endpoint:** `POST /api/ocr/multilingual/process/<document_id>`

Process an already uploaded document with multilingual support.

**Request:**
```bash
curl -X POST http://localhost:5000/api/ocr/multilingual/process/1
```

**Response:**
```json
{
  "success": true,
  "detected_language": "French",
  "original_language": "French",
  "translated": true,
  "data": { ... }
}
```

### 3. Detect Language

**Endpoint:** `POST /api/ocr/multilingual/detect-language`

Detect the language of a document without full OCR processing.

**Request:**
```bash
curl -X POST http://localhost:5000/api/ocr/multilingual/detect-language \
  -F "file=@pharma_label_french.png"
```

**Response:**
```json
{
  "success": true,
  "detected_language_code": "fra",
  "detected_language": "French"
}
```

### 4. Get Supported Languages

**Endpoint:** `GET /api/ocr/multilingual/languages`

Get list of all supported languages for OCR.

**Request:**
```bash
curl http://localhost:5000/api/ocr/multilingual/languages
```

**Response:**
```json
{
  "success": true,
  "supported_languages": {
    "eng": "English",
    "fra": "French",
    "deu": "German",
    ...
  }
}
```

## How It Works

### Language Detection

The system uses multiple methods to detect language:

1. **Image-based Detection**: Tesseract OCR is run with multiple language models to find the best match
2. **Text-based Detection**: Uses `langdetect` library for additional accuracy
3. **Confidence Scoring**: Selects the language with the highest confidence score

### Text Extraction

Once language is detected:
- Tesseract OCR is configured with the detected language
- Text is extracted with optimized settings for that language
- Confidence scores are calculated

### Translation

The extracted text is automatically translated to English using:
- **Primary**: TextBlob (free, no API key required)
- **Fallback**: Google Cloud Translation (if configured)

### Compliance Validation

After translation to English:
- Pharmaceutical data is extracted (drug name, batch number, etc.)
- Compliance rules are applied
- Error detection runs on the English text

## Usage Examples

### Example 1: French Document

```python
from services.multilingual_ocr_service import MultilingualOCRService

service = MultilingualOCRService()

# Process French pharmaceutical label
result = service.process_image_multilingual('pharma_label_french.png')

print(f"Detected Language: {result['detected_language']}")
print(f"Original Language: {result['original_language']}")
print(f"Translated: {result['translated']}")
print(f"Extracted Text (English):\n{result['extracted_text']}")
```

### Example 2: PDF with Mixed Languages

```python
# Process PDF with automatic language detection
result = service.process_pdf_multilingual('batch_record.pdf')

# Results will be in English regardless of original language
print(result['extracted_text'])
```

### Example 3: Language Detection Only

```python
# Just detect language without full OCR
detected_lang = service._detect_language_from_image('document.png')
print(f"Language: {service.LANGUAGE_CODES[detected_lang]}")
```

## Configuration

### Translation Service

By default, the system uses TextBlob for translation. To use Google Cloud Translation:

```python
service = MultilingualOCRService(translation_service='google')
```

Requires Google Cloud credentials to be set up.

### Custom Language Support

To add support for additional languages:

1. Add language code to `LANGUAGE_CODES` dictionary
2. Ensure Tesseract has language data installed
3. Update language mapping in detection methods

## Performance Considerations

- **Language Detection**: ~1-2 seconds per image
- **OCR Processing**: ~2-5 seconds per image (varies by language)
- **Translation**: ~1-3 seconds per document
- **Total Processing Time**: ~4-10 seconds per document

## Troubleshooting

### Issue: Language Not Detected Correctly

**Solution**: 
- Ensure image quality is good
- Try uploading a clearer image
- Check if language is in supported list

### Issue: Translation Not Working

**Solution**:
- Ensure TextBlob is installed: `pip install textblob`
- Check internet connection (TextBlob requires online translation)
- Fallback to original text if translation fails

### Issue: Tesseract Language Data Missing

**Solution**:
- Install additional language data for Tesseract
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
- Linux: `sudo apt-get install tesseract-ocr-<lang>`
- macOS: `brew install tesseract-lang`

## Testing

### Test with Sample Files

Sample files in French and English are available in `backend/samples/`:

```bash
# Test French document
curl -X POST http://localhost:5000/api/ocr/multilingual/upload \
  -F "file=@backend/samples/pharma_label_french.png"

# Test English document
curl -X POST http://localhost:5000/api/ocr/multilingual/upload \
  -F "file=@backend/samples/pharma_label_1.png"
```

### Unit Tests

Run multilingual OCR tests:

```bash
python -m pytest tests/test_multilingual_ocr.py -v
```

## Future Enhancements

- [ ] Support for more languages
- [ ] Batch processing for multiple documents
- [ ] Language-specific compliance rules
- [ ] Confidence threshold configuration
- [ ] Custom translation models
- [ ] Real-time language detection UI

## Dependencies

The multilingual feature requires:

```
textblob==0.19.0      # Translation
langdetect==1.0.9     # Language detection
pytesseract==0.3.10   # OCR with language support
```

Install with:
```bash
pip install -r requirements.txt
```

## Support

For issues or questions about multilingual OCR:

1. Check this guide
2. Review API response errors
3. Check backend logs in `backend/logs/`
4. Open an issue on GitHub

---

**Last Updated**: January 2025
**Version**: 1.0.0
