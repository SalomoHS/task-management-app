from flask import Blueprint, request, jsonify
from ai_agent import AICrudAgent
from utils.jwt_utils import jwt_required, admin_required
from rich.console import Console

console = Console()
ai_agent_bp = Blueprint('ai_agent', __name__)

# Initialize AI agent
ai_agent = AICrudAgent()

@ai_agent_bp.route('/ai-agent/create/<entity_type>', methods=['POST'])
@jwt_required
def create_entity(entity_type):
    """Create a new entity using AI - requires authentication"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        result = ai_agent.create_entity(entity_type, data)
        return jsonify({
            'success': True,
            'message': f'{entity_type} created successfully',
            'data': result
        })
    
    except Exception as e:
        console.print(f"[red]Error creating {entity_type}: {e}[/red]")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_agent_bp.route('/ai-agent/read/<entity_type>', methods=['GET'])
@jwt_required
def read_entities(entity_type):
    """Read entities with optional criteria - requires authentication"""
    try:
        criteria = request.args.to_dict()
        result = ai_agent.read_entity(entity_type, criteria)
        
        return jsonify({
            'success': True,
            'message': f'Found {len(result)} {entity_type} entities',
            'data': result
        })
    
    except Exception as e:
        console.print(f"[red]Error reading {entity_type}: {e}[/red]")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_agent_bp.route('/ai-agent/update/<entity_type>/<entity_id>', methods=['PUT'])
@jwt_required
def update_entity(entity_type, entity_id):
    """Update an existing entity - requires authentication"""
    try:
        updates = request.get_json()
        if not updates:
            return jsonify({'error': 'No update data provided'}), 400
        
        result = ai_agent.update_entity(entity_type, entity_id, updates)
        return jsonify({
            'success': True,
            'message': f'{entity_type} {entity_id} updated successfully',
            'data': result
        })
    
    except Exception as e:
        console.print(f"[red]Error updating {entity_type} {entity_id}: {e}[/red]")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_agent_bp.route('/ai-agent/delete/<entity_type>/<entity_id>', methods=['DELETE'])
@jwt_required
def delete_entity(entity_type, entity_id):
    """Delete an entity - requires authentication"""
    try:
        result = ai_agent.delete_entity(entity_type, entity_id)
        return jsonify({
            'success': True,
            'message': f'{entity_type} {entity_id} deleted successfully',
            'data': result
        })
    
    except Exception as e:
        console.print(f"[red]Error deleting {entity_type} {entity_id}: {e}[/red]")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_agent_bp.route('/ai-agent/query/<entity_type>', methods=['POST'])
@jwt_required
def query_entities(entity_type):
    """Query entities using natural language - requires authentication"""
    try:
        query_data = request.get_json()
        if not query_data or 'query' not in query_data:
            return jsonify({'error': 'No query provided'}), 400
        
        result = ai_agent.query_entities(entity_type, query_data['query'])
        return jsonify({
            'success': True,
            'message': f'Query returned {len(result)} {entity_type} entities',
            'data': result
        })
    
    except Exception as e:
        console.print(f"[red]Error querying {entity_type}: {e}[/red]")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_agent_bp.route('/ai-agent/validate/<entity_type>', methods=['POST'])
@jwt_required
def validate_entity(entity_type):
    """Validate entity data - requires authentication"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided for validation'}), 400
        
        result = ai_agent.validate_entity(entity_type, data)
        return jsonify({
            'success': True,
            'message': f'{entity_type} validation completed',
            'data': result
        })
    
    except Exception as e:
        console.print(f"[red]Error validating {entity_type}: {e}[/red]")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_agent_bp.route('/ai-agent/health', methods=['GET'])
def ai_agent_health():
    """Check AI agent health - no authentication required"""
    try:
        # Test basic functionality
        test_result = ai_agent.validate_entity("test", {"name": "test"})
        
        return jsonify({
            'status': 'healthy',
            'message': 'AI Agent is running',
            'gemini_model': 'gemini-2.5-flash',
            'test_validation': test_result
        })
    
    except Exception as e:
        console.print(f"[red]AI Agent health check failed: {e}[/red]")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503