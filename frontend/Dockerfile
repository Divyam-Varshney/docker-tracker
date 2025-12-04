# Stage 1: Build stage (dependencies install karne ke liye)
FROM python:3.11-slim AS builder

WORKDIR /app

# System dependencies install karo (Docker SDK ke liye)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies install karo
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Distroless runtime (minimal, secure)
FROM gcr.io/distroless/python3-debian12

# Python packages builder stage se copy karo
COPY --from=builder /root/.local /root/.local

# Application code copy karo
WORKDIR /app
COPY app.py .
COPY db.py .

# Python path set karo
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/root/.local/lib/python3.11/site-packages

# Port expose karo
EXPOSE 5000

# Non-root user ke permission (distroless mein default non-root hota hai)
# Flask app start karo
CMD ["app.py"]
