FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies and Docker CLI
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    wget \
    curl \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (to verify socket access)
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh && \
    rm get-docker.sh

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY db.py .

# Create non-root user but add to docker group
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    usermod -aG docker appuser || true

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run as root (needed for Docker socket access)
USER root

# Run application
CMD ["python", "-u", "app.py"]
