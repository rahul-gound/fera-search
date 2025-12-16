FROM searxng/searxng:latest

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install additional Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose port
EXPOSE 8080

# Run with granian
CMD ["python", "-m", "searx.webapp"]
