# Fera Search - Privacy-Respecting Metasearch Engine
# Docker image for easy deployment on Oracle Cloud, DigitalOcean, or any Docker host

FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt requirements-server.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt -r requirements-server.txt

# Copy the rest of the application
COPY . .

# Create non-root user for security
RUN useradd -m -s /bin/bash ferasearch && \
    chown -R ferasearch:ferasearch /app

# Switch to non-root user
USER ferasearch

# Expose port
EXPOSE 8080

# Environment variables
ENV SEARXNG_SETTINGS_PATH=/app/searx/settings.yml
ENV SEARXNG_SECRET=ferasearch-secret-key-change-me

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/healthz')" || exit 1

# Run the application with Granian (production WSGI server)
CMD ["python", "-m", "granian", "--interface", "wsgi", "--host", "0.0.0.0", "--port", "8080", "searx.webapp:app"]
