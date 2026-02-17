
"""
OCR Routes - API endpoints for OCR processing with Ollama
"""

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from database import db
from models.database import Document, OCRResult
from services.ollama_ocr_service import OllamaOCRService
from services.compliance_service import ComplianceService
from services.error_detection_service import ErrorDetectionService

bp = Blueprint('ocr', __name__, url_prefix='/api/ocr')

# Initialize Ollama OCR service (primary engine)
ocr_service = OllamaOCRService(
    ollama_endpoint=os.getenv('OLLAMA_ENDPOINT', 'http://localhost:11434'),
    model_name=os.getenv('OLLAMA_MODEL', 'glm-ocr:latest'),
    timeout=int(os.getenv('OLLAMA_TIMEOUT', '30'))
)
compliance_service = ComplianceService()
error_service = ErrorDetectionService()

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'tiff'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
def upload_document():
    """Upload and process a document with Ollama OCR"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        
        # Create document record
        document = Document(
            filename=filename,
            file_path=file_path,
            file_type=filename.rsplit('.', 1)[1].lower(),
            file_size=os.path.getsize(file_path),
            status='processing'
        )
        db.session.add(document)
        db.session.commit()
        
        # Process with Ollama OCR
        try:
            if document.file_type == 'pdf':
                ocr_result = ocr_service.process_pdf(file_path)
            else:
                ocr_result = ocr_service.process_image(file_path)
            
            # Save OCR result
            ocr_record = OCRResult(
                document_id=document.id,
                extracted_text=ocr_result['extracted_text'],
                confidence_score=ocr_result['confidence_score'],
                processing_time=ocr_result['processing_time'],
                drug_name=ocr_result.get('drug_name'),
                batch_number=ocr_result.get('batch_number'),
                expiry_date=ocr_result.get('expiry_date'),
                manufacturer=ocr_result.get('manufacturer'),
                controlled_substance=ocr_result.get('controlled_substance', False),
                ocr_engine='ollama',
                model_name=ocr_result.get('model_name'),
                pages_processed=ocr_result.get('pages_processed')
            )
            db.session.add(ocr_record)
            
            # Update document status
            document.status = 'completed'
            db.session.commit()
            
            return jsonify({
                'success': True,
                'document_id': document.id,
                'ocr_result_id': ocr_record.id,
                'data': ocr_record.to_dict()
            }), 200
            
        except Exception as e:
            document.status = 'failed'
            db.session.commit()
            return jsonify({'error': f'Ollama OCR processing failed: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/process/<int:document_id>', methods=['POST'])
def process_document(document_id):
    """Process an already uploaded document with Ollama OCR"""
    try:
        document = Document.query.get_or_404(document_id)
        
        # Process with Ollama OCR
        if document.file_type == 'pdf':
            ocr_result = ocr_service.process_pdf(document.file_path)
        else:
            ocr_result = ocr_service.process_image(document.file_path)
        
        # Save OCR result
        ocr_record = OCRResult(
            document_id=document.id,
            extracted_text=ocr_result['extracted_text'],
            confidence_score=ocr_result['confidence_score'],
            processing_time=ocr_result['processing_time'],
            drug_name=ocr_result.get('drug_name'),
            batch_number=ocr_result.get('batch_number'),
            expiry_date=ocr_result.get('expiry_date'),
            manufacturer=ocr_result.get('manufacturer'),
            controlled_substance=ocr_result.get('controlled_substance', False),
            ocr_engine='ollama',
            model_name=ocr_result.get('model_name'),
            pages_processed=ocr_result.get('pages_processed')
        )
        db.session.add(ocr_record)
        document.status = 'completed'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': ocr_record.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/results/<int:result_id>', methods=['GET'])
def get_ocr_result(result_id):
    """Get OCR result by ID"""
    try:
        ocr_result = OCRResult.query.get_or_404(result_id)
        return jsonify({
            'success': True,
            'data': ocr_result.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/results/<int:result_id>/validate', methods=['POST'])
def validate_result(result_id):
    """Validate OCR result for compliance"""
    try:
        ocr_result = OCRResult.query.get_or_404(result_id)
        
        # Run compliance checks
        ocr_data = ocr_result.to_dict()
        compliance_checks = compliance_service.validate_ocr_result(ocr_data)
        
        # Save compliance checks to database
        from models.database import ComplianceCheck
        for check in compliance_checks:
            compliance_record = ComplianceCheck(
                ocr_result_id=ocr_result.id,
                check_type=check['check_type'],
                status=check['status'],
                message=check['message'],
                severity=check['severity']
            )
            db.session.add(compliance_record)
        
        db.session.commit()
        
        # Calculate compliance score
        compliance_score = compliance_service.calculate_compliance_score(compliance_checks)
        
        return jsonify({
            'success': True,
            'compliance_score': compliance_score,
            'checks': compliance_checks
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/results/<int:result_id>/errors', methods=['GET'])
def detect_errors(result_id):
    """Detect errors in OCR result"""
    try:
        ocr_result = OCRResult.query.get_or_404(result_id)
        
        # Detect errors
        ocr_data = ocr_result.to_dict()
        errors = error_service.detect_errors(ocr_data)
        
        # Save errors to database
        from models.database import ErrorDetection
        for error in errors:
            error_record = ErrorDetection(
                ocr_result_id=ocr_result.id,
                error_type=error['error_type'],
                field_name=error['field_name'],
                expected_value=error.get('expected_value'),
                actual_value=error['actual_value'],
                confidence=error['confidence'],
                suggestion=error.get('suggestion')
            )
            db.session.add(error_record)
        
        db.session.commit()
        
        # Get correction suggestions
        suggestions = error_service.suggest_corrections(errors)
        
        return jsonify({
            'success': True,
            'errors': errors,
            'suggestions': suggestions
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/documents', methods=['GET'])
def list_documents():
    """List all documents"""
    try:
        documents = Document.query.order_by(Document.upload_date.desc()).all()
        return jsonify({
            'success': True,
            'data': [doc.to_dict() for doc in documents]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    """Delete a document and its results"""
    try:
        document = Document.query.get_or_404(document_id)
        
        # Delete file
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete from database (cascade will handle related records)
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Document deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============ MULTILINGUAL OCR ENDPOINTS (Ollama Native Support) ============

@bp.route('/multilingual/upload', methods=['POST'])
def upload_multilingual():
    """Upload and process a document with Ollama (native multilingual support)"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        
        # Create document record
        document = Document(
            filename=filename,
            file_path=file_path,
            file_type=filename.rsplit('.', 1)[1].lower(),
            file_size=os.path.getsize(file_path),
            status='processing'
        )
        db.session.add(document)
        db.session.commit()
        
        # Process with Ollama (handles multilingual natively)
        try:
            if document.file_type == 'pdf':
                ocr_result = ocr_service.process_pdf(file_path)
            else:
                ocr_result = ocr_service.process_image(file_path)
            
            # Save OCR result
            ocr_record = OCRResult(
                document_id=document.id,
                extracted_text=ocr_result['extracted_text'],
                confidence_score=ocr_result['confidence_score'],
                processing_time=ocr_result['processing_time'],
                drug_name=ocr_result.get('drug_name'),
                batch_number=ocr_result.get('batch_number'),
                expiry_date=ocr_result.get('expiry_date'),
                manufacturer=ocr_result.get('manufacturer'),
                controlled_substance=ocr_result.get('controlled_substance', False),
                ocr_engine='ollama',
                model_name=ocr_result.get('model_name'),
                pages_processed=ocr_result.get('pages_processed')
            )
            db.session.add(ocr_record)
            
            # Update document status
            document.status = 'completed'
            db.session.commit()
            
            return jsonify({
                'success': True,
                'document_id': document.id,
                'ocr_result_id': ocr_record.id,
                'data': ocr_record.to_dict()
            }), 200
            
        except Exception as e:
            document.status = 'failed'
            db.session.commit()
            return jsonify({'error': f'Ollama OCR processing failed: {str(e)}'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/multilingual/process/<int:document_id>', methods=['POST'])
def process_multilingual(document_id):
    """Process an already uploaded document with Ollama (native multilingual support)"""
    try:
        document = Document.query.get_or_404(document_id)
        
        # Process with Ollama (handles multilingual natively)
        if document.file_type == 'pdf':
            ocr_result = ocr_service.process_pdf(document.file_path)
        else:
            ocr_result = ocr_service.process_image(document.file_path)
        
        # Save OCR result
        ocr_record = OCRResult(
            document_id=document.id,
            extracted_text=ocr_result['extracted_text'],
            confidence_score=ocr_result['confidence_score'],
            processing_time=ocr_result['processing_time'],
            drug_name=ocr_result.get('drug_name'),
            batch_number=ocr_result.get('batch_number'),
            expiry_date=ocr_result.get('expiry_date'),
            manufacturer=ocr_result.get('manufacturer'),
            controlled_substance=ocr_result.get('controlled_substance', False),
            ocr_engine='ollama',
            model_name=ocr_result.get('model_name'),
            pages_processed=ocr_result.get('pages_processed')
        )
        db.session.add(ocr_record)
        document.status = 'completed'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': ocr_record.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/multilingual/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages for Ollama OCR"""
    try:
        languages = ocr_service.get_supported_languages()
        return jsonify({
            'success': True,
            'supported_languages': languages
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
