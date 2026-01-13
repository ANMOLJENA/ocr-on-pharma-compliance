"""
Error Detection Service - Detects and suggests corrections for OCR errors
"""

import re
from typing import List, Dict, Any
from difflib import SequenceMatcher

class ErrorDetectionService:
    """Service for detecting errors in OCR results"""
    
    def __init__(self):
        self.common_drugs = self._load_drug_database()
        self.common_errors = self._load_common_ocr_errors()
    
    def _load_drug_database(self) -> List[str]:
        """Load common pharmaceutical drug names"""
        return [
            'ACETAMINOPHEN', 'IBUPROFEN', 'ASPIRIN', 'AMOXICILLIN',
            'LISINOPRIL', 'METFORMIN', 'ATORVASTATIN', 'SIMVASTATIN',
            'OMEPRAZOLE', 'AMLODIPINE', 'METOPROLOL', 'LOSARTAN',
            'ALBUTEROL', 'GABAPENTIN', 'HYDROCHLOROTHIAZIDE', 'SERTRALINE'
        ]
    
    def _load_common_ocr_errors(self) -> Dict[str, str]:
        """Load common OCR character misrecognitions"""
        return {
            '0': 'O',  # Zero vs letter O
            'O': '0',
            '1': 'I',  # One vs letter I
            'I': '1',
            '5': 'S',
            'S': '5',
            '8': 'B',
            'B': '8'
        }
    
    def detect_errors(self, ocr_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect potential errors in OCR results
        
        Args:
            ocr_data: Dictionary containing OCR results
            
        Returns:
            List of detected errors with suggestions
        """
        errors = []
        
        # Check drug name
        if ocr_data.get('drug_name'):
            drug_errors = self._check_drug_name(ocr_data['drug_name'])
            errors.extend(drug_errors)
        
        # Check batch number format
        if ocr_data.get('batch_number'):
            batch_errors = self._check_batch_number(ocr_data['batch_number'])
            errors.extend(batch_errors)
        
        # Check expiry date format
        if ocr_data.get('expiry_date'):
            date_errors = self._check_expiry_date(ocr_data['expiry_date'])
            errors.extend(date_errors)
        
        # Check for common OCR character errors
        text_errors = self._check_common_ocr_errors(ocr_data.get('extracted_text', ''))
        errors.extend(text_errors)
        
        return errors
    
    def _check_drug_name(self, drug_name: str) -> List[Dict[str, Any]]:
        """Check drug name for potential errors"""
        errors = []
        
        # Extract just the drug name (remove dosage)
        name_only = re.split(r'\d+', drug_name)[0].strip().upper()
        
        # Check if it matches known drugs
        best_match = self._find_closest_match(name_only, self.common_drugs)
        
        if best_match and best_match != name_only:
            similarity = self._calculate_similarity(name_only, best_match)
            
            if similarity > 0.7:  # Potential typo
                errors.append({
                    'error_type': 'spelling',
                    'field_name': 'drug_name',
                    'actual_value': drug_name,
                    'expected_value': best_match,
                    'confidence': similarity,
                    'suggestion': f"Did you mean '{best_match}'?"
                })
        
        return errors
    
    def _check_batch_number(self, batch_number: str) -> List[Dict[str, Any]]:
        """Check batch number for format errors"""
        errors = []
        
        # Expected format: BN-YYYY-NNNNNN
        if not re.match(r'^[A-Z]{2}-\d{4}-\d{6}$', batch_number):
            errors.append({
                'error_type': 'format',
                'field_name': 'batch_number',
                'actual_value': batch_number,
                'expected_value': 'BN-YYYY-NNNNNN',
                'confidence': 0.9,
                'suggestion': 'Batch number should follow format: BN-YYYY-NNNNNN'
            })
        
        return errors
    
    def _check_expiry_date(self, expiry_date: str) -> List[Dict[str, Any]]:
        """Check expiry date for format errors"""
        errors = []
        
        # Common date formats: MM/YYYY, MM-YYYY, MM.YYYY
        valid_formats = [
            r'^\d{2}/\d{4}$',
            r'^\d{2}-\d{4}$',
            r'^\d{2}\.\d{4}$'
        ]
        
        is_valid = any(re.match(pattern, expiry_date) for pattern in valid_formats)
        
        if not is_valid:
            errors.append({
                'error_type': 'format',
                'field_name': 'expiry_date',
                'actual_value': expiry_date,
                'expected_value': 'MM/YYYY',
                'confidence': 0.85,
                'suggestion': 'Expiry date should be in MM/YYYY format'
            })
        
        return errors
    
    def _check_common_ocr_errors(self, text: str) -> List[Dict[str, Any]]:
        """Check for common OCR character misrecognitions"""
        errors = []
        
        # Check for suspicious patterns
        suspicious_patterns = [
            (r'\b[O0]{2,}\b', 'Possible confusion between O and 0'),
            (r'\b[I1]{2,}\b', 'Possible confusion between I and 1'),
            (r'[A-Z]{10,}', 'Unusually long uppercase sequence'),
        ]
        
        for pattern, message in suspicious_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                errors.append({
                    'error_type': 'character_confusion',
                    'field_name': 'extracted_text',
                    'actual_value': match.group(),
                    'expected_value': None,
                    'confidence': 0.6,
                    'suggestion': message
                })
        
        return errors
    
    def _find_closest_match(self, text: str, candidates: List[str]) -> str:
        """Find the closest matching string from candidates"""
        if not candidates:
            return None
        
        best_match = None
        best_ratio = 0
        
        for candidate in candidates:
            ratio = self._calculate_similarity(text, candidate)
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = candidate
        
        return best_match if best_ratio > 0.6 else None
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity ratio between two strings"""
        return SequenceMatcher(None, str1.upper(), str2.upper()).ratio()
    
    def suggest_corrections(self, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate correction suggestions based on detected errors
        
        Args:
            errors: List of detected errors
            
        Returns:
            Dictionary with correction suggestions
        """
        suggestions = {
            'total_errors': len(errors),
            'critical_errors': len([e for e in errors if e.get('confidence', 0) > 0.8]),
            'corrections': []
        }
        
        for error in errors:
            if error.get('confidence', 0) > 0.7:
                suggestions['corrections'].append({
                    'field': error['field_name'],
                    'current': error['actual_value'],
                    'suggested': error.get('expected_value'),
                    'reason': error.get('suggestion')
                })
        
        return suggestions
