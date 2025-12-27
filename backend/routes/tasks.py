"""
Task CRUD routes using Supabase client directly with JWT authentication
"""
from flask import Blueprint, request, jsonify
from utils.supabaseClient import supabase_client
from utils.jwt_utils import jwt_required

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@tasks_bp.route('', methods=['GET'])
@jwt_required
def get_tasks():
    """Get all tasks - requires authentication"""
    try:
        response = supabase_client.schema('task_management_app').table('tasks').select('*, status_id(status)').execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required
def get_task(task_id):
    """Get a specific task - requires authentication"""
    try:
        response = supabase_client.schema('task_management_app').table('tasks').select('*, status_id(status)').eq('task_id', task_id).execute()
        if not response.data:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify(response.data[0])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('', methods=['POST'])
@jwt_required
def create_task():
    """Create a new task - requires authentication"""
    try:
        data = request.get_json()
        if not data or not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        if not data or not data.get('status_id'):
            return jsonify({'error': 'Status is required'}), 400

        task_data = {
            'title': data['title'],
            'description': data.get('description', 'no description'),
            'status_id': data.get('status_id'),
        }
        
        response = supabase_client.schema('task_management_app').table('tasks').insert(task_data).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required
def update_task(task_id):
    """Update a task - requires authentication"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        update_data = {}
        if 'title' in data:
            update_data['title'] = data['title']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'status_id' in data:
            update_data['status_id'] = data['status_id']
        
        response = supabase_client.schema('task_management_app').table('tasks').update(update_data).eq('task_id', task_id).execute()
        if not response.data:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify(response.data[0])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required
def delete_task(task_id):
    """Delete a task - requires authentication"""
    try:
        response = supabase_client.schema('task_management_app').table('tasks').delete().eq('task_id', task_id).execute()
        if not response.data:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500