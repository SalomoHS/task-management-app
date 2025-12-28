import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from typing import Optional, Any
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self):
        self.connection_params = {
            'dbname': os.getenv('DB_NAME'),
            'host': os.getenv('DB_HOST'),
            'port': int(os.getenv('DB_PORT')),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'options': f'-c search_path={os.getenv("DB_SCHEMA")}'
        }
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            yield conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    @contextmanager
    def get_cursor(self, cursor_factory=None):
        """Context manager for database cursors"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=cursor_factory)
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                conn.rollback()
                logger.error(f"Database operation error: {e}")
                raise
            finally:
                cursor.close()
    
    def execute_query(self, query: str, params: Optional[tuple] = None, 
                     fetch_one: bool = False, fetch_all: bool = False) -> Optional[Any]:
        """Execute a SQL query and return results"""
        try:
            with self.get_cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(query, params)
                
                if fetch_one:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
                else:
                    return None
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise
    
    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute an UPDATE/INSERT/DELETE query and return affected rows"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Update execution error: {e}")
            raise

# Global database instance
db = DatabaseConnection()