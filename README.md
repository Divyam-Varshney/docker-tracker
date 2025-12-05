# 🐳 Docker Status Tracker - Complete DevOps Monitoring Dashboard

<div align="center">

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**A production-ready Docker monitoring dashboard with real-time container tracking, service health checks, and port monitoring**

[Features](#-features) • [Quick Start](#-quick-start-in-3-steps) • [Architecture](#-architecture) • [Troubleshooting](#-troubleshooting) • [API Docs](#-api-documentation)

![Dashboard Preview](https://img.shields.io/badge/Status-Production_Ready-brightgreen?style=for-the-badge)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start-in-3-steps)
- [Detailed Setup Guide](#-detailed-setup-guide)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [AWS Deployment](#-aws-deployment)
- [DevOps Concepts](#-devops-concepts-covered)
- [Contributing](#-contributing)

---

## 🌟 Overview

**Docker Status Tracker** is a comprehensive monitoring solution that provides real-time visibility into your Docker infrastructure. Built with a modern 3-tier architecture, it offers instant insights into container health, service status, and network ports.

### What Does It Monitor?

✅ **Docker Containers** - Track all running and stopped containers  
✅ **NGINX Status** - Monitor your web server health  
✅ **MySQL Database** - Check database connectivity  
✅ **Port Availability** - Real-time port status monitoring  
✅ **Docker Daemon** - Verify Docker engine status  
✅ **Historical Logs** - Track changes over time  

---

## ✨ Features

### Core Monitoring Features

- 🔴 **Real-time Container Tracking** - See all containers with status, ports, and images
- 🟢 **Live Service Health Checks** - Monitor NGINX, MySQL, and Docker daemon
- 🟡 **Port Monitoring** - Check which ports are open/closed on your system
- 🔵 **Auto-refresh Dashboard** - Updates every 15 seconds automatically
- ⚪ **Historical Logging** - MySQL-backed audit trail
- 🟣 **RESTful API** - Clean endpoints for integration

### Technical Features

- ⚡ **Fast & Lightweight** - Optimized Docker images
- 🔒 **Secure** - Minimal attack surface
- 📱 **Responsive UI** - Works on all devices
- 🎨 **Modern Design** - Dark theme, clean interface
- 🔧 **Easy Setup** - One-command deployment
- 📊 **Visual Dashboard** - Intuitive status cards

---

## 🏗️ Architecture

### 3-Tier Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                      CLIENT BROWSER                          │
│                    (http://localhost)                        │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    TIER-1: FRONTEND                          │
│  ┌────────────────────────────────────────────────────┐     │
│  │  NGINX (Alpine)                 Port: 80          │     │
│  │  - Serves Bootstrap 5 UI                          │     │
│  │  - Reverse Proxy to Backend                       │     │
│  │  - Static Content Server                          │     │
│  │  IP: 172.20.0.4                                   │     │
│  └────────────────────────────────────────────────────┘     │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    TIER-2: BACKEND                           │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Flask API (Python 3.11)        Port: 5000       │     │
│  │  - Docker SDK Integration                         │     │
│  │  - Real-time Status Checks                        │     │
│  │  - RESTful API Endpoints                         │     │
│  │  - Port Monitoring Logic                          │     │
│  │  IP: 172.20.0.3                                   │     │
│  │  Mounts: /var/run/docker.sock (read-only)        │     │
│  └────────────────────────────────────────────────────┘     │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    TIER-3: DATABASE                          │
│  ┌────────────────────────────────────────────────────┐     │
│  │  MySQL 8.0                      Port: 3306        │     │
│  │  - Status Logs Storage                            │     │
│  │  - Container History                              │     │
│  │  - Persistent Volume: mysql-data                  │     │
│  │  IP: 172.20.0.2                                   │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘

                    DOCKER BRIDGE NETWORK
            Network: devops-network (172.20.0.0/16)
```

---

## 📦 Prerequisites

### Required Software

| Software | Minimum Version | Check Command |
|----------|----------------|---------------|
| Docker | 20.10+ | `docker --version` |
| Docker Compose | 2.0+ | `docker-compose --version` |
| Git | 2.0+ | `git --version` |

### System Requirements

- **Operating System**: Linux, macOS, or Windows with WSL2
- **RAM**: Minimum 2GB available
- **Disk Space**: 2GB free space
- **CPU**: 2+ cores recommended

### Port Requirements

Ensure these ports are available:

- **80** - NGINX frontend
- **3306** - MySQL database
- **5000** - Flask backend (optional, for direct access)

---

## 🚀 Quick Start (In 3 Steps)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Divyam-Varshney/docker-tracker.git
cd docker-tracker
```

### Step 2: Start All Services

```bash
docker-compose up -d --build
```

This command will:
- Build all Docker images
- Create custom network
- Start MySQL, Flask, and NGINX containers
- Set up persistent storage

### Step 3: Access the Dashboard

Open your browser and go to:

```
http://localhost
```

**That's it! Your dashboard is now running!** 🎉

---

## 📋 Detailed Setup Guide

### Complete Installation Process

#### 1. **System Preparation**

```bash
# Update your system
sudo apt update && sudo apt upgrade -y  # For Ubuntu/Debian

# Install Docker (if not already installed)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# IMPORTANT: Logout and login again for changes to take effect
# Or run: newgrp docker
```

#### 2. **Clone and Setup Project**

```bash
# Clone repository
git clone https://github.com/Divyam-Varshney/docker-tracker.git

# Navigate to project directory
cd docker-tracker

# Verify project structure
ls -la
# You should see: backend/, frontend/, database/, docker-compose.yml
```

#### 3. **Configure Docker Socket Permissions**

```bash
# Check Docker socket permissions
ls -l /var/run/docker.sock

# If needed, give proper permissions
sudo chmod 666 /var/run/docker.sock

# Alternative (more secure): Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### 4. **Start the Application**

```bash
# Build and start all containers
docker-compose up -d --build

# The --build flag ensures fresh builds
# The -d flag runs containers in background (detached mode)
```

#### 5. **Verify Everything is Running**

```bash
# Check container status
docker-compose ps

# You should see 3 containers running:
# - mysql (healthy)
# - flask-backend (healthy)
# - nginx-frontend (healthy)

# View logs (optional)
docker-compose logs -f

# Press Ctrl+C to stop viewing logs
```

#### 6. **Test the Application**

```bash
# Test backend API
curl http://localhost:5000/health

# Expected output:
# {"api":"healthy","docker":"connected","database":"Connected"}

# Test frontend
curl http://localhost

# Open in browser
# http://localhost
```

---

## 📁 Project Structure

```
docker-tracker/
├── 📂 frontend/                    # Tier-1: NGINX Frontend
│   ├── 🐳 Dockerfile              # NGINX Alpine image config
│   ├── ⚙️  nginx.conf             # Reverse proxy configuration
│   └── 📂 html/
│       └── 🌐 index.html          # Dashboard UI (Bootstrap 5)
│
├── 📂 backend/                     # Tier-2: Flask Backend
│   ├── 🐳 Dockerfile              # Python Flask image config
│   ├── 📝 requirements.txt        # Python dependencies
│   ├── 🐍 app.py                  # Main Flask application
│   └── 🐍 db.py                   # MySQL database helper
│
├── 📂 database/                    # Tier-3: MySQL Database
│   ├── 📊 init.sql                # Database initialization script
│   └── 📖 README.md               # Database documentation
│
├── 🐳 docker-compose.yml           # Multi-container orchestration
├── 📝 README.md                    # This file
├── 📄 .gitignore                   # Git ignore rules
└── 📜 LICENSE                      # MIT License
```

### Key Files Explained

- **`docker-compose.yml`** - Defines all services, networks, and volumes
- **`backend/app.py`** - Flask REST API with Docker monitoring logic
- **`backend/db.py`** - MySQL connection and query helper functions
- **`frontend/nginx.conf`** - NGINX reverse proxy and static file serving
- **`frontend/html/index.html`** - React-like dashboard UI
- **`database/init.sql`** - Creates tables and initial data

---

## 📡 API Documentation

### Base URL

```
http://localhost/api
```

### Available Endpoints

#### 1. **Health Check** `GET /health`

Check if API is running and services are connected.

**Request:**
```bash
curl http://localhost/api/health
```

**Response:**
```json
{
  "api": "healthy",
  "docker": "connected",
  "database": "Connected",
  "timestamp": "2024-12-05T10:30:00"
}
```

---

#### 2. **System Status** `GET /status`

Get status of NGINX, MySQL, and Docker daemon.

**Request:**
```bash
curl http://localhost/api/status
```

**Response:**
```json
{
  "nginx_status": "Running",
  "db_status": "Connected",
  "docker_status": "Running",
  "timestamp": "2024-12-05T10:30:00"
}
```

---

#### 3. **Docker Containers** `GET /containers`

List all Docker containers with details.

**Request:**
```bash
curl http://localhost/api/containers
```

**Response:**
```json
{
  "containers": [
    {
      "name": "nginx-frontend",
      "image": "nginx:alpine",
      "status": "running",
      "ports": "80→80/tcp",
      "created": "2024-12-05",
      "id": "a1b2c3d4"
    },
    {
      "name": "flask-backend",
      "image": "python:3.11-slim",
      "status": "running",
      "ports": "5000→5000/tcp",
      "created": "2024-12-05",
      "id": "e5f6g7h8"
    }
  ],
  "total": 3,
  "running": 3
}
```

---

#### 4. **Port Status** `GET /ports`

Check status of important network ports.

**Request:**
```bash
curl http://localhost/api/ports
```

**Response:**
```json
{
  "ports": [
    {
      "port": 80,
      "service": "NGINX/HTTP",
      "status": "Open",
      "protocol": "TCP"
    },
    {
      "port": 3306,
      "service": "MySQL",
      "status": "Open",
      "protocol": "TCP"
    },
    {
      "port": 5000,
      "service": "Flask Backend",
      "status": "Open",
      "protocol": "TCP"
    }
  ],
  "total": 6,
  "open": 3
}
```

---

#### 5. **System Logs** `GET /logs`

Fetch recent system logs from database.

**Request:**
```bash
curl http://localhost/api/logs
```

**Response:**
```json
{
  "logs": [
    {
      "log_type": "system",
      "message": "NGINX:Running, DB:Connected, Docker:Running",
      "created_at": "2024-12-05T10:30:00"
    }
  ],
  "count": 50
}
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file (optional - defaults are set):

```env
# Database Configuration
DB_HOST=mysql
DB_USER=devops_user
DB_PASSWORD=devops_pass
DB_NAME=docker_tracker
DB_PORT=3306

# MySQL Root Password
MYSQL_ROOT_PASSWORD=root_password

# Flask Configuration
FLASK_ENV=production
PYTHONUNBUFFERED=1
```

### Changing Ports

Edit `docker-compose.yml`:

```yaml
services:
  nginx:
    ports:
      - "8080:80"  # Change 80 to 8080 for external access
  
  backend:
    ports:
      - "5001:5000"  # Change 5000 to 5001
  
  mysql:
    ports:
      - "3307:3306"  # Change 3306 to 3307
```

---

## 🐛 Troubleshooting

### Issue 1: "Docker socket permission denied"

**Symptoms:**
- Backend shows "Docker not available"
- Container list is empty

**Solution:**
```bash
# Option 1: Fix socket permissions (temporary)
sudo chmod 666 /var/run/docker.sock

# Option 2: Add user to docker group (permanent)
sudo usermod -aG docker $USER
newgrp docker

# Rebuild containers
docker-compose down
docker-compose up -d --build
```

---

### Issue 2: "Port already in use"

**Symptoms:**
```
Error: bind: address already in use
```

**Solution:**
```bash
# Find what's using the port
sudo lsof -i :80

# Stop the service
sudo systemctl stop apache2  # or nginx, or whatever is using it

# Or kill the process
sudo kill -9 <PID>

# Restart your containers
docker-compose restart
```

---

### Issue 3: "Database connection failed"

**Symptoms:**
- Database status shows "Disconnected"
- Backend can't connect to MySQL

**Solution:**
```bash
# Check if MySQL is healthy
docker-compose ps mysql

# Wait 30-60 seconds for MySQL to fully start
# MySQL needs time to initialize

# Check MySQL logs
docker-compose logs mysql

# If still failing, restart MySQL
docker-compose restart mysql

# Test connection manually
docker exec -it mysql mysql -u devops_user -pdevops_pass docker_tracker
```

---

### Issue 4: "Containers not showing up"

**Symptoms:**
- "No containers found" message
- Container count shows 0

**Solution:**
```bash
# Verify Docker socket is mounted
docker inspect flask-backend | grep docker.sock

# Check backend logs
docker-compose logs backend

# Restart backend with proper permissions
docker-compose down
docker-compose up -d --build

# Verify from inside container
docker exec -it flask-backend python -c "import docker; print(docker.from_env().containers.list())"
```

---

### Issue 5: "API shows disconnected"

**Symptoms:**
- Red "API Disconnected" badge
- No data loading

**Solution:**
```bash
# Check if all containers are running
docker-compose ps

# Test backend directly
curl http://localhost:5000/health

# Check nginx logs
docker-compose logs nginx

# Restart all services
docker-compose restart

# If still not working, rebuild everything
docker-compose down
docker-compose up -d --build
```

---

### Common Commands for Debugging

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# Check container status
docker-compose ps

# Restart a specific service
docker-compose restart backend

# Enter a container
docker exec -it flask-backend bash

# Check network connectivity
docker exec -it flask-backend ping mysql

# Test MySQL from backend
docker exec -it flask-backend python -c "from db import Database; print(Database().check_connection())"

# Full restart
docker-compose down
docker-compose up -d --build
```

---

## ☁️ AWS Deployment Guide

### Step-by-Step AWS EC2 Deployment

#### 1. **Launch EC2 Instance**

1. Go to **AWS Console** → EC2 → **Launch Instance**
2. Choose **Ubuntu 22.04 LTS** AMI
3. Select **t2.medium** (2 vCPU, 4GB RAM)
4. Configure **Security Group**:

```
Type            Protocol    Port    Source
SSH             TCP         22      My IP
HTTP            TCP         80      0.0.0.0/0
Custom TCP      TCP         5000    0.0.0.0/0 (optional)
MySQL           TCP         3306    My IP (optional)
```

#### 2. **Connect to Instance**

```bash
# Download your .pem key
chmod 400 your-key.pem

# SSH into instance
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

#### 3. **Install Docker**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose -y

# Add user to docker group
sudo usermod -aG docker ubuntu
newgrp docker

# Verify installation
docker --version
docker-compose --version
```

#### 4. **Deploy Application**

```bash
# Clone repository
git clone https://github.com/Divyam-Varshney/docker-tracker.git
cd docker-tracker

# Fix Docker socket permissions
sudo chmod 666 /var/run/docker.sock

# Start application
docker-compose up -d --build

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

#### 5. **Access Application**

```
http://<EC2_PUBLIC_IP>
```

#### 6. **Setup Auto-restart on Reboot**

```bash
# Enable Docker to start on boot
sudo systemctl enable docker

# Add to crontab
crontab -e

# Add this line:
@reboot cd /home/ubuntu/docker-tracker && docker-compose up -d
```

---

## 🎓 DevOps Concepts Covered

This project demonstrates 15+ key DevOps concepts:

### 1. Containerization (Docker)
- ✅ Multi-stage builds
- ✅ Image optimization
- ✅ Container networking
- ✅ Volume persistence
- ✅ Health checks

### 2. Orchestration (Docker Compose)
- ✅ Multi-container management
- ✅ Service dependencies
- ✅ Network configuration
- ✅ Environment variables

### 3. Networking
- ✅ Custom bridge networks
- ✅ Container DNS resolution
- ✅ Port mapping
- ✅ Reverse proxy (NGINX)

### 4. Database Management
- ✅ MySQL containerization
- ✅ Data persistence
- ✅ Initialization scripts
- ✅ Connection pooling

### 5. API Development
- ✅ RESTful architecture
- ✅ CORS handling
- ✅ Error handling
- ✅ JSON responses

### 6. System Monitoring
- ✅ Real-time status checks
- ✅ Port availability
- ✅ Service health checks
- ✅ Historical logging

### 7. Version Control (Git)
- ✅ Repository structure
- ✅ .gitignore best practices
- ✅ README documentation

### 8. Security
- ✅ Read-only socket mounts
- ✅ Non-root users (where possible)
- ✅ Environment variables
- ✅ Network isolation

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** this repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'feat: Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Commit Message Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Add new feature
fix: Fix bug
docs: Update documentation
style: Code formatting
refactor: Code refactoring
test: Add tests
chore: Maintenance
```

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024 Divyam Varshney

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 📞 Support & Contact

- **GitHub**: [@Divyam-Varshney](https://github.com/Divyam-Varshney)
- **Project**: [docker-tracker](https://github.com/Divyam-Varshney/docker-tracker)
- **Issues**: [Report Bug](https://github.com/Divyam-Varshney/docker-tracker/issues)

---

## 🙏 Acknowledgments

- Docker community
- Flask framework
- Bootstrap team
- NGINX project
- MySQL developers
- DevOps community

---

<div align="center">

**⭐ If you found this helpful, please star the repository!**

Made with ❤️ for the DevOps community

![Footer](https://img.shields.io/badge/Built_with-Docker_|_Flask_|_Bootstrap-blue?style=for-the-badge)

</div>
