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

3. Run the development server:
   ```bash
   python -m searx.webapp
   ```

### Using AI Summarization

To use the AI summarization feature, prefix your query with `summarize:`:
```
summarize: The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building...
```

The Hugging Face token is already configured in the code.

## Deploying on Appwrite

### Option 1: Appwrite Functions

1. **Create an Appwrite account:**
   - Go to [Appwrite Cloud](https://cloud.appwrite.io/) or self-host Appwrite
   - Create a new project

2. **Install Appwrite CLI:**
   ```bash
   npm install -g appwrite-cli
   appwrite login
   ```

3. **Initialize Appwrite Function:**
   ```bash
   appwrite init function
   ```

4. **Create `appwrite.json` in project root:**
   ```json
   {
     "projectId": "your-project-id",
     "functions": [
       {
         "name": "fera-search",
         "runtime": "python-3.9",
         "execute": ["any"],
         "entrypoint": "searx/webapp.py",
         "commands": "pip install -r requirements.txt"
       }
     ]
   }
   ```

5. **Deploy to Appwrite:**
   ```bash
   appwrite deploy function
   ```

### Option 2: Appwrite with Docker

1. **Create a `Dockerfile`:**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements.txt
   
   EXPOSE 8888
   CMD ["python", "-m", "searx.webapp"]
   ```

2. **Build and push to registry:**
   ```bash
   docker build -t fera-search:latest .
   docker tag fera-search:latest your-registry/fera-search:latest
   docker push your-registry/fera-search:latest
   ```

3. **Deploy on Appwrite Cloud or self-hosted Appwrite with Docker**

### Option 3: Deploy with Docker Compose (Self-hosted)

1. **Create `docker-compose.yml`:**
   ```yaml
   version: '3.8'
   services:
     fera-search:
       build: .
       ports:
         - "8888:8888"
       restart: always
   ```

2. **Run:**
   ```bash
   docker-compose up -d
   ```

### Deployment with Caddy (for SSL on fera-search.tech)

Create a `Caddyfile`:
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