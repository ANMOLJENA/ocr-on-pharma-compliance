#!/usr/bin/env python
"""Test the full multilingual OCR pipeline"""

import requests
import os
from pathlib import Path

# Test with a French sample image
test_image = "backend/samples/pharma_label_french.png"

if not os.path.exists(test_image):
    print(f"Test image not found: {test_image}")
    print("Available samples:")
    for f in os.listdir("backend/samples"):
        print(f"  - {f}")
    exit(1)

print(f"Testing multilingual OCR with: {test_image}")
print("=" * 60)

# Upload file
with open(test_image, 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/api/ocr/multilingual/upload', files=files)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

if response.status_code == 200:
    data = response.json()
    print("\n" + "=" * 60)
    print("RESULTS:")
    print("=" * 60)
    print(f"Success: {data.get('success')}")
    print(f"Detected Language: {data.get('detected_language')}")
    print(f"Translated: {data.get('translated')}")
    print(f"\nOriginal Text (first 200 chars):")
    print(data.get('original_text', 'N/A')[:200])
    print(f"\nTranslated Text (first 200 chars):")
    print(data.get('translated_text', 'N/A')[:200])
