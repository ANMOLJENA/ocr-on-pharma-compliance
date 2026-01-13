"""
Analytics Routes - API endpoints for analytics and statistics
"""

from flask import Blueprint, jsonify
from sqlalchemy import func
from database import db
from models.database import Document, OCRResult, ComplianceCheck, ErrorDetection
from datetime import datetime, timedelta

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@bp.route('/dashboard', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Total documents processed
        total_documents = Document.query.count()
        
        # Documents by status
        status_counts = db.session.query(
            Document.status,
            func.count(Document.id)
        ).group_by(Document.status).all()
        
        # Average confidence score
        avg_confidence = db.session.query(
            func.avg(OCRResult.confidence_score)
        ).scalar() or 0
        
        # Total compliance checks
        total_checks = ComplianceCheck.query.count()
        passed_checks = ComplianceCheck.query.filter_by(status='passed').count()
        failed_checks = ComplianceCheck.query.filter_by(status='failed').count()
        
        # Total errors detected
        total_errors = ErrorDetection.query.count()
        
        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_documents = Document.query.filter(
            Document.upload_date >= week_ago
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_documents': total_documents,
                'status_breakdown': {status: count for status, count in status_counts},
                'average_confidence': round(avg_confidence, 2),
                'compliance': {
                    'total_checks': total_checks,
                    'passed': passed_checks,
                    'failed': failed_checks,
                    'pass_rate': round((passed_checks / total_checks * 100) if total_checks > 0 else 0, 2)
                },
                'total_errors': total_errors,
                'recent_activity': recent_documents
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/accuracy', methods=['GET'])
def get_accuracy_metrics():
    """Get OCR accuracy metrics"""
    try:
        # Confidence score distribution
        confidence_ranges = [
            (0.0, 0.5, 'Low'),
            (0.5, 0.7, 'Medium'),
            (0.7, 0.9, 'High'),
            (0.9, 1.0, 'Very High')
        ]
        
        distribution = []
        for min_val, max_val, label in confidence_ranges:
            count = OCRResult.query.filter(
                OCRResult.confidence_score >= min_val,
                OCRResult.confidence_score < max_val
            ).count()
            distribution.append({
                'range': label,
                'count': count
            })
        
        # Average processing time
        avg_processing_time = db.session.query(
            func.avg(OCRResult.processing_time)
        ).scalar() or 0
        
        return jsonify({
            'success': True,
            'data': {
                'confidence_distribution': distribution,
                'average_processing_time': round(avg_processing_time, 2)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/compliance-trends', methods=['GET'])
def get_compliance_trends():
    """Get compliance trends over time"""
    try:
        # Get compliance checks grouped by date
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        trends = db.session.query(
            func.date(ComplianceCheck.checked_date).label('date'),
            ComplianceCheck.status,
            func.count(ComplianceCheck.id).label('count')
        ).filter(
            ComplianceCheck.checked_date >= thirty_days_ago
        ).group_by(
            func.date(ComplianceCheck.checked_date),
            ComplianceCheck.status
        ).all()
        
        # Format data
        trend_data = {}
        for date, status, count in trends:
            date_str = date.isoformat()
            if date_str not in trend_data:
                trend_data[date_str] = {'passed': 0, 'failed': 0, 'warning': 0}
            trend_data[date_str][status] = count
        
        return jsonify({
            'success': True,
            'data': trend_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/error-analysis', methods=['GET'])
def get_error_analysis():
    """Get error analysis statistics"""
    try:
        # Errors by type
        error_types = db.session.query(
            ErrorDetection.error_type,
            func.count(ErrorDetection.id).label('count')
        ).group_by(ErrorDetection.error_type).all()
        
        # Most common error fields
        error_fields = db.session.query(
            ErrorDetection.field_name,
            func.count(ErrorDetection.id).label('count')
        ).group_by(ErrorDetection.field_name).order_by(
            func.count(ErrorDetection.id).desc()
        ).limit(10).all()
        
        return jsonify({
            'success': True,
            'data': {
                'error_types': [{'type': t, 'count': c} for t, c in error_types],
                'common_fields': [{'field': f, 'count': c} for f, c in error_fields]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/controlled-substances', methods=['GET'])
def get_controlled_substances_stats():
    """Get statistics on controlled substances"""
    try:
        total_controlled = OCRResult.query.filter_by(
            controlled_substance=True
        ).count()
        
        total_results = OCRResult.query.count()
        
        percentage = (total_controlled / total_results * 100) if total_results > 0 else 0
        
        return jsonify({
            'success': True,
            'data': {
                'total_controlled': total_controlled,
                'total_documents': total_results,
                'percentage': round(percentage, 2)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
