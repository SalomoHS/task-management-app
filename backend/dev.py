from flask import Flask, jsonify
from flask_cors import CORS
from utils.db_connection import db
import os
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from routes.tasks import tasks_bp
    from routes.users import users_bp
    from routes.agent import agent_bp
    
    app.register_blueprint(tasks_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(agent_bp)
    
    @app.route('/health')
    async def health_check():
        # Test psycopg2 connection with tasks table
        try:
            db.execute_query('SELECT 1', fetch_one=True)
            db_status = 'connected'
        except:
            db_status = 'disconnected'
        
        return jsonify({
            'status': 'healthy', 
            'message': 'Task Management API is running',
            'database': db_status
        })
    
    @app.route('/api/health')
    async def api_health_check():
        """API health check endpoint"""
        try:
            db.execute_query('SELECT 1', fetch_one=True)
            db_status = 'connected'
        except:
            db_status = 'disconnected'
            
        return jsonify({
            'status': 'healthy',
            'api_version': '1.0.0',
            'database': db_status
        })
    
    return app

app = create_app()