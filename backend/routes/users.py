"""
User routes with hardcoded dummy admin account
"""
from flask import Blueprint, request, jsonify
from datetime import datetime

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

# Hardcoded dummy admin user
DUMMY_ADMIN = {
    'id': 1,
    'username': 'admin',
    'password': 'admin123',  # Simple password for demo
    'role': 'admin',
    'created_at': '2024-01-01T00:00:00Z'
}

@users_bp.route('', methods=['GET'])
def get_users():
    """Get all users - returns hardcoded admin (without password)"""
    admin_safe = DUMMY_ADMIN.copy()
    admin_safe.pop('password', None)  # Don't expose password
    return jsonify([admin_safe])

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user - only admin (id=1) exists"""
    if user_id == 1:
        admin_safe = DUMMY_ADMIN.copy()
        admin_safe.pop('password', None)  # Don't expose password
        return jsonify(admin_safe)
    else:
        return jsonify({'error': 'User not found'}), 404

@users_bp.route('/login', methods=['POST'])
def login():
    """Login endpoint for admin user"""
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        username = data['username']
        password = data['password']
        
        # Check credentials against hardcoded admin
        if username == DUMMY_ADMIN['username'] and password == DUMMY_ADMIN['password']:
            admin_safe = DUMMY_ADMIN.copy()
            admin_safe.pop('password', None)  # Don't return password
            return jsonify({
                'message': 'Login successful',
                'user': admin_safe
            })
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('', methods=['POST'])
def create_user():
    """Create user endpoint - not implemented, admin already exists"""
    return jsonify({'error': 'User creation disabled - admin user already exists'}), 400

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user endpoint - not implemented"""
    return jsonify({'error': 'User updates disabled - using hardcoded admin'}), 400

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user endpoint - not implemented"""
    return jsonify({'error': 'User deletion disabled - admin user is permanent'}), 400