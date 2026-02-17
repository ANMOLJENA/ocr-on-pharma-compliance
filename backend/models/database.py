from database import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class Document(db.Model):
    """Model for uploaded documents"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    
    # Relationships
    ocr_results = db.relationship('OCRResult', backref='document', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'upload_date': self.upload_date.isoformat(),
            'status': self.status
        }


class OCRResult(db.Model):
    """Model for OCR processing results"""
    __tablename__ = 'ocr_results'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    extracted_text = db.Column(db.Text)
    confidence_score = db.Column(db.Float)
    processing_time = db.Column(db.Float)  # in seconds
    processed_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Pharmaceutical specific fields
    drug_name = db.Column(db.String(255))
    batch_number = db.Column(db.String(100))
    expiry_date = db.Column(db.String(50))
    manufacturer = db.Column(db.String(255))
    controlled_substance = db.Column(db.Boolean, default=False)
    
    # Ollama migration fields
    ocr_engine = db.Column(db.String(50), default='tesseract')  # 'ollama' or 'tesseract'
    model_name = db.Column(db.String(100))  # e.g., 'llava:latest'
    fallback_used = db.Column(db.Boolean, default=False)
    fallback_reason = db.Column(db.String(255))  # reason for fallback
    pages_processed = db.Column(db.Integer)  # for PDF documents
    ocr_metadata = db.Column(JSON, default={})  # additional metadata
    
    # Relationships
    compliance_checks = db.relationship('ComplianceCheck', backref='ocr_result', lazy=True, cascade='all, delete-orphan')
    errors = db.relationship('ErrorDetection', backref='ocr_result', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'extracted_text': self.extracted_text,
            'confidence_score': self.confidence_score,
            'processing_time': self.processing_time,
            'processed_date': self.processed_date.isoformat(),
            'drug_name': self.drug_name,
            'batch_number': self.batch_number,
            'expiry_date': self.expiry_date,
            'manufacturer': self.manufacturer,
            'controlled_substance': self.controlled_substance,
            'ocr_engine': self.ocr_engine,
            'model_name': self.model_name,
            'fallback_used': self.fallback_used,
            'fallback_reason': self.fallback_reason,
            'pages_processed': self.pages_processed,
            'ocr_metadata': self.ocr_metadata
        }


class ComplianceCheck(db.Model):
    """Model for compliance validation results"""
    __tablename__ = 'compliance_checks'
    
    id = db.Column(db.Integer, primary_key=True)
    ocr_result_id = db.Column(db.Integer, db.ForeignKey('ocr_results.id'), nullable=False)
    rule_id = db.Column(db.Integer, db.ForeignKey('compliance_rules.id'))
    check_type = db.Column(db.String(100))  # format, content, regulatory
    status = db.Column(db.String(50))  # passed, failed, warning
    message = db.Column(db.Text)
    severity = db.Column(db.String(50))  # low, medium, high, critical
    checked_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ocr_result_id': self.ocr_result_id,
            'rule_id': self.rule_id,
            'check_type': self.check_type,
            'status': self.status,
            'message': self.message,
            'severity': self.severity,
            'checked_date': self.checked_date.isoformat()
        }


class ErrorDetection(db.Model):
    """Model for detected errors in OCR results"""
    __tablename__ = 'error_detections'
    
    id = db.Column(db.Integer, primary_key=True)
    ocr_result_id = db.Column(db.Integer, db.ForeignKey('ocr_results.id'), nullable=False)
    error_type = db.Column(db.String(100))  # spelling, format, missing_data, invalid_data
    field_name = db.Column(db.String(100))
    expected_value = db.Column(db.String(255))
    actual_value = db.Column(db.String(255))
    confidence = db.Column(db.Float)
    suggestion = db.Column(db.String(255))
    detected_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ocr_result_id': self.ocr_result_id,
            'error_type': self.error_type,
            'field_name': self.field_name,
            'expected_value': self.expected_value,
            'actual_value': self.actual_value,
            'confidence': self.confidence,
            'suggestion': self.suggestion,
            'detected_date': self.detected_date.isoformat()
        }


class ComplianceRule(db.Model):
    """Model for compliance rules"""
    __tablename__ = 'compliance_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    rule_name = db.Column(db.String(255), nullable=False)
    rule_type = db.Column(db.String(100))  # format, content, regulatory
    description = db.Column(db.Text)
    pattern = db.Column(db.String(500))  # regex pattern or validation rule
    severity = db.Column(db.String(50))  # low, medium, high, critical
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    compliance_checks = db.relationship('ComplianceCheck', backref='rule', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'rule_name': self.rule_name,
            'rule_type': self.rule_type,
            'description': self.description,
            'pattern': self.pattern,
            'severity': self.severity,
            'is_active': self.is_active,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat()
        }


class AuditLog(db.Model):
    """Model for audit trail"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(100))  # document, ocr_result, rule
    entity_id = db.Column(db.Integer)
    user_id = db.Column(db.String(100))
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'user_id': self.user_id,
            'details': self.details,
            'timestamp': self.timestamp.isoformat()
        }
