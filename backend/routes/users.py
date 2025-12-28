"""
User routes with hardcoded dummy admin account and JWT authentication
"""
from flask import Blueprint, request, jsonify
from utils.jwt_utils import generate_jwt_token, jwt_required, admin_required

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

# Hardcoded dummy admin user
DUMMY_ADMIN = {
    'id': 1,
    'username': 'admin',
    'password': 'admin',  # Simple password for demo
    'role': 'admin',
    'created_at': '2024-01-01T00:00:00Z'
}

@users_bp.route('', methods=['GET'])
@jwt_required
async def get_users():
    """Get all users - returns hardcoded admin (without password) - requires authentication"""
    admin_safe = DUMMY_ADMIN.copy()
    admin_safe.pop('password', None)  # Don't expose password
    return jsonify([admin_safe])

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required
async def get_user(user_id):
    """Get a specific user - only admin (id=1) exists - requires authentication"""
    if user_id == 1:
        admin_safe = DUMMY_ADMIN.copy()
        admin_safe.pop('password', None)  # Don't expose password
        return jsonify(admin_safe)
    else:
        return jsonify({'error': 'User not found'}), 404

@users_bp.route('/login', methods=['POST'])
async def login():
    """Login endpoint for admin user - returns JWT token on success"""
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        username = data['username']
        password = data['password']
        
        # Check credentials against hardcoded admin
        if username == DUMMY_ADMIN['username'] and password == DUMMY_ADMIN['password']:
            # Generate JWT token
            token = generate_jwt_token(DUMMY_ADMIN)
            
            admin_safe = DUMMY_ADMIN.copy()
            admin_safe.pop('password', None)  # Don't return password
            
            return jsonify({
                'message': 'Login successful',
                'user': admin_safe,
                'token': token,
                'token_type': 'Bearer'
            })
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('', methods=['POST'])
@jwt_required
@admin_required
async def create_user():
    """Create user endpoint - not implemented, admin already exists - requires admin access"""
    return jsonify({'error': 'User creation disabled - admin user already exists'}), 400

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required
@admin_required
async def update_user(user_id):
    """Update user endpoint - not implemented - requires admin access"""
    return jsonify({'error': 'User updates disabled - using hardcoded admin'}), 400

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_user(user_id):
    """Delete user endpoint - not implemented - requires admin access"""
    return jsonify({'error': 'User deletion disabled - admin user is permanent'}), 400

@users_bp.route('/me', methods=['GET'])
@jwt_required
def get_current_user():
    """Get current authenticated user info"""
    user_id = request.current_user.get('user_id')
    if user_id == 1:
        admin_safe = DUMMY_ADMIN.copy()
        admin_safe.pop('password', None)
        return jsonify(admin_safe)
    else:
        return jsonify({'error': 'User not found'}), 404

@users_bp.route('/verify-token', methods=['POST'])
async def verify_token():
    """Verify if a JWT token is valid"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'valid': False, 'error': 'Token is required'}), 400
        
        from utils.jwt_utils import decode_jwt_token
        payload = decode_jwt_token(token)
        
        if payload:
            return jsonify({
                'valid': True,
                'user_id': payload.get('user_id'),
                'username': payload.get('username'),
                'role': payload.get('role')
            })
        else:
            return jsonify({'valid': False, 'error': 'Invalid or expired token'}), 401
            
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500