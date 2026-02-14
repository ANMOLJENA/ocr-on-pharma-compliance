from abc import ABC, abstractmethod
from typing import Dict, List, Any

class OCRServiceInterface(ABC):
    """Interface for OCR services"""
    
    @abstractmethod
    def extract_text(self, image_path: str) -> Dict[str, Any]:
        """
        Extract text from a single image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with 'success', 'text', and 'error' keys
        """
        pass
    
    @abstractmethod
    def extract_text_from_images(self, image_paths: List[str]) -> Dict[str, Any]:
        """
        Extract text from multiple images.
        
        Args:
            image_paths: List of paths to image files
            
        Returns:
            Dictionary with 'success', 'text', 'by_page', and 'error' keys
        """
        pass


class LanguageDetectionServiceInterface(ABC):
    """Interface for language detection services"""
    
    @abstractmethod
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the given text.
        
        Args:
            text: Text to detect language for
            
        Returns:
            Dictionary with 'success', 'language_code', 'language_name', 'confidence', and 'error' keys
        """
        pass


class TranslationServiceInterface(ABC):
    """Interface for translation services"""
    
    @abstractmethod
    def translate_to_english(self, text: str, source_language: str) -> Dict[str, Any]:
        """
        Translate text to English.
        
        Args:
            text: Text to translate
            source_language: Source language code
            
        Returns:
            Dictionary with 'success', 'translated_text', and 'error' keys
        """
        pass
    
    @abstractmethod
    def translate_pages(self, texts: List[str], source_language: str) -> Dict[str, Any]:
        """
        Translate multiple text segments.
        
        Args:
            texts: List of text segments to translate
            source_language: Source language code
            
        Returns:
            Dictionary with 'success', 'translated_texts', and 'error' keys
        """
        pass


class PDFProcessingServiceInterface(ABC):
    """Interface for PDF processing services"""
    
    @abstractmethod
    def extract_pages_as_images(self, pdf_path: str, output_dir: str) -> Dict[str, Any]:
        """
        Extract all pages from a PDF and convert them to images.
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save extracted page images
            
        Returns:
            Dictionary with 'success', 'page_count', 'image_paths', and 'error' keys
        """
        pass
    
    @abstractmethod
    def get_page_count(self, pdf_path: str) -> Dict[str, Any]:
        """
        Get the number of pages in a PDF.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with 'success', 'page_count', and 'error' keys
        """
        pass
