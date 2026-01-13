# Tesseract OCR Setup Guide

Complete guide to install and configure Tesseract OCR for the pharmaceutical compliance system.

## What is Tesseract?

Tesseract is a free, open-source OCR engine developed by Google. It's highly accurate and supports 100+ languages.

## Installation

### Windows

1. **Download Tesseract Installer**
   - Visit: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the latest installer (e.g., `tesseract-ocr-w64-setup-5.3.3.exe`)

2. **Run Installer**
   - Double-click the downloaded file
   - **Important**: Note the installation path (default: `C:\Program Files\Tesseract-OCR`)
   - Check "Add to PATH" option if available

3. **Verify Installation**
   ```cmd
   tesseract --version
   ```

4. **Update .env File**
   ```env
   OCR_SERVICE=tesseract
   TESSERACT_CMD=C:/Program Files/Tesseract-OCR/tesseract.exe
   ```

### Linux (Ubuntu/Debian)

1. **Install via apt**
   ```bash
   sudo apt update
   sudo apt install tesseract-ocr
   sudo apt install libtesseract-dev
   ```

2. **Verify Installation**
   ```bash
   tesseract --version
   ```

3. **Update .env File**
   ```env
   OCR_SERVICE=tesseract
   TESSERACT_CMD=/usr/bin/tesseract
   ```

### macOS

1. **Install via Homebrew**
   ```bash
   brew install tesseract
   ```

2. **Verify Installation**
   ```bash
   tesseract --version
   ```

3. **Update .env File**
   ```env
   OCR_SERVICE=tesseract
   TESSERACT_CMD=/usr/local/bin/tesseract
   ```

## Python Dependencies

Install required Python packages:

```bash
pip install pytesseract==0.3.10
pip install Pillow==10.1.0
pip install opencv-python==4.8.1.78
pip install pdf2image==1.16.3
```

Or install all at once:
```bash
pip install -r requirements.txt
```

## Additional Setup for PDF Processing

### Windows

1. **Install Poppler** (required for pdf2image)
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases
   - Extract to `C:\Program Files\poppler`
   - Add to PATH: `C:\Program Files\poppler\Library\bin`

2. **Verify**
   ```cmd
   pdftoppm -v
   ```

### Linux

```bash
sudo apt install poppler-utils
```

### macOS

```bash
brew install poppler
```

## Language Data (Optional)

For better accuracy with specific languages:

### Download Additional Languages

1. Visit: https://github.com/tesseract-ocr/tessdata
2. Download language files (e.g., `eng.traineddata` for English)
3. Place in Tesseract's `tessdata` directory:
   - Windows: `C:\Program Files\Tesseract-OCR\tessdata`
   - Linux: `/usr/share/tesseract-ocr/5/tessdata`
   - macOS: `/usr/local/share/tessdata`

### Use Multiple Languages

Update your code:
```python
ocr_service = TesseractOCRService(lang='eng+fra')  # English + French
```

## Configuration

### Basic Configuration (.env)

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URI=sqlite:///ocr_compliance.db

# OCR Service
OCR_SERVICE=tesseract
TESSERACT_CMD=C:/Program Files/Tesseract-OCR/tesseract.exe

# Upload Settings
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Advanced Tesseract Configuration

Edit `services/ocr_service.py` to customize:

```python
# Page Segmentation Modes (PSM)
# 0 = Orientation and script detection only
# 1 = Automatic page segmentation with OSD
# 3 = Fully automatic page segmentation (default)
# 6 = Assume a single uniform block of text
# 11 = Sparse text. Find as much text as possible

self.config = '--oem 3 --psm 6'  # LSTM engine, uniform block

# For pharmaceutical labels (structured text)
self.config = '--oem 3 --psm 6 -c preserve_interword_spaces=1'

# For better number recognition
self.config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
```

## Testing Your Setup

### 1. Test Tesseract Directly

Create a test image and run:

```bash
tesseract test_image.jpg output
cat output.txt
```

### 2. Test Python Integration

Create `test_ocr.py`:

