"""
JWT utility functions for authentication
"""
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
import os
import inspect
from dotenv import load_dotenv
load_dotenv()

# JWT Secret key - in production, this should be in environment variables
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24

def generate_jwt_token(user_data):
    """
    Generate JWT token for authenticated user
    """
    payload = {
        'user_id': user_data['id'],
        'username': user_data['username'],
        'role': user_data['role'],
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def decode_jwt_token(token):
    """
    Decode and validate JWT token
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def verify_jwt_token():
    """
    Helper function to verify JWT token from request
    Returns: (payload, error_response)
    """
    token = None
    
    # Check for token in Authorization header
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            token = auth_header.split(' ')[1]  # Bearer <token>
        except IndexError:
            return None, (jsonify({'error': 'Invalid authorization header format'}), 401)
    
    if not token:
        return None, (jsonify({'error': 'Token is missing'}), 401)
    
    # Decode token
    payload = decode_jwt_token(token)
    if payload is None:
        return None, (jsonify({'error': 'Token is invalid or expired'}), 401)
        
    return payload, None

def jwt_required(f):
    """
    Decorator to require JWT authentication for routes
    Supports both sync and async routes
    """
    if inspect.iscoroutinefunction(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            payload, error_response = verify_jwt_token()
            if error_response:
                return error_response
            
            # Add user info to request context
            request.current_user = payload
            
            return await f(*args, **kwargs)
        return decorated_function
    else:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            payload, error_response = verify_jwt_token()
            if error_response:
                return error_response
            
            # Add user info to request context
            request.current_user = payload
            
            return f(*args, **kwargs)
        return decorated_function

def admin_required(f):
    """
    Decorator to require admin role for routes
    Supports both sync and async routes
    """
    if inspect.iscoroutinefunction(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            if not hasattr(request, 'current_user'):
                return jsonify({'error': 'Authentication required'}), 401
            
            if request.current_user.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            return await f(*args, **kwargs)
        return decorated_function
    else:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'current_user'):
                return jsonify({'error': 'Authentication required'}), 401
            
            if request.current_user.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            return f(*args, **kwargs)
        return decorated_function