# Ollama OCR Migration Guide

## Overview

This guide provides comprehensive instructions for deploying and configuring the Ollama OCR migration in the OCR Compliance System. The migration replaces Tesseract OCR with Ollama vision models while maintaining backward compatibility through an automatic fallback mechanism.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Deployment](#deployment)
5. [Troubleshooting](#troubleshooting)
6. [Performance Tuning](#performance-tuning)
7. [Rollback Plan](#rollback-plan)

## Prerequisites

### System Requirements

- **OS**: Windows, Linux, or macOS
- **Python**: 3.8 or higher
- **RAM**: Minimum 8GB (16GB recommended for Ollama)
- **Disk Space**: 10GB+ for Ollama models
- **GPU** (optional): NVIDIA GPU with CUDA support for faster processing

### Required Software

1. **Ollama**: Download from https://ollama.ai
2. **Tesseract OCR**: For fallback (already installed in most systems)
3. **Python Dependencies**: See requirements.txt

## Installation

### Step 1: Install Ollama

#### Windows
1. Download Ollama from https://ollama.ai/download
2. Run the installer
3. Verify installation:
   ```bash
   ollama --version
   ```

#### Linux
```bash
curl https://ollama.ai/install.sh | sh
```

#### macOS
```bash
brew install ollama
```

### Step 2: Download Vision Model

```bash
# Download llava model (recommended for OCR)
ollama pull llava:latest

# Or download a specific version
ollama pull llava:7b
ollama pull llava:13b
```

Available models:
- `llava:latest` - Latest version (recommended)
- `llava:7b` - Smaller, faster model
- `llava:13b` - Larger, more accurate model

### Step 3: Start Ollama Service

```bash
# Start Ollama server
ollama serve

# Or run in background (Linux/macOS)
ollama serve &

# Or run as service (Windows)
# Ollama runs as a service by default after installation
```

Verify Ollama is running:
```bash
curl http://localhost:11434/api/tags
```

### Step 4: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create or update `.env` file in the backend directory:

```env
# Ollama Configuration
OLLAMA_ENABLED=true
OLLAMA_ENDPOINT=http://localhost:11434
OLLAMA_MODEL=llava:latest
OLLAMA_TIMEOUT=30

# Tesseract Configuration (fallback)
TESSERACT_CMD=/usr/bin/tesseract
TESSERACT_FALLBACK=true

# Offline Mode
OFFLINE_MODE=false

# Database
DATABASE_URI=sqlite:///ocr_compliance.db

# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

### Configuration File

Update `backend/config.py` if needed:

```python
class Config:
    # Ollama settings
    OLLAMA_ENABLED = os.getenv('OLLAMA_ENABLED', 'true').lower() == 'true'
    OLLAMA_ENDPOINT = os.getenv('OLLAMA_ENDPOINT', 'http://localhost:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llava:latest')
    OLLAMA_TIMEOUT = int(os.getenv('OLLAMA_TIMEOUT', '30'))
    
    # Tesseract fallback
    TESSERACT_FALLBACK = os.getenv('TESSERACT_FALLBACK', 'true').lower() == 'true'
```

### Model Selection

Choose the appropriate model based on your needs:

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| llava:7b | 4GB | Fast | Good | Real-time processing |
| llava:13b | 8GB | Medium | Better | Balanced performance |
| llava:latest | 8GB | Medium | Best | Production (recommended) |

## Deployment

### Step 1: Verify Configuration

```bash
cd backend
python -c "from config import Config; print(f'Ollama: {Config.OLLAMA_ENABLED}, Endpoint: {Config.OLLAMA_ENDPOINT}')"
```

### Step 2: Initialize Database

```bash
python setup.py
```

### Step 3: Run Tests

```bash
# Run property-based tests
python -m pytest test_ollama_ocr_properties.py -v

# Run integration tests
python -m pytest test_ollama_integration.py -v
```

### Step 4: Start Backend Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Step 5: Verify Deployment

```bash
# Check Ollama availability
curl http://localhost:11434/api/tags

# Test OCR endpoint
curl -X POST http://localhost:5000/api/ocr/upload \
  -F "file=@test_image.png"
```

## Troubleshooting

### Ollama Connection Issues

**Problem**: "Failed to connect to Ollama at http://localhost:11434"

**Solutions**:
1. Verify Ollama is running: `ollama serve`
2. Check endpoint configuration: `OLLAMA_ENDPOINT=http://localhost:11434`
3. Verify firewall allows port 11434
4. Check if Ollama is listening: `netstat -an | grep 11434`

### Model Not Found

**Problem**: "Model llava:latest not found in Ollama"

**Solutions**:
1. Download the model: `ollama pull llava:latest`
2. List available models: `ollama list`
3. Check model name spelling in configuration

### Timeout Issues

**Problem**: "Ollama request timeout after 30 seconds"

**Solutions**:
1. Increase timeout: `OLLAMA_TIMEOUT=60`
2. Check system resources (CPU, RAM, disk)
3. Reduce image size before processing
4. Use smaller model: `OLLAMA_MODEL=llava:7b`

### Memory Issues

**Problem**: "Out of memory" or "CUDA out of memory"

**Solutions**:
1. Use smaller model: `ollama pull llava:7b`
2. Increase system RAM
3. Enable GPU acceleration if available
4. Process images sequentially instead of parallel

### Fallback Not Working

**Problem**: "Tesseract fallback not triggered"

**Solutions**:
1. Verify Tesseract is installed: `tesseract --version`
2. Check `TESSERACT_FALLBACK=true` in configuration
3. Verify `TESSERACT_CMD` points to correct binary
4. Check logs for error details

## Performance Tuning

### Optimize for Speed

```env
# Use smaller model
OLLAMA_MODEL=llava:7b

# Reduce timeout
OLLAMA_TIMEOUT=20

# Enable GPU if available
# (Ollama auto-detects NVIDIA GPUs)
```

### Optimize for Accuracy

```env
# Use larger model
OLLAMA_MODEL=llama:13b

# Increase timeout
OLLAMA_TIMEOUT=60

# Preprocess images
# (Already enabled by default)
```

### Batch Processing

For processing multiple documents:

```python
from services.ocr_service_factory import OCRServiceFactory

factory = OCRServiceFactory()

# Process multiple images
for image_path in image_paths:
    result = factory.process_image(image_path)
    # Process result
```

### Monitoring Performance

Check performance metrics:

```bash
# View processing times
SELECT 
    ocr_engine,
    AVG(processing_time) as avg_time,
    COUNT(*) as total_processed
FROM ocr_results
GROUP BY ocr_engine;
```

## Rollback Plan

### Quick Disable Ollama

If Ollama causes issues, quickly disable it:

```env
OLLAMA_ENABLED=false
```

The system will automatically use Tesseract for all processing.

### Restart Services

```bash
# Stop backend
# (Ctrl+C in terminal)

# Restart with Ollama disabled
OLLAMA_ENABLED=false python app.py
```

### Database Rollback

No database migration is required. The new fields are optional:
- `ocr_engine`: Defaults to 'tesseract'
- `fallback_used`: Defaults to False
- `model_name`: Nullable
- `metadata`: Defaults to empty JSON

### Complete Rollback

To completely remove Ollama:

1. Disable in configuration: `OLLAMA_ENABLED=false`
2. Uninstall Ollama: Follow OS-specific uninstall instructions
3. Restart backend service
4. System continues working with Tesseract

## Supported Languages

The system supports 40+ languages:

### European Languages
- English (en)
- French (fr)
- German (de)
- Spanish (es)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Dutch (nl)
- Swedish (sv)
- Polish (pl)
- Turkish (tr)
- Greek (el)
- Hebrew (he)
- Estonian (et)

### Asian Languages
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- Thai (th)

### Indian Languages
- Hindi (hi)
- Tamil (ta)
- Telugu (te)
- Kannada (kn)
- Malayalam (ml)
- Gujarati (gu)
- Marathi (mr)
- Bengali (bn)
- Punjabi (pa)
- Urdu (ur)

## API Endpoints

### Upload and Process

```bash
POST /api/ocr/upload
Content-Type: multipart/form-data

Response:
{
  "success": true,
  "document_id": 1,
  "ocr_result_id": 1,
  "data": {
    "extracted_text": "...",
    "confidence_score": 0.85,
    "processing_time": 2.5,
    "ocr_engine": "ollama",
    "fallback_used": false,
    "drug_name": "...",
    "batch_number": "...",
    "expiry_date": "...",
    "manufacturer": "...",
    "controlled_substance": false
  }
}
```

### Get Supported Languages

```bash
GET /api/ocr/multilingual/languages

Response:
{
  "success": true,
  "supported_languages": {
    "en": "English",
    "fr": "French",
    ...
  }
}
```

## Monitoring and Logging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Log Locations

- Backend logs: `backend/logs/ocr_service.log`
- Flask logs: Console output
- Database logs: Check database file

### Performance Metrics

Query performance statistics:

```sql
SELECT 
    ocr_engine,
    COUNT(*) as total,
    AVG(processing_time) as avg_time,
    MIN(processing_time) as min_time,
    MAX(processing_time) as max_time,
    AVG(confidence_score) as avg_confidence
FROM ocr_results
WHERE processed_date > datetime('now', '-7 days')
GROUP BY ocr_engine;
```

## Support and Resources

- **Ollama Documentation**: https://ollama.ai/docs
- **Vision Models**: https://ollama.ai/library
- **GitHub Issues**: Report issues on project repository
- **Community**: Join Ollama community forums

## Version History

- **v1.0.0** (2024): Initial Ollama OCR migration
  - Ollama vision model support
  - Automatic fallback to Tesseract
  - 40+ language support
  - Property-based testing
  - Comprehensive error handling
