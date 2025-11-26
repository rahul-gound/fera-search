# Fera Search 🔍

<p align="center">
  <img src="client/simple/src/brand/searxng.svg" alt="Fera Search Logo" width="120">
</p>

**Fera Search** is a privacy-respecting metasearch engine based on [SearXNG](https://github.com/searxng/searxng), featuring an orange-themed professional design and AI-powered summarization.

## About

This project is a customized fork of SearXNG, a free internet metasearch engine that aggregates results from various search services and databases. Users are neither tracked nor profiled.

## Features

- 🔒 **Privacy-respecting** metasearch engine
- 🚫 **No tracking** or profiling of users
- 🔍 **Aggregates results** from multiple search engines
- 🏠 **Self-hostable**
- ⚙️ **Highly configurable**
- 🎨 **Professional orange theme**
- 🤖 **AI-powered summarization** using Hugging Face

## Quick Start

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

3. Set up Hugging Face API token (for AI summarization):
   ```bash
   export HF_TOKEN="your_huggingface_token_here"
   ```

4. Run the development server:
   ```bash
   python -m searx.webapp
   ```

### Using AI Summarization

To use the AI summarization feature, prefix your query with `summarize:`:
```
summarize: The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building...
```

## Deploying on DigitalOcean

### Option 1: DigitalOcean Droplet (Recommended)

1. **Create a Droplet:**
   - Go to [DigitalOcean](https://cloud.digitalocean.com/)
   - Create a new Droplet with Ubuntu 22.04 LTS
   - Choose at least 1GB RAM / 1 CPU ($6/month)
   - Add your SSH key for access

2. **Connect to your Droplet:**
   ```bash
   ssh root@your_droplet_ip
   ```

3. **Install dependencies:**
   ```bash
   apt update && apt upgrade -y
   apt install -y python3 python3-pip python3-venv git
   ```

4. **Clone and setup Fera Search:**
   ```bash
   cd /opt
   git clone https://github.com/rahul-gound/fera-search.git
   cd fera-search
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure environment variables:**
   ```bash
   export HF_TOKEN="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"
   export SEARXNG_SECRET=$(openssl rand -hex 32)
   export SEARXNG_BASE_URL="https://fera-search.tech"
   ```

6. **Install and configure Caddy for SSL:**
   ```bash
   apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
   curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
   curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list
   apt update
   apt install caddy
   ```

7. **Create Caddyfile:**
   ```bash
   cat > /etc/caddy/Caddyfile << 'EOF'
   fera-search.tech {
       reverse_proxy localhost:8888
   }
   EOF
   ```

8. **Point your domain to DigitalOcean:**
   - In your domain registrar, set the A record for `fera-search.tech` to your Droplet's IP address

9. **Create a systemd service for Fera Search:**
   ```bash
   cat > /etc/systemd/system/fera-search.service << 'EOF'
   [Unit]
   Description=Fera Search
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/opt/fera-search
   Environment="HF_TOKEN=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"
   Environment="SEARXNG_SECRET=your_secret_key_here"
   Environment="SEARXNG_BASE_URL=https://fera-search.tech"
   ExecStart=/opt/fera-search/venv/bin/python -m searx.webapp
   Restart=always

   [Install]
   WantedBy=multi-user.target
   EOF
   ```

10. **Start services:**
    ```bash
    systemctl daemon-reload
    systemctl enable fera-search
    systemctl start fera-search
    systemctl restart caddy
    ```

11. **Verify it's running:**
    ```bash
    systemctl status fera-search
    curl http://localhost:8888
    ```

Your Fera Search instance should now be live at `https://fera-search.tech`!

### Option 2: DigitalOcean App Platform

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect your GitHub repository (`rahul-gound/fera-search`)
4. Configure:
   - **Run Command:** `python -m searx.webapp`
   - **HTTP Port:** 8888
   - **Environment Variables:**
     - `HF_TOKEN` = `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`
     - `SEARXNG_SECRET` = (generate a random string)
     - `SEARXNG_BASE_URL` = `https://your-app-name.ondigitalocean.app`
5. Deploy!

### Deployment with Caddy (Local/VPS)

Create a `Caddyfile` (default port is 8888, configurable in `searx/settings.yml`):
```
fera-search.tech {
    reverse_proxy localhost:8888
}
```

Run Caddy:
```bash
caddy run
```

### Using Make

You can also use the `make` command for common operations:

```bash
# Install dependencies
make install

# Run the application
make run
```

## Configuration

Configuration files are located in the `searx/settings.yml` file. See the [SearXNG Configuration Guide](https://docs.searxng.org/admin/settings/index.html) for detailed configuration options.

### Environment Variables

| Variable | Description |
|----------|-------------|
| `HF_TOKEN` | Hugging Face API token for AI summarization |
| `SEARXNG_SECRET` | Secret key for the instance |
| `SEARXNG_BASE_URL` | Public URL of the instance |

## Documentation

For comprehensive documentation, refer to the [SearXNG Documentation](https://docs.searxng.org/).

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.rst](CONTRIBUTING.rst) file for guidelines.

## License

This project is licensed under the GNU Affero General Public License (AGPL-3.0). See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [SearXNG](https://github.com/searxng/searxng) - The original project this fork is based on
- [Hugging Face](https://huggingface.co/) - AI model hosting and inference
- All the contributors to SearXNG