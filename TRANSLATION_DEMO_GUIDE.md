# OCR Translation Demo - User Guide

## 🚀 Quick Start

Your OCR Compliance System with multilingual translation is now running!

### Access the Application

- **Frontend**: http://localhost:8082/
- **Backend API**: http://localhost:5000/
- **Translation Demo Page**: http://localhost:8082/translation

## 📋 Features

### Translation Demo Page (`/translation`)

This dedicated page allows you to:

1. **Upload Documents** - Support for JPG, PNG, and PDF files (up to 10MB)
2. **Automatic Language Detection** - Detects from 40+ languages including:
   - European: English, French, German, Spanish, Italian, Portuguese, Russian, Dutch, Swedish, Polish, Turkish, Greek, Hebrew, Thai
   - Asian: Chinese, Japanese, Korean
   - Indian: Hindi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Marathi, Bengali, Punjabi, Urdu
   - Additional: Estonian

3. **Smart Translation** - Automatically translates non-English text to English using MyMemory API
4. **Side-by-Side View** - See both original and translated text simultaneously

## 🎯 How to Use

### Step 1: Navigate to Translation Demo
- Open your browser and go to: http://localhost:8082/translation
- Or click "Translation" in the navigation menu

### Step 2: Upload a Document
1. Click the upload area or drag and drop a file
2. Supported formats: JPG, PNG, PDF
3. Maximum file size: 10MB

### Step 3: Process & Translate
1. Click the "Process & Translate" button
2. Wait for the OCR and translation to complete (usually 2-5 seconds)

### Step 4: View Results
The results are displayed in three tabs:

#### **Overview Tab**
- Shows the bilingual text viewer with original and translated text side-by-side
- Language detection badge with confidence score
- Translation status indicator

#### **Text Tab**
- Original text in the detected language (amber background)
- English translation (green background)
- Easy to compare and verify translations

#### **Details Tab**
- Language information (detected language, language code, confidence)
- Translation information (status, source/target languages)
- Text statistics (character count, word count, line count)

## 🔍 Understanding the Results

### Language Detection Badge
- **Language Name**: The detected language (e.g., "Hindi", "Spanish")
- **Language Code**: ISO 639-1 code (e.g., "hi", "es")
- **Confidence Score**: Detection accuracy (0-100%)
  - 90-100%: Very confident
  - 70-89%: Confident
  - Below 70%: Less confident

### Translation Status
- **Translated**: Document was in a non-English language and has been translated
- **Not Translated**: Document was already in English or translation was not needed

### Color Coding
- **Amber/Yellow**: Original text in detected language
- **Green**: Translated English text
- **Blue**: Information and status messages

## 📊 Backend API Endpoints

If you want to integrate with the API directly:

### Get Supported Languages
```bash
GET http://localhost:5000/api/ocr/multilingual/languages
```

### Upload and Process Document
```bash
POST http://localhost:5000/api/ocr/multilingual/upload
Content-Type: multipart/form-data

file: [your file]
```

### Detect Language from File
```bash
POST http://localhost:5000/api/ocr/multilingual/detect-language
Content-Type: multipart/form-data

file: [your file]
```

## 🛠️ Technical Details

### OCR Engine
- **Tesseract OCR**: Industry-standard open-source OCR engine
- **Multi-language support**: 100+ languages
- **High accuracy**: Optimized for pharmaceutical labels

### Translation Service
- **MyMemory API**: Free translation API with no API key required
- **Smart Chunking**: Intelligently splits long text while preserving context
- **Sentence-based splitting**: Maintains meaning across chunks
- **500-character limit per chunk**: Respects API constraints
- **50-character overlap**: Ensures context preservation

### Language Detection
- **langdetect library**: Fast and accurate language detection
- **Confidence scoring**: Provides reliability metrics
- **Multi-page support**: Combines text from multiple pages for better accuracy

## 🎨 UI Components

### OCRResultsDisplay
The main results component with:
- Tabbed interface (Overview, Text, Details)
- Language detection badge
- Bilingual text viewer
- Translation status indicators
- Text statistics

### BilingualTextViewer
Side-by-side text comparison:
- Original text with language label
- Translated text with target language label
- Synchronized scrolling
- Color-coded backgrounds

### LanguageDetectionBadge
Shows language information:
- Language name and flag
- Language code
- Confidence score with visual indicator

## 🔧 Troubleshooting

### Translation Not Working
- **Issue**: HTTP 429 errors
- **Cause**: MyMemory API rate limiting
- **Solution**: Wait a few seconds between requests

### Language Detection Fails
- **Issue**: "Unknown" language detected
- **Cause**: Text too short or unclear
- **Solution**: Upload a clearer image with more text

### OCR Accuracy Issues
- **Issue**: Incorrect text extraction
- **Cause**: Poor image quality, skewed text, or low resolution
- **Solution**: 
  - Use high-resolution images (300 DPI or higher)
  - Ensure good lighting and contrast
  - Straighten skewed text before uploading

## 📝 Sample Test Files

You can test with the sample files in `backend/samples/`:
- `french.png` - French pharmaceutical label
- `pharma_label_french.png` - French prescription label
- `prescription_label_french.png` - French prescription
- `batch_record_french.png` - French batch record

## 🌐 Supported Languages (40+)

### European Languages (14)
English, French, German, Spanish, Italian, Portuguese, Russian, Dutch, Swedish, Polish, Turkish, Greek, Hebrew, Thai

### Asian Languages (3)
Chinese, Japanese, Korean

### Indian Languages (10)
Hindi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Marathi, Bengali, Punjabi, Urdu

### Additional Languages (1)
Estonian

## 📞 Support

For issues or questions:
1. Check the browser console for error messages
2. Check the backend logs in the terminal
3. Verify both servers are running
4. Ensure you have internet connection (required for translation API)

## 🎉 Enjoy!

Your multilingual OCR translation system is ready to use. Upload documents in any supported language and see instant translations!
