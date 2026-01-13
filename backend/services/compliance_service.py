"""
Compliance Service - Validates OCR results against compliance rules
"""

import re
from typing import List, Dict, Any
from datetime import datetime

class ComplianceService:
    """Service for compliance checking"""
    
    def __init__(self):
        self.rules = self._load_default_rules()
    
    def _load_default_rules(self) -> List[Dict[str, Any]]:
        """Load default compliance rules"""
        return [
            {
                'rule_name': 'Drug Name Required',
                'rule_type': 'content',
                'check': lambda data: bool(data.get('drug_name')),
                'message': 'Drug name is required on pharmaceutical labels',
                'severity': 'critical'
            },
            {
                'rule_name': 'Batch Number Format',
                'rule_type': 'format',
                'check': lambda data: self._validate_batch_number(data.get('batch_number')),
                'message': 'Batch number must follow standard format',
                'severity': 'high'
            },
            {
                'rule_name': 'Expiry Date Required',
                'rule_type': 'content',
                'check': lambda data: bool(data.get('expiry_date')),
                'message': 'Expiry date is required',
                'severity': 'critical'
            },
            {
                'rule_name': 'Manufacturer Information',
                'rule_type': 'content',
                'check': lambda data: bool(data.get('manufacturer')),
                'message': 'Manufacturer information is required',
                'severity': 'high'
            },
            {
                'rule_name': 'Controlled Substance Marking',
                'rule_type': 'regulatory',
                'check': lambda data: self._validate_controlled_substance(data),
                'message': 'Controlled substances must be properly marked',
                'severity': 'critical'
            }
        ]
    
    def validate_ocr_result(self, ocr_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validate OCR results against compliance rules
        
        Args:
            ocr_data: Dictionary containing OCR results
            
        Returns:
            List of compliance check results
        """
        results = []
        
        for rule in self.rules:
            try:
                passed = rule['check'](ocr_data)
                
                results.append({
                    'rule_name': rule['rule_name'],
                    'check_type': rule['rule_type'],
                    'status': 'passed' if passed else 'failed',
                    'message': rule['message'] if not passed else f"{rule['rule_name']} validation passed",
                    'severity': rule['severity']
                })
            except Exception as e:
                results.append({
                    'rule_name': rule['rule_name'],
                    'check_type': rule['rule_type'],
                    'status': 'error',
                    'message': f"Validation error: {str(e)}",
                    'severity': 'medium'
                })
        
        return results
    
    def _validate_batch_number(self, batch_number: str) -> bool:
        """Validate batch number format"""
        if not batch_number:
            return False
        
        # Example: BN-YYYY-NNNNNN format
        pattern = r'^[A-Z]{2}-\d{4}-\d{6}$'
        return bool(re.match(pattern, batch_number))
    
    def _validate_controlled_substance(self, data: Dict[str, Any]) -> bool:
        """Validate controlled substance marking"""
        is_controlled = data.get('controlled_substance', False)
        text = data.get('extracted_text', '')
        
        # If marked as controlled, ensure proper labeling in text
        if is_controlled:
            return bool(re.search(r'schedule\s+[I-V]+', text, re.IGNORECASE))
        
        return True
    
    def calculate_compliance_score(self, checks: List[Dict[str, Any]]) -> float:
        """
        Calculate overall compliance score
        
        Args:
            checks: List of compliance check results
            
        Returns:
            Compliance score (0-100)
        """
        if not checks:
            return 0.0
        
        total_weight = 0
        passed_weight = 0
        
        severity_weights = {
            'critical': 4,
            'high': 3,
            'medium': 2,
            'low': 1
        }
        
        for check in checks:
            weight = severity_weights.get(check.get('severity', 'medium'), 2)
            total_weight += weight
            
            if check.get('status') == 'passed':
                passed_weight += weight
        
        return (passed_weight / total_weight * 100) if total_weight > 0 else 0.0
