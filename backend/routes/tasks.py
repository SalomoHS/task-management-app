"""
Task CRUD routes using psycopg2 with JWT authentication
"""
from flask import Blueprint, request, jsonify
from utils.db_connection import db
from utils.jwt_utils import jwt_required

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@tasks_bp.route('', methods=['GET'])
@jwt_required
async def get_tasks():
    """Get all tasks - requires authentication"""
    try:
        query = """
        SELECT t.*, s.status 
        FROM tasks t 
        LEFT JOIN status s ON t.status_id = s.status_id
        ORDER BY t.task_id
        """
        tasks = db.execute_query(query, fetch_all=True)
        return jsonify(tasks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required
async def get_task(task_id):
    """Get a specific task - requires authentication"""
    try:
        query = """
        SELECT t.*, s.status 
        FROM tasks t 
        LEFT JOIN status s ON t.status_id = s.status_id
        WHERE t.task_id = %s
        """
        task = db.execute_query(query, (task_id,), fetch_one=True)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify(task)
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

        query = """
        INSERT INTO tasks (title, description, status_id)
        VALUES (%s, %s, %s)
        RETURNING *
        """
        params = (
            data['title'],
            data.get('description', 'no description'),
            data['status_id']
        )
        
        task = db.execute_query(query, params, fetch_one=True)
        return jsonify(task), 201
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
        
        # Build dynamic update query based on provided fields
        update_fields = []
        params = []
        
        if 'title' in data:
            update_fields.append('title = %s')
            params.append(data['title'])
        if 'description' in data:
            update_fields.append('description = %s')
            params.append(data['description'])
        if 'status_id' in data:
            update_fields.append('status_id = %s')
            params.append(data['status_id'])
        
        if not update_fields:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        params.append(task_id)  # Add task_id for WHERE clause
        
        query = f"""
        UPDATE tasks 
        SET {', '.join(update_fields)}
        WHERE task_id = %s
        RETURNING *
        """
        
        task = db.execute_query(query, tuple(params), fetch_one=True)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify(task)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required
async def delete_task(task_id):
    """Delete a task - requires authentication"""
    try:
        query = "DELETE FROM tasks WHERE task_id = %s RETURNING *"
        task = db.execute_query(query, (task_id,), fetch_one=True)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500