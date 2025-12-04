import mysql.connector
from datetime import datetime
import os

class Database:
    """
    MySQL database connection aur operations handle karta hai
    """
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', 'mysql'),
            'user': os.getenv('DB_USER', 'devops_user'),
            'password': os.getenv('DB_PASSWORD', 'devops_pass'),
            'database': os.getenv('DB_NAME', 'docker_tracker'),
            'port': int(os.getenv('DB_PORT', 3306))
        }
        self.connection = None
    
    def connect(self):
        """Database se connection banao"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
            return self.connection
        except mysql.connector.Error as e:
            print(f"Database connection error: {e}")
            return None
    
    def check_connection(self):
        """Database connection working hai ya nahi check karo"""
        try:
            conn = self.connect()
            if conn and conn.is_connected():
                return 'Connected'
            return 'Disconnected'
        except:
            return 'Disconnected'
    
    def create_tables(self):
        """Initial tables create karo agar exist nahi karte"""
        try:
            conn = self.connect()
            if not conn:
                return False
            
            cursor = conn.cursor()
            
            # Status logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS status_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    log_type VARCHAR(50),
                    message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_created (created_at)
                )
            """)
            
            # Container logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS container_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    container_name VARCHAR(255),
                    status VARCHAR(50),
                    ports TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_container (container_name),
                    INDEX idx_created (created_at)
                )
            """)
            
            conn.commit()
            cursor.close()
            print("Database tables created successfully!")
            return True
            
        except mysql.connector.Error as e:
            print(f"Table creation error: {e}")
            return False
    
    def log_status(self, log_type, message):
        """System status log karo database mein"""
        try:
            conn = self.connect()
            if not conn:
                return False
            
            cursor = conn.cursor()
            query = "INSERT INTO status_logs (log_type, message) VALUES (%s, %s)"
            cursor.execute(query, (log_type, message))
            conn.commit()
            cursor.close()
            return True
            
        except mysql.connector.Error as e:
            print(f"Logging error: {e}")
            return False
    
    def log_container(self, name, status, ports):
        """Container information log karo"""
        try:
            conn = self.connect()
            if not conn:
                return False
            
            cursor = conn.cursor()
            query = """
                INSERT INTO container_logs (container_name, status, ports) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (name, status, ports))
            conn.commit()
            cursor.close()
            return True
            
        except mysql.connector.Error as e:
            print(f"Container logging error: {e}")
            return False
    
    def get_recent_logs(self, limit=50):
        """Recent logs fetch karo database se"""
        try:
            conn = self.connect()
            if not conn:
                return []
            
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT log_type, message, created_at 
                FROM status_logs 
                ORDER BY created_at DESC 
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            logs = cursor.fetchall()
            cursor.close()
            
            # Datetime ko string mein convert karo (JSON serialization ke liye)
            for log in logs:
                log['created_at'] = log['created_at'].isoformat()
            
            return logs
            
        except mysql.connector.Error as e:
            print(f"Log fetch error: {e}")
            return []
    
    def close(self):
        """Database connection close karo"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
