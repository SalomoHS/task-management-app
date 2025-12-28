from flask import Blueprint, request, jsonify
from agents.gateway import AgentGateway
from utils.jwt_utils import jwt_required

agent_bp = Blueprint('agent', __name__)

@agent_bp.route('/api/agent/process', methods=['POST'])
@jwt_required
async def process_prompt():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({'error': 'No prompt provided'}), 400
    
    prompt = data['prompt']
    
    # Get token from header
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if auth_header else None
    
    try:
        gateway = AgentGateway()
        result = await gateway.call_agents(prompt, token)
        
        if isinstance(result, dict):
            if result.get('status') == 'rejected':
                return jsonify({
                    'status': 'rejected',
                    'response': result['message']
                }), 400
        
        return jsonify({
            'status': 'success',
            'response': str(result)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
