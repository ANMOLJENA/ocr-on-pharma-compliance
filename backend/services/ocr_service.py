"""
OCR Service - Main OCR processing logic using Tesseract OCR
"""

import time
from typing import Dict, Any, Tuple
import re
import os
try:
    import pytesseract
    from PIL import Image
    import cv2
    import numpy as np
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("Warning: Tesseract dependencies not installed. Install with: pip install pytesseract pillow opencv-python")

class OCRService:
    """Service for OCR processing using Tesseract"""
    
    def __init__(self, tesseract_cmd=None):
        """
        Initialize OCR service with Tesseract
        
        Args:
            tesseract_cmd: Path to tesseract executable (optional)
        """
        if not TESSERACT_AVAILABLE:
            raise ImportError("Tesseract dependencies not installed")
        
        # Set Tesseract command path if provided
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        elif os.getenv('TESSERACT_CMD'):
            pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_CMD')
        
        # Tesseract configuration for better accuracy
        self.config = '--oem 3 --psm 6'  # LSTM OCR Engine, Assume uniform block of text
    
    def process_image(self, image_path: str) -> Dict[str, Any]:
        """
        Process an image and extract text using Tesseract OCR
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing OCR results
        """
        start_time = time.time()
        
        try:
            # Preprocess image for better OCR accuracy
            preprocessed_image = self._preprocess_image(image_path)
            
            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(
                preprocessed_image,
                config=self.config
            )
            
            # Get confidence scores
            confidence_score = self._calculate_confidence(preprocessed_image)
            
            processing_time = time.time() - start_time
            
            # Extract pharmaceutical information
            pharma_data = self._extract_pharmaceutical_data(extracted_text)
            
            return {
                'extracted_text': extracted_text,
                'confidence_score': confidence_score,
                'processing_time': processing_time,
                **pharma_data
            }
            
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process a PDF document and extract text using Tesseract
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing OCR results
        """
        start_time = time.time()
        
        try:
            from pdf2image import convert_from_path
            
            # Determine poppler path based on OS
            poppler_path = None
            import platform
            import shutil
            
            if platform.system() == 'Windows':
                # Try common Windows installation paths
                possible_paths = [
                    r'C:\Users\KIIT0001\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin',
                    r'C:\Program Files\poppler\Library\bin',
                    r'C:\Program Files (x86)\poppler\Library\bin',
                    os.getenv('POPPLER_PATH')  # Check environment variable
                ]
                for path in possible_paths:
                    if path and os.path.exists(path):
                        poppler_path = path
                        break
                
                # If still not found, try to find pdftoppm in PATH
                if not poppler_path:
                    pdftoppm_path = shutil.which('pdftoppm')
                    if pdftoppm_path:
                        poppler_path = os.path.dirname(pdftoppm_path)
            
            # Convert PDF to images
            if poppler_path:
                images = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
            else:
                images = convert_from_path(pdf_path, dpi=300)
            
            all_text = []
            total_confidence = 0
            
            # Process each page
            for i, image in enumerate(images):
                # Convert PIL Image to numpy array for preprocessing
                img_array = np.array(image)
                preprocessed = self._preprocess_image_array(img_array)
                
                # Extract text
                page_text = pytesseract.image_to_string(
                    preprocessed,
                    config=self.config
                )
                all_text.append(page_text)
                
                # Calculate confidence for this page
                page_confidence = self._calculate_confidence(preprocessed)
                total_confidence += page_confidence
            
            # Combine all pages
            extracted_text = "\n\n--- Page Break ---\n\n".join(all_text)
            confidence_score = total_confidence / len(images) if images else 0
            
            processing_time = time.time() - start_time
            
            pharma_data = self._extract_pharmaceutical_data(extracted_text)
            
            return {
                'extracted_text': extracted_text,
                'confidence_score': confidence_score,
                'processing_time': processing_time,
                **pharma_data
            }
            
        except ImportError:
            raise Exception("pdf2image not installed. Install with: pip install pdf2image")
        except Exception as e:
            error_msg = str(e)
            if "poppler" in error_msg.lower():
                raise Exception(
                    "PDF processing failed: Poppler is required for PDF processing. "
                    "Please install Poppler:\n"
                    "Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases\n"
                    "Linux: sudo apt-get install poppler-utils\n"
                    "macOS: brew install poppler\n"
                    "Or try uploading an image (PNG/JPG) instead."
                )
            raise Exception(f"PDF processing failed: {error_msg}")
    
    def _preprocess_image(self, image_path: str):
        """
        Preprocess image for better OCR accuracy
        
        Args:
            image_path: Path to image file
            
        Returns:
            Preprocessed image
        """
        # Read image
        image = cv2.imread(image_path)
        
        if image is None:
            # Try with PIL if cv2 fails
            pil_image = Image.open(image_path)
            image = np.array(pil_image)
        
        return self._preprocess_image_array(image)
    
    def _preprocess_image_array(self, image):
        """
        Preprocess image array for better OCR accuracy
        
        Args:
            image: Image as numpy array
            
        Returns:
            Preprocessed image
        """
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
    
    def _calculate_confidence(self, image) -> float:
        """
        Calculate OCR confidence score
        
        Args:
            image: Preprocessed image
            
        Returns:
            Confidence score (0-1)
        """
        try:
            # Get detailed OCR data with confidence scores
            data = pytesseract.image_to_data(
                image,
                config=self.config,
                output_type=pytesseract.Output.DICT
            )
            
            # Calculate average confidence for words with confidence > 0
            confidences = [
                int(conf) for conf in data['conf']
                if conf != '-1' and int(conf) > 0
            ]
            
            if confidences:
                avg_confidence = sum(confidences) / len(confidences)
                return avg_confidence / 100.0  # Convert to 0-1 scale
            
            return 0.5  # Default confidence if no data
            
        except Exception:
            return 0.5  # Default confidence on error
    
    def _mock_ocr_extraction(self, file_path: str) -> str:
        """Mock OCR extraction for testing purposes (fallback)"""
        return """
        PHARMACEUTICAL LABEL
        
        Drug Name: ACETAMINOPHEN 500mg
        Batch Number: BN-2024-001234
        Expiry Date: 12/2025
        Manufacturer: PharmaCorp Inc.
        
        CONTROLLED SUBSTANCE: Schedule II
        
        Storage: Store at room temperature
        Dosage: Take 1-2 tablets every 4-6 hours
        """
    
    def _extract_pharmaceutical_data(self, text: str) -> Dict[str, Any]:
        """
        Extract pharmaceutical-specific information from OCR text
        
        Args:
            text: Extracted text from OCR
            
        Returns:
            Dictionary with pharmaceutical data
        """
        data = {
            'drug_name': None,
            'batch_number': None,
            'expiry_date': None,
            'manufacturer': None,
            'controlled_substance': False
        }
        
        # Extract drug name
        drug_match = re.search(r'Drug Name:\s*([^\n]+)', text, re.IGNORECASE)
        if drug_match:
            data['drug_name'] = drug_match.group(1).strip()
        
        # Extract batch number
        batch_match = re.search(r'Batch Number:\s*([^\n]+)', text, re.IGNORECASE)
        if batch_match:
            data['batch_number'] = batch_match.group(1).strip()
        
        # Extract expiry date
        expiry_match = re.search(r'Expiry Date:\s*([^\n]+)', text, re.IGNORECASE)
        if expiry_match:
            data['expiry_date'] = expiry_match.group(1).strip()
        
        # Extract manufacturer
        mfr_match = re.search(r'Manufacturer:\s*([^\n]+)', text, re.IGNORECASE)
        if mfr_match:
            data['manufacturer'] = mfr_match.group(1).strip()
        
        # Check for controlled substance
        if re.search(r'controlled\s+substance|schedule\s+[I-V]+', text, re.IGNORECASE):
            data['controlled_substance'] = True
        
        return data
    
    def validate_text_quality(self, text: str, confidence: float) -> Tuple[bool, str]:
        """
        Validate the quality of extracted text
        
        Args:
            text: Extracted text
            confidence: OCR confidence score
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not text or len(text.strip()) < 10:
            return False, "Extracted text is too short or empty"
        
        if confidence < 0.7:
            return False, f"Low confidence score: {confidence:.2f}"
        
        return True, "Text quality is acceptable"


