from flask import Flask, jsonify
from flask_cors import CORS
import docker
import psutil
import socket
from datetime import datetime
from db import Database

app = Flask(__name__)
CORS(app)  # Frontend se API call karne ke liye

# Docker client initialize karo
try:
    docker_client = docker.from_env()
except Exception as e:
    print(f"Docker client initialization failed: {e}")
    docker_client = None

# Database connection
db = Database()

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'Docker Status Tracker API',
        'version': '1.0.0'
    })

@app.route('/status')
def system_status():
    """
    System status check karo - NGINX, Database, Docker daemon
    """
    nginx_status = check_nginx_status()
    db_status = db.check_connection()
    docker_status = check_docker_status()
    
    # Database mein log save karo
    db.log_status('system', f'NGINX:{nginx_status}, DB:{db_status}, Docker:{docker_status}')
    
    return jsonify({
        'nginx_status': nginx_status,
        'db_status': db_status,
        'docker_status': docker_status,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/containers')
def get_containers():
    """
    Docker containers ki list return karo (running + stopped)
    """
    if not docker_client:
        return jsonify({'error': 'Docker not available', 'containers': []}), 500
    
    try:
        containers = docker_client.containers.list(all=True)
        container_list = []
        
        for container in containers:
            # Port mapping extract karo
            ports = container.attrs.get('NetworkSettings', {}).get('Ports', {})
            port_str = ', '.join([f"{k.split('/')[0]}" for k in ports.keys() if ports[k]]) or 'N/A'
            
            container_info = {
                'name': container.name,
                'image': container.image.tags[0] if container.image.tags else 'unknown',
                'status': container.status,
                'ports': port_str,
                'created': container.attrs['Created'][:10],  # Date only
                'id': container.short_id
            }
            container_list.append(container_info)
            
            # Database mein container info log karo
            db.log_container(container.name, container.status, port_str)
        
        return jsonify({
            'containers': container_list,
            'total': len(container_list)
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'containers': []}), 500

@app.route('/ports')
def get_ports():
    """
    Important ports ki status check karo (open/closed)
    """
    # Common ports jo check karni hain
    ports_to_check = [
        {'port': 80, 'service': 'NGINX/HTTP', 'protocol': 'TCP'},
        {'port': 443, 'service': 'HTTPS', 'protocol': 'TCP'},
        {'port': 3306, 'service': 'MySQL', 'protocol': 'TCP'},
        {'port': 5000, 'service': 'Flask Backend', 'protocol': 'TCP'},
        {'port': 8080, 'service': 'Alternative HTTP', 'protocol': 'TCP'},
    ]
    
    port_status = []
    
    for port_info in ports_to_check:
        status = check_port(port_info['port'])
        port_status.append({
            'port': port_info['port'],
            'service': port_info['service'],
            'status': 'Open' if status else 'Closed',
            'protocol': port_info['protocol']
        })
    
    return jsonify({'ports': port_status})

@app.route('/logs')
def get_logs():
    """
    Database se recent logs fetch karo
    """
    logs = db.get_recent_logs(limit=50)
    return jsonify({'logs': logs})

# Helper Functions

def check_nginx_status():
    """
    NGINX container running hai ya nahi check karo
    """
    if not docker_client:
        return 'Unknown'
    
    try:
        containers = docker_client.containers.list(filters={'name': 'nginx'})
        if containers and containers[0].status == 'running':
            return 'Running'
        return 'Stopped'
    except:
        return 'Unknown'

def check_docker_status():
    """
    Docker daemon running hai ya nahi
    """
    if docker_client:
        try:
            docker_client.ping()
            return 'Running'
        except:
            return 'Stopped'
    return 'Not Available'

def check_port(port):
    """
    Specific port open hai ya nahi check karo
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

if __name__ == '__main__':
    # Database tables create karo agar exist nahi karti
    db.create_tables()
    
    # Flask app start karo
    app.run(host='0.0.0.0', port=5000, debug=False)
