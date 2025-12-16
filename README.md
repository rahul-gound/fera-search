# Fera Search

<p align="center">
  <img src="client/simple/src/brand/searxng.svg" alt="Fera Search Logo" width="200">
</p>

**Fera Search** is a privacy-respecting metasearch engine based on SearXNG, featuring an orange-themed professional design and AI-powered summarization.

## About

This project is a customized fork of SearXNG, a free internet metasearch engine that aggregates results from various search services and databases. Users are neither tracked nor profiled.

## Features

- Privacy-respecting metasearch engine
- No tracking or profiling of users  
- Aggregates results from multiple search engines
- Self-hostable with Docker
- Highly configurable
- Professional orange theme
- Fera-SummarizeAI: AI-powered summarization using Cohere

## Quick Start with Docker (Recommended)

### Deploy on Oracle Cloud / Any Docker Host

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rahul-gound/fera-search.git
   cd fera-search
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **Access Fera Search at:** `http://your-server-ip:8080`

### Build Docker Image Manually

```bash
# Build the image
docker build -t fera-search:latest .

# Run the container
docker run -d -p 8080:8080 --name fera-search fera-search:latest
```

### Deploy with SSL (HTTPS) using Cloudflare Tunnel

For production deployment with automatic SSL using Cloudflare Tunnel:

**Quick Setup:**

1. Install Cloudflare Tunnel (cloudflared) on your server
2. Authenticate and create a tunnel:
   ```bash
   cloudflared tunnel login
   cloudflared tunnel create fera-search
   ```
3. Configure the tunnel to point to your local service:
   ```bash
   cloudflared tunnel route dns fera-search fera-search.tech
   ```
4. Run cloudflared alongside your Docker container:
   ```bash
   cloudflared tunnel run fera-search
   ```

**For detailed setup instructions, see [CLOUDFLARE_TUNNEL_SETUP.md](CLOUDFLARE_TUNNEL_SETUP.md)**

Cloudflare Tunnel provides automatic SSL/TLS, DDoS protection, and eliminates the need for a reverse proxy like Caddy or Nginx.

## Local Development

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rahul-gound/fera-search.git
   cd fera-search
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   python -m searx.webapp
   ```

## Fera-SummarizeAI

Fera-SummarizeAI provides AI-powered text summarization using Cohere API. To use the summarization feature, prefix your query with `summarize:`:
```
summarize: The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building...
```

The Cohere API key is already configured in the code.

## Configuration

Configuration files are located in the `searx/settings.yml` file. See the SearXNG Configuration Guide for detailed configuration options.

### Environment Variables

| Variable | Description |
|----------|-------------|
| `SEARXNG_SECRET` | Secret key for the instance |
| `SEARXNG_BASE_URL` | Public URL of the instance |

## File Structure for Customization

To customize logos and images:

| File | Description |
|------|-------------|
| `client/simple/src/brand/searxng.svg` | Main logo |
| `client/simple/src/brand/searxng-wordmark.svg` | Wordmark logo |
| `searx/static/themes/simple/img/favicon.png` | Favicon |
| `searx/static/themes/simple/img/searxng.png` | Search page logo |

## License

This project is licensed under the GNU Affero General Public License (AGPL-3.0). See the LICENSE file for details.

## Acknowledgments

- SearXNG - The original project this fork is based on
- Cohere - AI-powered summarization for Fera-SummarizeAI