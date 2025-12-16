# Quick Start Guide

Get fera-search running in 3 simple steps!

## Prerequisites

- Docker and Docker Compose installed
- (Optional) Google Gemini API key for AI search functionality

## Step 1: Clone the Repository

```bash
git clone https://github.com/rahul-gound/fera-search.git
cd fera-search
```

## Step 2: Start the Application

### Option A: With API Key (Full Functionality)

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your GEMINI_API_KEY
# Get your key at: https://makersuite.google.com/app/apikey
nano .env  # or use your favorite editor

# Start the application
docker compose up --build
```

### Option B: Without API Key (Testing Only)

```bash
# Start the application
docker compose up --build

# Note: Containers will start successfully, but search won't work
# You can still test the UI at http://localhost
```

## Step 3: Access the Application

Open your browser and go to:
- **Frontend**: http://localhost
- **Backend API**: http://localhost:5000/api/health

## Verify Everything Works

### Check Container Status

```bash
# In a new terminal window
docker ps

# You should see both containers running:
# - fera-backend
# - fera-frontend
```

### Test Health Endpoint

```bash
curl http://localhost:5000/api/health

# Expected response:
# {"status":"healthy","service":"fera-search"}
```

### Check Logs

```bash
# Backend logs
docker logs fera-backend

# Frontend logs
docker logs fera-frontend

# Follow logs in real-time
docker logs -f fera-backend
```

## Expected Output

When running `docker compose up --build`, you should see:

```
[+] Building ... 
 => [backend] ... 
 => [frontend] ...
[+] Running 2/2
 ✔ Container fera-backend   Started
 ✔ Container fera-frontend  Started

fera-backend   | [INFO] Starting gunicorn 22.0.0
fera-backend   | [INFO] Listening at: http://0.0.0.0:5000
fera-backend   | [INFO] Using worker: sync
fera-backend   | [INFO] Booting worker with pid: X
fera-backend   | [INFO] Booting worker with pid: Y

fera-frontend  | ... nginx: configuration file /etc/nginx/nginx.conf test is successful
fera-frontend  | ... nginx: configuration file /etc/nginx/nginx.conf test successful
```

**Key indicators of success:**
- No restart loops (containers don't stop and start repeatedly)
- Backend shows "Booting worker with pid"
- Frontend shows "nginx: configuration file ... test is successful"
- Both containers stay running

## Stop the Application

```bash
# Press Ctrl+C in the terminal running docker compose

# Or in another terminal:
docker compose down
```

## Troubleshooting

### Containers Keep Restarting?

This issue has been fixed! If you still experience it:

1. Pull the latest code: `git pull origin main`
2. Rebuild: `docker compose build --no-cache`
3. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed help

### Port Already in Use?

```bash
# Check what's using port 80
sudo lsof -i :80

# Check what's using port 5000
sudo lsof -i :5000

# Kill the process or edit docker-compose.yml to use different ports
```

### Search Not Working?

Make sure you have:
1. Created the `.env` file
2. Added your `GEMINI_API_KEY` to `.env`
3. Restarted the containers: `docker compose down && docker compose up`

## Next Steps

- Configure your Gemini API key for full functionality
- Explore the search interface at http://localhost
- Check out the API endpoints in [README.md](README.md)
- Customize the branding in `frontend/` directory

## Need Help?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- View full documentation in [README.md](README.md)
- Create an issue: https://github.com/rahul-gound/fera-search/issues

---

Enjoy using fera-search! 🔍✨