```python
import pytesseract
from PIL import Image

# Set Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Test OCR
image = Image.open('test_image.jpg')
text = pytesseract.image_to_string(image)
print(text)
```

Run:
```bash
python test_ocr.py
```

### 3. Test Backend API

Start the server:
```bash
python app.py
```

Upload a test document:
```bash
curl -X POST -F "file=@test_pharmaceutical_label.jpg" http://localhost:5000/api/ocr/upload
```

## Optimizing for Pharmaceutical Documents

### Image Preprocessing

The service includes automatic preprocessing:
- **Grayscale conversion**: Removes color noise
- **Denoising**: Reduces image artifacts
- **Adaptive thresholding**: Enhances text contrast
- **Morphological operations**: Cleans up text edges

### Tips for Better Accuracy

1. **Image Quality**
   - Use high-resolution images (300 DPI minimum)
   - Ensure good lighting and contrast
   - Avoid shadows and glare

2. **Image Format**
   - PNG or TIFF for best quality
   - JPEG is acceptable but may have compression artifacts

3. **Text Orientation**
   - Ensure text is horizontal
   - Use deskewing if needed

4. **Custom Training** (Advanced)
   - Train Tesseract on pharmaceutical-specific fonts
   - Create custom language data for medical terminology

## Troubleshooting

### Error: "tesseract is not installed"

**Solution**: Install Tesseract and add to PATH

### Error: "Failed to load language data"

**Solution**: 
- Check tessdata directory exists
- Verify language files are present
- Set TESSDATA_PREFIX environment variable

### Low Accuracy

**Solutions**:
1. Improve image quality
2. Adjust PSM mode
3. Use preprocessing
4. Train custom model

### PDF Processing Fails

**Solution**: Install poppler-utils (see PDF setup above)

### Import Error: "No module named 'cv2'"

**Solution**: 
```bash
pip install opencv-python
```

## Performance Optimization

### For Faster Processing

1. **Reduce Image Size**
   ```python
   image = image.resize((width//2, height//2))
   ```

2. **Use Faster PSM Mode**
   ```python
   self.config = '--oem 3 --psm 3'  # Faster but less accurate
   ```

3. **Process in Parallel**
   ```python
   from concurrent.futures import ThreadPoolExecutor
   ```

### For Better Accuracy

1. **Increase DPI**
   ```python
   images = convert_from_path(pdf_path, dpi=600)
   ```

2. **Use Best OCR Engine**
   ```python
   self.config = '--oem 1 --psm 6'  # LSTM only
   ```

3. **Apply More Preprocessing**
   - Sharpen images
   - Remove noise
   - Enhance contrast

## Example Usage

### Basic OCR

```python
from services.ocr_service import OCRService

ocr = OCRService()
result = ocr.process_image('pharmaceutical_label.jpg')

print(f"Text: {result['extracted_text']}")
print(f"Confidence: {result['confidence_score']}")
print(f"Drug: {result['drug_name']}")
```

### Advanced OCR with Layout

```python
from services.ocr_service import TesseractOCRService

ocr = TesseractOCRService(lang='eng')
result = ocr.process_with_layout_analysis('label.jpg')

print(f"Structured data: {result['structured_data']}")
```

## Next Steps

1. ✅ Install Tesseract
2. ✅ Install Python dependencies
3. ✅ Configure .env file
4. ✅ Test with sample images
5. ✅ Integrate with your frontend
6. 🔄 Fine-tune for your specific documents
7. 🔄 Train custom model (optional)

## Resources

- **Tesseract Documentation**: https://tesseract-ocr.github.io/
- **pytesseract GitHub**: https://github.com/madmaze/pytesseract
- **Training Tesseract**: https://tesseract-ocr.github.io/tessdoc/Training-Tesseract.html
- **Language Data**: https://github.com/tesseract-ocr/tessdata

## Support

If you encounter issues:
1. Check Tesseract version: `tesseract --version`
2. Verify Python packages: `pip list | grep tesseract`
3. Test with simple image first
4. Check logs in `logs/` directory
