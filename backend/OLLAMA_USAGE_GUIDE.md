# Ollama Usage Guide - Text Extraction from Images

## Quick Start

### Prerequisites
1. Ollama installed and running (`ollama serve`)
2. Model downloaded (`ollama pull llava:latest`)
3. Python with requests library installed

### Method 1: Using the Test Script (Easiest)

```bash
cd backend
python test_ollama_extract.py
```

This will:
- Load `samples/sampleocr.jpeg`
- Send it to Ollama for text extraction
- Display the extracted text
- Save results to `extracted_text.txt`

---

## Method 2: Using Python Directly

### Simple Example

```python
import base64
import requests

# Configuration
OLLAMA_ENDPOINT = "http://localhost:11434"
MODEL_NAME = "llava:latest"
IMAGE_PATH = "samples/sampleocr.jpeg"

# Read and encode image
with open(IMAGE_PATH, 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

# Prepare request
payload = {
    "model": MODEL_NAME,
    "prompt": "Extract all text from this image.",
    "images": [image_data],
    "stream": False
}

# Send to Ollama
response = requests.post(
    f"{OLLAMA_ENDPOINT}/api/generate",
    json=payload,
    timeout=60
)

# Get result
result = response.json()
extracted_text = result.get('response', '')
print(extracted_text)
```

---

## Method 3: Using the Web UI

1. Open http://localhost:8080 in your browser
2. Click "Upload Document"
3. Select `samples/sampleocr.jpeg`
4. Click "Upload & Process"
5. View extracted text in results

---

## Method 4: Using cURL (Command Line)

### Step 1: Encode the image to base64

**Windows (PowerShell):**
```powershell
$imageBytes = [System.IO.File]::ReadAllBytes("backend/samples/sampleocr.jpeg")
$base64String = [System.Convert]::ToBase64String($imageBytes)
$base64String | Out-File -FilePath "image_base64.txt"
```

**Linux/Mac:**
```bash
base64 backend/samples/sampleocr.jpeg > image_base64.txt
```

### Step 2: Create JSON request

Create a file `ocr_request.json`:
```json
{
  "model": "llava:latest",
  "prompt": "Extract all text from this image.",
  "images": ["<BASE64_IMAGE_DATA_HERE>"],
  "stream": false
}
```

Replace `<BASE64_IMAGE_DATA_HERE>` with the content from `image_base64.txt`

### Step 3: Send request

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d @ocr_request.json
```

---

## Understanding the Response

### Successful Response

```json
{
  "model": "llava:latest",
  "created_at": "2024-02-15T10:30:00Z",
  "response": "Drug Name: Aspirin 500mg\nBatch Number: BN-2024-001234\nExpiry Date: 12/2025\nManufacturer: PharmaCorp Inc.",
  "done": true,
  "total_duration": 2500000000,
  "load_duration": 500000000,
  "prompt_eval_count": 50,
  "prompt_eval_duration": 1000000000,
  "eval_count": 100,
  "eval_duration": 1000000000
}
```

**Key Fields:**
- `response`: The extracted text
- `done`: Whether processing is complete
- `total_duration`: Total time in nanoseconds

### Error Response

```json
{
  "error": "Failed to connect to Ollama"
}
```

---

## Troubleshooting

### Issue: "Failed to connect to Ollama"

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve
```

### Issue: "Model not found"

**Solution:**
```bash
# Download the model
ollama pull llava:latest

# Verify it's installed
ollama list
```

### Issue: "Request timed out"

**Solution:**
- Increase timeout in code (default 60 seconds)
- Check system resources (CPU, RAM)
- Try with a smaller image
- Use a faster model: `ollama pull llava:7b`

### Issue: "No text extracted"

**Possible causes:**
- Image quality too poor
- Image doesn't contain text
- Model not suitable for the image type

**Solution:**
- Try with a different image
- Improve image quality (brightness, contrast)
- Use a different model

---

## Available Models

### Recommended for OCR

| Model | Size | Speed | Accuracy | Command |
|-------|------|-------|----------|---------|
| llava:latest | 8GB | Medium | Best | `ollama pull llava:latest` |
| llava:13b | 8GB | Medium | Better | `ollama pull llava:13b` |
| llava:7b | 4GB | Fast | Good | `ollama pull llava:7b` |

### List installed models

```bash
ollama list
```

### Switch models

Update `OLLAMA_MODEL` in your code:
```python
MODEL_NAME = "llava:7b"  # or "llava:13b"
```

---

## Advanced Usage

### Extract Text with Custom Prompt

```python
payload = {
    "model": "llava:latest",
    "prompt": "Extract only the drug name and batch number from this pharmaceutical label.",
    "images": [image_data],
    "stream": False
}
```

### Process Multiple Images

```python
for image_path in image_paths:
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    payload = {
        "model": "llava:latest",
        "prompt": "Extract all text from this image.",
        "images": [image_data],
        "stream": False
    }
    
    response = requests.post(
        f"{OLLAMA_ENDPOINT}/api/generate",
        json=payload,
        timeout=60
    )
    
    result = response.json()
    print(result.get('response', ''))
```

### Stream Response (for large documents)

```python
payload = {
    "model": "llava:latest",
    "prompt": "Extract all text from this image.",
    "images": [image_data],
    "stream": True  # Enable streaming
}

response = requests.post(
    f"{OLLAMA_ENDPOINT}/api/generate",
    json=payload,
    stream=True
)

# Process streaming response
for line in response.iter_lines():
    if line:
        data = json.loads(line)
        print(data.get('response', ''), end='', flush=True)
```

---

## Performance Tips

1. **Use appropriate model size:**
   - Fast processing: `llava:7b`
   - Balanced: `llava:latest`
   - Best accuracy: `llava:13b`

2. **Optimize images:**
   - Resize large images
   - Improve contrast and brightness
   - Remove unnecessary background

3. **Batch processing:**
   - Process multiple images sequentially
   - Don't overwhelm system resources

4. **Monitor resources:**
   - Check CPU and RAM usage
   - Adjust timeout based on system performance

---

## Integration with Web UI

The web UI automatically uses Ollama for OCR:

1. Upload image via web interface
2. Backend sends to Ollama
3. Results displayed in UI
4. Data stored in database

No additional configuration needed!

---

## API Endpoints

### Ollama Endpoints

- `GET /api/tags` - List available models
- `POST /api/generate` - Generate text from image
- `POST /api/pull` - Download a model
- `DELETE /api/delete` - Delete a model

### Our Backend Endpoints

- `POST /api/ocr/upload` - Upload and process document
- `GET /api/ocr/multilingual/languages` - Get supported languages
- `GET /api/ocr/results/<id>` - Get OCR result

---

## Next Steps

1. ✅ Run `python test_ollama_extract.py` to test extraction
2. ✅ Upload images via web UI
3. ✅ Check extracted text in results
4. ✅ Validate pharmaceutical data extraction
5. ✅ Monitor performance metrics

---

## Support

For issues:
1. Check Ollama is running: `ollama serve`
2. Verify model is installed: `ollama list`
3. Check logs in `backend/logs/`
4. Review error messages in web UI

