# Troubleshooting Docker Issues

## Container Restart Loop (1 second off, 1 second on)

If your Docker containers are automatically starting and stopping repeatedly, here are common causes and solutions:

### 1. Check Container Logs

First, check what's causing the crash:

```bash
# View backend logs
docker logs fera-backend

# View frontend logs  
docker logs fera-frontend

# Follow logs in real-time
docker logs -f fera-backend
```

### 2. Common Issues and Solutions

#### Missing Dependencies

**Symptom**: Backend container crashes with "ModuleNotFoundError"

**Solution**: Rebuild the containers to ensure all dependencies are installed:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

#### Port Conflicts

**Symptom**: Container exits with "port already in use" or "address already in use"

**Solution**: Check if ports 80 or 5000 are already in use:
```bash
# Check what's using port 80
sudo lsof -i :80

# Check what's using port 5000
sudo lsof -i :5000

# Kill the process or change ports in docker-compose.yml
```

#### Insufficient Resources

**Symptom**: Container crashes without clear error messages

**Solution**: Check Docker resource limits:
```bash
# Check Docker stats
docker stats

# Increase Docker Desktop memory/CPU limits if needed (Docker Desktop -> Settings -> Resources)
```

#### Gunicorn Worker Timeout

**Symptom**: Backend crashes with timeout errors

**Solution**: The Dockerfile now includes proper worker configuration. If you still see issues, you can adjust:
- Edit `backend/Dockerfile` and increase `--timeout` value (currently 120 seconds)
- Rebuild: `docker-compose build backend`

### 3. Health Check Issues

If containers are marked as "unhealthy":

```bash
# Check health status
docker ps

# Disable health checks temporarily to test if that's the issue
# Comment out the healthcheck sections in docker-compose.yml
```

### 4. API Key Issues

**Note**: Missing GEMINI_API_KEY will NOT cause containers to crash. The containers will start successfully but return errors when you try to use the search functionality.

To configure your API key:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
docker-compose down
docker-compose up
```

### 5. Debug Mode

Run containers in foreground to see all logs:

```bash
docker-compose up --build
```

Or run containers individually:

```bash
# Backend only
cd backend
docker build -t fera-backend .
docker run -p 5000:5000 -e GEMINI_API_KEY=your_key fera-backend

# Frontend only
cd frontend
docker build -t fera-frontend .
docker run -p 80:80 fera-frontend
```

### 6. Clean Slate

If nothing works, completely reset Docker state:

```bash
# Stop and remove containers, networks, and volumes
docker-compose down -v

# Remove images
docker rmi fera-backend fera-frontend

# Clean Docker system
docker system prune -a

# Rebuild from scratch
docker-compose up --build
```

### 7. Check Docker Daemon

Ensure Docker daemon is running properly:

```bash
# Check Docker status
docker info

# Restart Docker daemon (Linux)
sudo systemctl restart docker

# Restart Docker Desktop (Mac/Windows)
# Use Docker Desktop GUI to restart
```

## Still Having Issues?

If you're still experiencing problems:

1. Check the GitHub issues: https://github.com/rahul-gound/fera-search/issues
2. Create a new issue with:
   - Full error logs from `docker logs fera-backend` and `docker logs fera-frontend`
   - Your OS and Docker version: `docker --version`
   - Output of `docker-compose config` to verify configuration
   - Steps to reproduce the issue
