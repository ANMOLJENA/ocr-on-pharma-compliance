"""
Ollama OCR Service - OCR processing using Ollama vision models
"""

import time
import base64
import requests
import logging
from typing import Dict, Any, Optional
import os

try:
    import cv2
    import numpy as np
    from PIL import Image
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    print("Warning: OpenCV/PIL not available. Image preprocessing will be limited.")

logger = logging.getLogger(__name__)


class OllamaOCRService:
    """Service for OCR processing using Ollama vision models"""
    
    def __init__(self, ollama_endpoint: str, model_name: str, timeout: int = 30):
        """
        Initialize Ollama OCR service
        
        Args:
            ollama_endpoint: URL of Ollama server (e.g., http://localhost:11434)
            model_name: Name of the vision model to use (e.g., glm-ocr:latest)
            timeout: Request timeout in seconds (default 30)
        """
        self.ollama_endpoint = ollama_endpoint.rstrip('/')
        self.model_name = model_name
        self.timeout = timeout
        self.api_endpoint = f"{self.ollama_endpoint}/api/generate"
        
        logger.info(f"Initialized OllamaOCRService with endpoint: {self.ollama_endpoint}, model: {self.model_name}")
    
    def process_image(self, image_path: str) -> Dict[str, Any]:
        """
        Process an image and extract text using Ollama
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing OCR results
        """
        start_time = time.time()
        
        try:
            # Preprocess image for better OCR accuracy
            preprocessed_image_bytes = self._preprocess_image(image_path)
            
            # Encode to base64
            image_data = base64.b64encode(preprocessed_image_bytes).decode('utf-8')
            
            # Send to Ollama
            extracted_text = self._send_to_ollama(image_data)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence(extracted_text)
            
            processing_time = time.time() - start_time
            
            # Extract pharmaceutical information
            pharma_data = self._extract_pharmaceutical_data(extracted_text)
            
            return {
                'extracted_text': extracted_text,
                'confidence_score': confidence_score,
                'processing_time': processing_time,
                'ocr_engine': 'ollama',
                'model_name': self.model_name,
                **pharma_data
            }
            
        except Exception as e:
            logger.error(f"Ollama OCR processing failed for {image_path}: {str(e)}")
            raise Exception(f"Ollama OCR processing failed: {str(e)}")
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process a PDF document and extract text using Ollama
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing OCR results
        """
        start_time = time.time()
        
        try:
            from pdf2image import convert_from_path
            import platform
            import shutil
            
            # Determine poppler path based on OS
            poppler_path = None
            if platform.system() == 'Windows':
                poppler_path = shutil.which('poppler')
            
            # Convert PDF to images
            images = convert_from_path(pdf_path, poppler_path=poppler_path)
            
            if not images:
                raise Exception("Failed to convert PDF to images")
            
            # Process each page
            all_text = []
            confidence_scores = []
            
            for page_num, image in enumerate(images, 1):
                try:
                    # Convert PIL image to bytes
                    import io
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    image_data = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
                    
                    # Send to Ollama
                    page_text = self._send_to_ollama(image_data)
                    all_text.append(page_text)
                    
                    # Calculate confidence for this page
                    page_confidence = self._calculate_confidence(page_text)
                    confidence_scores.append(page_confidence)
                    
                except Exception as e:
                    logger.error(f"Failed to process page {page_num} of {pdf_path}: {str(e)}")
                    raise Exception(f"Failed to process page {page_num}: {str(e)}")
            
            # Combine results with page break markers
            combined_text = "\n--- Page Break ---\n".join(all_text)
            average_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            
            processing_time = time.time() - start_time
            
            # Extract pharmaceutical information from combined text
            pharma_data = self._extract_pharmaceutical_data(combined_text)
            
            return {
                'extracted_text': combined_text,
                'confidence_score': average_confidence,
                'processing_time': processing_time,
                'ocr_engine': 'ollama',
                'model_name': self.model_name,
                'pages_processed': len(images),
                **pharma_data
            }
            
        except Exception as e:
            logger.error(f"Ollama PDF processing failed for {pdf_path}: {str(e)}")
            raise Exception(f"Ollama PDF processing failed: {str(e)}")
    
    def _send_to_ollama(self, image_data: str) -> str:
        """
        Send image to Ollama for text extraction
        
        Args:
            image_data: Base64 encoded image data
            
        Returns:
            Extracted text from the image
        """
        try:
            payload = {
                "model": self.model_name,
                "prompt": "Extract all text from this image. Return only the extracted text without any explanation.",
                "images": [image_data],
                "stream": False
            }
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
            
            result = response.json()
            extracted_text = result.get('response', '').strip()
            
            if not extracted_text:
                logger.warning("Ollama returned empty response")
            
            return extracted_text
            
        except requests.Timeout:
            logger.error(f"Ollama request timeout after {self.timeout} seconds")
            raise Exception(f"Ollama request timeout after {self.timeout} seconds")
        except requests.ConnectionError as e:
            logger.error(f"Failed to connect to Ollama at {self.api_endpoint}: {str(e)}")
            raise Exception(f"Failed to connect to Ollama: {str(e)}")
        except Exception as e:
            logger.error(f"Error sending image to Ollama: {str(e)}")
            raise Exception(f"Error communicating with Ollama: {str(e)}")
    
    def _calculate_confidence(self, text: str) -> float:
        """
        Calculate confidence score for extracted text
        
        Args:
            text: Extracted text from Ollama
            
        Returns:
            Confidence score between 0 and 1
        """
        if not text or not text.strip():
            return 0.0
        
        # Simple heuristic: longer text with more alphanumeric characters suggests better confidence
        text_length = len(text.strip())
        alphanumeric_count = sum(1 for c in text if c.isalnum())
        
        # Normalize to 0-1 range
        # Assume good confidence if text is reasonably long and has good alphanumeric ratio
        if text_length == 0:
            return 0.0
        
        alphanumeric_ratio = alphanumeric_count / text_length
        
        # Base confidence on alphanumeric ratio (0.5-1.0 range)
        confidence = 0.5 + (alphanumeric_ratio * 0.5)
        
        # Clamp to 0-1 range
        return max(0.0, min(1.0, confidence))
    
    def _extract_pharmaceutical_data(self, text: str) -> Dict[str, Any]:
        """
        Extract pharmaceutical data from OCR text
        
        Args:
            text: Extracted text from OCR
            
        Returns:
            Dictionary containing pharmaceutical data
        """
        import re
        
        pharma_data = {
            'drug_name': None,
            'batch_number': None,
            'expiry_date': None,
            'manufacturer': None,
            'controlled_substance': False
        }
        
        if not text:
            return pharma_data
        
        # Extract drug name (common pharmaceutical naming patterns)
        drug_patterns = [
            r'(?:Drug|Medication|Active Ingredient):\s*([A-Za-z\s\-]+)',
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*(?:Tablet|Capsule|Injection)',
        ]
        for pattern in drug_patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                pharma_data['drug_name'] = match.group(1).strip()
                break
        
        # Extract batch number
        batch_patterns = [
            r'(?:Batch|Lot)\s*(?:No|Number|#)?:?\s*([A-Z0-9\-]+)',
            r'Batch:\s*([A-Z0-9\-]+)',
        ]
        for pattern in batch_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                pharma_data['batch_number'] = match.group(1).strip()
                break
        
        # Extract expiry date
        expiry_patterns = [
            r'(?:Expiry|Exp|Expires?)\s*(?:Date|on)?:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(?:Expiry|Exp):\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        ]
        for pattern in expiry_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                pharma_data['expiry_date'] = match.group(1).strip()
                break
        
        # Extract manufacturer
        mfg_patterns = [
            r'(?:Manufacturer|Mfg|Made by):\s*([A-Za-z\s\&\.\,]+?)(?:\n|$)',
            r'(?:Manufactured by|Mfg by):\s*([A-Za-z\s\&\.\,]+?)(?:\n|$)',
        ]
        for pattern in mfg_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                pharma_data['manufacturer'] = match.group(1).strip()
                break
        
        # Detect controlled substances
        controlled_keywords = [
            'controlled substance', 'schedule i', 'schedule ii', 'schedule iii',
            'schedule iv', 'schedule v', 'narcotic', 'opioid', 'benzodiazepine',
            'amphetamine', 'barbiturate', 'stimulant'
        ]
        text_lower = text.lower()
        for keyword in controlled_keywords:
            if keyword in text_lower:
                pharma_data['controlled_substance'] = True
                break
        
        return pharma_data
    
    def _verify_model_available(self) -> bool:
        """
        Verify that the configured model is available in Ollama
        
        Returns:
            True if model is available, False otherwise
        """
        try:
            tags_endpoint = f"{self.ollama_endpoint}/api/tags"
            response = requests.get(tags_endpoint, timeout=self.timeout)
            
            if response.status_code != 200:
                logger.warning(f"Failed to get Ollama tags: {response.status_code}")
                return False
            
            models = response.json().get('models', [])
            model_names = [m.get('name', '') for m in models]
            
            # Check if our model is in the list
            for model_name in model_names:
                if self.model_name in model_name or model_name in self.model_name:
                    logger.info(f"Model {self.model_name} is available in Ollama")
                    return True
            
            logger.warning(f"Model {self.model_name} not found in Ollama. Available models: {model_names}")
            return False
            
        except Exception as e:
            logger.error(f"Error verifying model availability: {str(e)}")
            return False
    
    def _download_model(self) -> bool:
        """
        Attempt to download the configured model
        
        Returns:
            True if download successful, False otherwise
        """
        try:
            pull_endpoint = f"{self.ollama_endpoint}/api/pull"
            payload = {"name": self.model_name}
            
            logger.info(f"Attempting to download model {self.model_name}...")
            response = requests.post(
                pull_endpoint,
                json=payload,
                timeout=300  # Longer timeout for model download
            )
            
            if response.status_code != 200:
                logger.error(f"Failed to download model: {response.status_code} - {response.text}")
                return False
            
            logger.info(f"Successfully downloaded model {self.model_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error downloading model: {str(e)}")
            return False
    
    def _preprocess_image(self, image_path: str) -> bytes:
        """
        Preprocess image for better OCR accuracy
        
        Args:
            image_path: Path to image file
            
        Returns:
            Preprocessed image as bytes
        """
        try:
            if not OPENCV_AVAILABLE:
                # If OpenCV not available, return original image
                with open(image_path, 'rb') as f:
                    return f.read()
            
            # Read image
            image = cv2.imread(image_path)
            
            if image is None:
                # Try with PIL if cv2 fails
                pil_image = Image.open(image_path)
                image = np.array(pil_image)
            
            # Preprocess the image array
            processed = self._preprocess_image_array(image)
            
            # Convert back to bytes
            import io
            _, buffer = cv2.imencode('.png', processed)
            return buffer.tobytes()
            
        except Exception as e:
            logger.warning(f"Image preprocessing failed, using original: {str(e)}")
            # Return original image if preprocessing fails
            with open(image_path, 'rb') as f:
                return f.read()
    
    def _preprocess_image_array(self, image) -> np.ndarray:
        """
        Preprocess image array for better OCR accuracy
        
        Args:
            image: Image as numpy array
            
        Returns:
            Preprocessed image array
        """
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Apply denoising
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Apply adaptive thresholding for better text contrast
            thresh = cv2.adaptiveThreshold(
                denoised, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11, 2
            )
            
            # Optional: Dilation and erosion to remove noise
            kernel = np.ones((1, 1), np.uint8)
            processed = cv2.dilate(thresh, kernel, iterations=1)
            processed = cv2.erode(processed, kernel, iterations=1)
            
            return processed
            
        except Exception as e:
            logger.warning(f"Image array preprocessing failed: {str(e)}")
            # Return original if preprocessing fails
            return image

    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get list of supported languages for Ollama OCR

        Returns:
            Dictionary of language codes and names
        """
        return {
            # European languages
            'en': 'English',
            'fr': 'French',
            'de': 'German',
            'es': 'Spanish',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'pl': 'Polish',
            'tr': 'Turkish',
            'el': 'Greek',
            'he': 'Hebrew',
            'et': 'Estonian',

            # Asian languages
            'zh': 'Chinese',
            'ja': 'Japanese',
            'ko': 'Korean',
            'th': 'Thai',

            # Indian languages
            'hi': 'Hindi',
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'gu': 'Gujarati',
            'mr': 'Marathi',
            'bn': 'Bengali',
            'pa': 'Punjabi',
            'ur': 'Urdu',
        }
