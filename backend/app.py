from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from utils.supabaseClient import supabase_client

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from routes.tasks import tasks_bp
    from routes.users import users_bp
    
    app.register_blueprint(tasks_bp)
    app.register_blueprint(users_bp)
    
    @app.route('/health')
    def health_check():
        # Test Supabase connection with tasks table
        try:
            supabase_client.schema('task_management_app').table('tasks').select('*').limit(1).execute()
            db_status = 'connected'
        except:
            db_status = 'disconnected'
        
        return jsonify({
            'status': 'healthy', 
            'message': 'Task Management API is running',
            'database': db_status
        })
    
    @app.route('/api/health')
    def api_health_check():
        """API health check endpoint"""
        try:
            supabase_client.schema('task_management_app').table('tasks').select('*').limit(1).execute()
            db_status = 'connected'
        except:
            db_status = 'disconnected'
            
        return jsonify({
            'status': 'healthy',
            'api_version': '1.0.0',
            'database': db_status
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)