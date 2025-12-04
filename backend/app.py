from flask import Flask, jsonify
from flask_cors import CORS
import docker
import socket
import os
from datetime import datetime
from db import Database

app = Flask(__name__)
CORS(app)

# Docker client with extensive error handling
docker_client = None
docker_error = None

def init_docker_client():
    """Initialize Docker client with multiple connection attempts"""
    global docker_client, docker_error
    
    try:
        # Try default socket
        docker_client = docker.from_env()
        docker_client.ping()
        print("✅ Docker client connected via /var/run/docker.sock")
        return True
    except Exception as e1:
        print(f"⚠️  Default socket failed: {e1}")
        
        try:
            # Try explicit socket path
            docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
            docker_client.ping()
            print("✅ Docker client connected via explicit socket")
            return True
        except Exception as e2:
            docker_error = f"Socket connection failed: {str(e1)[:100]}"
            print(f"❌ Docker client initialization failed: {e2}")
            return False

# Initialize on import
init_docker_client()

# Database connection
db = Database()

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'Docker Status Tracker API is live!',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """Complete health check"""
    docker_status = 'connected' if docker_client else 'disconnected'
    if docker_error:
        docker_status = f'error: {docker_error}'
    
    return jsonify({
        'api': 'healthy',
        'docker': docker_status,
        'database': db.check_connection(),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/status')
def system_status():
    """System status - NGINX, Database, Docker"""
    nginx_status = check_nginx_status()
    db_status = db.check_connection()
    docker_status = check_docker_status()
    
    # Log to database
    try:
        db.log_status('system', f'NGINX:{nginx_status}, DB:{db_status}, Docker:{docker_status}')
    except Exception as e:
        print(f"Logging error: {e}")
    
    return jsonify({
        'nginx_status': nginx_status,
        'db_status': db_status,
        'docker_status': docker_status,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/containers')
def get_containers():
    """Get all Docker containers"""
    if not docker_client:
        return jsonify({
            'error': 'Docker not available. Make sure /var/run/docker.sock is mounted.',
            'containers': [],
            'total': 0,
            'running': 0
        }), 200
    
    try:
        containers = docker_client.containers.list(all=True)
        container_list = []
        running_count = 0
        
        for container in containers:
            try:
                # Get port mappings
                ports_dict = container.attrs.get('NetworkSettings', {}).get('Ports', {}) or {}
                port_list = []
                
                for container_port, host_bindings in ports_dict.items():
                    if host_bindings:
                        for binding in host_bindings:
                            host_port = binding.get('HostPort', 'N/A')
                            port_list.append(f"{host_port}→{container_port}")
                    else:
                        port_list.append(container_port)
                
                port_str = ', '.join(port_list) if port_list else 'No exposed ports'
                
                # Get image name
                image_tags = container.image.tags
                image_name = image_tags[0] if image_tags else container.image.short_id
                
                # Get creation date
                created = container.attrs.get('Created', '')
                created_date = created[:10] if created else 'Unknown'
                
                # Count running containers
                if container.status == 'running':
                    running_count += 1
                
                container_info = {
                    'name': container.name,
                    'image': image_name,
                    'status': container.status,
                    'ports': port_str,
                    'created': created_date,
                    'id': container.short_id
                }
                container_list.append(container_info)
                
                # Log to database
                try:
                    db.log_container(container.name, container.status, port_str)
                except:
                    pass
                    
            except Exception as e:
                print(f"Error processing container: {e}")
                continue
        
        return jsonify({
            'containers': container_list,
            'total': len(container_list),
            'running': running_count
        })
    
    except Exception as e:
        print(f"Error fetching containers: {e}")
        return jsonify({
            'error': str(e),
            'containers': [],
            'total': 0,
            'running': 0
        }), 200

@app.route('/ports')
def get_ports():
    """Check important ports status"""
    
    # These ports we'll check on the docker host
    ports_to_check = [
        {'port': 80, 'service': 'NGINX/HTTP', 'protocol': 'TCP', 'host': 'nginx'},
        {'port': 443, 'service': 'HTTPS', 'protocol': 'TCP', 'host': 'nginx'},
        {'port': 3306, 'service': 'MySQL', 'protocol': 'TCP', 'host': 'mysql'},
        {'port': 5000, 'service': 'Flask Backend', 'protocol': 'TCP', 'host': 'localhost'},
        {'port': 8080, 'service': 'Alternative HTTP', 'protocol': 'TCP', 'host': 'localhost'},
        {'port': 22, 'service': 'SSH', 'protocol': 'TCP', 'host': 'localhost'},
    ]
    
    port_status = []
    open_count = 0
    
    for port_info in ports_to_check:
        is_open = check_port(port_info['port'], port_info['host'])
        status = 'Open' if is_open else 'Closed'
        
        if is_open:
            open_count += 1
        
        port_status.append({
            'port': port_info['port'],
            'service': port_info['service'],
            'status': status,
            'protocol': port_info['protocol']
        })
    
    return jsonify({
        'ports': port_status,
        'total': len(port_status),
        'open': open_count
    })

@app.route('/logs')
def get_logs():
    """Get recent logs from database"""
    try:
        logs = db.get_recent_logs(limit=50)
        return jsonify({
            'logs': logs,
            'count': len(logs)
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'logs': [],
            'count': 0
        })

@app.route('/docker-info')
def docker_info():
    """Get Docker system information"""
    if not docker_client:
        return jsonify({
            'error': 'Docker not available',
            'details': docker_error or 'Docker client not initialized'
        }), 200
    
    try:
        info = docker_client.info()
        return jsonify({
            'containers_total': info.get('Containers', 0),
            'containers_running': info.get('ContainersRunning', 0),
            'containers_paused': info.get('ContainersPaused', 0),
            'containers_stopped': info.get('ContainersStopped', 0),
            'images': info.get('Images', 0),
            'docker_version': info.get('ServerVersion', 'Unknown'),
            'os': info.get('OperatingSystem', 'Unknown'),
            'architecture': info.get('Architecture', 'Unknown')
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 200

# ==================== HELPER FUNCTIONS ====================

def check_nginx_status():
    """Check if NGINX container is running"""
    if not docker_client:
        return 'Unknown'
    
    try:
        # Try multiple common nginx container names
        nginx_patterns = ['nginx', 'nginx-frontend', 'frontend', 'tier2-app-nginx']
        
        for pattern in nginx_patterns:
            try:
                containers = docker_client.containers.list(
                    all=True,
                    filters={'name': pattern}
                )
                
                if containers:
                    for container in containers:
                        if container.status == 'running':
                            return 'Running'
                    return 'Stopped'
            except Exception as e:
                continue
        
        # If no nginx container found by name, check port 80
        if check_port(80, 'nginx'):
            return 'Running'
        
        return 'Not Found'
        
    except Exception as e:
        print(f"NGINX check error: {e}")
        return 'Unknown'

def check_docker_status():
    """Check if Docker daemon is accessible"""
    if not docker_client:
        return 'Not Available'
    
    try:
        docker_client.ping()
        return 'Running'
    except Exception as e:
        print(f"Docker ping error: {e}")
        return 'Error'

def check_port(port, host='localhost'):
    """Check if a port is open on a specific host"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # 2 second timeout
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Port check error for {host}:{port} - {e}")
        return False

# ==================== STARTUP ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Docker Status Tracker Backend Starting...")
    print("=" * 60)
    
    # Create database tables
    try:
        if db.create_tables():
            print("✅ Database tables created/verified")
        else:
            print("⚠️  Database setup issue (will retry on first request)")
    except Exception as e:
        print(f"⚠️  Database error: {e}")
    
    # Test Docker connection
    if docker_client:
        try:
            docker_client.ping()
            containers = docker_client.containers.list()
            print(f"✅ Docker daemon connected - {len(containers)} containers running")
        except Exception as e:
            print(f"⚠️  Docker connection issue: {e}")
    else:
        print("❌ Docker client not available")
        print("   Make sure to mount: -v /var/run/docker.sock:/var/run/docker.sock")
    
    # Check database
    db_status = db.check_connection()
    if db_status == 'Connected':
        print("✅ Database connected")
    else:
        print(f"⚠️  Database status: {db_status}")
    
    print("=" * 60)
    print("🌐 Flask server running on http://0.0.0.0:5000")
    print("=" * 60)
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
