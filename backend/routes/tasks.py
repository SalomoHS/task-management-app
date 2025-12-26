"""
Task CRUD routes using Supabase client directly
"""
from flask import Blueprint, request, jsonify
from utils.supabaseClient import supabase_client

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    try:
        response = supabase_client.schema('task_management_app').table('tasks').select('*').execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task"""
    try:
        response = supabase_client.schema('task_management_app').table('tasks').select('*').eq('task_id', task_id).execute()
        if not response.data:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify(response.data[0])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('', methods=['POST'])
def create_task():
    """Create a new task"""
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
def update_task(task_id):
    """Update a task"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        update_data = {}
        if 'title' in data:
            update_data['title'] = data['title']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'status' in data:
            update_data['status_id'] = data['status_id']
        
        response = supabase_client.schema('task_management_app').table('tasks').update(update_data).eq('task_id', task_id).execute()
        if not response.data:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify(response.data[0])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        response = supabase_client.schema('task_management_app').table('tasks').delete().eq('task_id', task_id).execute()
        if not response.data:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500