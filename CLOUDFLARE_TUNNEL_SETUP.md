# Cloudflare Tunnel Setup Guide

This guide explains how to deploy Fera Search with Cloudflare Tunnel for secure HTTPS access without exposing ports or using a reverse proxy like Caddy or Nginx.

## Prerequisites

- A Cloudflare account
- A domain added to Cloudflare
- Docker and Docker Compose installed on your server
- Fera Search running (via `docker compose up -d`)

## Step 1: Install Cloudflare Tunnel (cloudflared)

### On Linux (Ubuntu/Debian)
```bash
# Download cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb

# Install it
sudo dpkg -i cloudflared-linux-amd64.deb
```

### On other systems
Visit https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation

## Step 2: Authenticate with Cloudflare

```bash
cloudflared tunnel login
```

This will open a browser window. Select your domain and authorize the tunnel.

## Step 3: Create a Tunnel

```bash
cloudflared tunnel create fera-search
```

This creates a tunnel and saves the credentials to `~/.cloudflared/`.

## Step 4: Configure the Tunnel

Create a configuration file at `~/.cloudflared/config.yml`:

```yaml
tunnel: <TUNNEL-ID-FROM-STEP-3>
credentials-file: /home/YOUR_USER/.cloudflared/<TUNNEL-ID>.json

ingress:
  - hostname: fera-search.tech
    service: http://localhost:8080
  - service: http_status:404
```

Replace:
- `<TUNNEL-ID-FROM-STEP-3>` with the tunnel ID from step 3
- `YOUR_USER` with your username
- `fera-search.tech` with your domain

## Step 5: Route DNS to the Tunnel

```bash
cloudflared tunnel route dns fera-search fera-search.tech
```

This creates a CNAME record pointing your domain to the tunnel.

## Step 6: Run the Tunnel

### Option A: Run in foreground (for testing)
```bash
cloudflared tunnel run fera-search
```

### Option B: Install as a service (recommended for production)
```bash
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

## Step 7: Access Your Site

Visit `https://fera-search.tech` (or your domain) - it should now be accessible with automatic HTTPS!

## Benefits of Cloudflare Tunnel

- **No port forwarding needed**: Keeps your server ports closed
- **Automatic HTTPS**: Free SSL certificates managed by Cloudflare
- **DDoS protection**: Built-in Cloudflare protection
- **Easy setup**: No need for reverse proxy configuration
- **Zero trust security**: Can add authentication layers if needed

## Troubleshooting

### Check tunnel status
```bash
cloudflared tunnel info fera-search
```

### View tunnel logs
```bash
sudo journalctl -u cloudflared -f
```

### List all tunnels
```bash
cloudflared tunnel list
```

### Delete a tunnel
```bash
cloudflared tunnel delete fera-search
```

## Docker Compose with Cloudflared (Optional)

You can also run cloudflared as a Docker container alongside Fera Search:

```yaml
services:
  fera-search:
    build: .
    image: fera-search:latest
    container_name: fera-search
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - SEARXNG_SECRET=change-this-to-a-random-secret-key
      - SEARXNG_BASE_URL=https://fera-search.tech
    volumes:
      - ./searx/settings.yml:/app/searx/settings.yml:ro

  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared
    restart: unless-stopped
    command: tunnel --no-autoupdate run
    environment:
      - TUNNEL_TOKEN=<YOUR_TUNNEL_TOKEN>
    depends_on:
      - fera-search
```

To get your tunnel token, run:
```bash
cloudflared tunnel token fera-search
```