class TesseractOCRService(OCRService):
    """Tesseract OCR implementation with advanced features"""
    
    def __init__(self, tesseract_cmd: str = None, lang: str = 'eng'):
        """
        Initialize Tesseract OCR service
        
        Args:
            tesseract_cmd: Path to tesseract executable
            lang: Language code (default: 'eng' for English)
        """
        super().__init__(tesseract_cmd)
        self.lang = lang
        # Enhanced config for pharmaceutical documents
        self.config = f'--oem 3 --psm 6 -l {lang}'
    
    def process_with_layout_analysis(self, image_path: str) -> Dict[str, Any]:
        """
        Process image with layout analysis for structured documents
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with OCR results and layout information
        """
        try:
            preprocessed = self._preprocess_image(image_path)
            
            # Get detailed layout information
            data = pytesseract.image_to_data(
                preprocessed,
                config=self.config,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract structured data
            structured_data = self._extract_structured_data(data)
            
            # Get full text
            full_text = pytesseract.image_to_string(preprocessed, config=self.config)
            
            return {
                'extracted_text': full_text,
                'structured_data': structured_data,
                'confidence_score': self._calculate_confidence(preprocessed),
                **self._extract_pharmaceutical_data(full_text)
            }
            
        except Exception as e:
            raise Exception(f"Layout analysis failed: {str(e)}")
    
    def _extract_structured_data(self, ocr_data: Dict) -> Dict[str, Any]:
        """
        Extract structured data from OCR output
        
        Args:
            ocr_data: Tesseract output dictionary
            
        Returns:
            Structured data with bounding boxes and confidence
        """
        structured = {
            'blocks': [],
            'lines': [],
            'words': []
        }
        
        n_boxes = len(ocr_data['text'])
        for i in range(n_boxes):
            if int(ocr_data['conf'][i]) > 0:
                word_data = {
                    'text': ocr_data['text'][i],
                    'confidence': int(ocr_data['conf'][i]),
                    'bbox': {
                        'x': ocr_data['left'][i],
                        'y': ocr_data['top'][i],
                        'width': ocr_data['width'][i],
                        'height': ocr_data['height'][i]
                    }
                }
                structured['words'].append(word_data)
        
        return structured


class AzureOCRService(OCRService):
    """Azure Computer Vision OCR implementation"""
    
    def __init__(self, endpoint: str, api_key: str):
        super().__init__()
        # TODO: Initialize Azure Computer Vision client
        # from azure.cognitiveservices.vision.computervision import ComputerVisionClient
        # from msrest.authentication import CognitiveServicesCredentials
        # self.client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(api_key))
        pass


class GoogleOCRService(OCRService):
    """Google Cloud Vision OCR implementation"""
    
    def __init__(self, credentials_path: str):
        super().__init__()
        # TODO: Initialize Google Cloud Vision client
        # from google.cloud import vision
        # self.client = vision.ImageAnnotatorClient.from_service_account_json(credentials_path)
        pass
