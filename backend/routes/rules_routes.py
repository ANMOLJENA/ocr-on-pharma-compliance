"""
Rules Routes - API endpoints for managing compliance rules
"""

from flask import Blueprint, request, jsonify
from database import db
from models.database import ComplianceRule

bp = Blueprint('rules', __name__, url_prefix='/api/rules')

@bp.route('/', methods=['GET'])
def list_rules():
    """List all compliance rules"""
    try:
        rules = ComplianceRule.query.order_by(ComplianceRule.created_date.desc()).all()
        return jsonify({
            'success': True,
            'data': [rule.to_dict() for rule in rules]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:rule_id>', methods=['GET'])
def get_rule(rule_id):
    """Get a specific rule"""
    try:
        rule = ComplianceRule.query.get_or_404(rule_id)
        return jsonify({
            'success': True,
            'data': rule.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_rule():
    """Create a new compliance rule"""
    try:
        data = request.get_json()
        
        rule = ComplianceRule(
            rule_name=data['rule_name'],
            rule_type=data['rule_type'],
            description=data.get('description'),
            pattern=data.get('pattern'),
            severity=data.get('severity', 'medium'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(rule)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': rule.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:rule_id>', methods=['PUT'])
def update_rule(rule_id):
    """Update a compliance rule"""
    try:
        rule = ComplianceRule.query.get_or_404(rule_id)
        data = request.get_json()
        
        if 'rule_name' in data:
            rule.rule_name = data['rule_name']
        if 'rule_type' in data:
            rule.rule_type = data['rule_type']
        if 'description' in data:
            rule.description = data['description']
        if 'pattern' in data:
            rule.pattern = data['pattern']
        if 'severity' in data:
            rule.severity = data['severity']
        if 'is_active' in data:
            rule.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': rule.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    """Delete a compliance rule"""
    try:
        rule = ComplianceRule.query.get_or_404(rule_id)
        db.session.delete(rule)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Rule deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:rule_id>/toggle', methods=['POST'])
def toggle_rule(rule_id):
    """Toggle rule active status"""
    try:
        rule = ComplianceRule.query.get_or_404(rule_id)
        rule.is_active = not rule.is_active
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': rule.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
