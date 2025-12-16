# fera-search

A privacy-respecting, hackable metasearch engine powered by SearXNG.

## Features

- Privacy-focused search aggregation
- Docker-based deployment
- Ready for Cloudflare integration
- Easy local development setup

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Running Locally

1. Clone the repository:
```bash
git clone https://github.com/rahul-gound/fera-search.git
cd fera-search
```

2. Build and run with Docker Compose:
```bash
docker-compose up -d
```

3. Access the search engine at http://localhost:8080

### Environment Variables

Create a `.env` file in the root directory:

```env
SEARXNG_SECRET_KEY=your-secret-key-here
SEARXNG_BASE_URL=http://localhost:8080/
```

## Dependencies

All required Python dependencies including `sniffio` (required by `httpx-socks`) are listed in `requirements.txt` and automatically installed during Docker build.

## Deployment

### With Cloudflare

1. Build the Docker image:
```bash
docker build -t fera-search .
```

2. Run the container:
```bash
docker run -d -p 8080:8080 --name fera-search fera-search
```

3. Configure Cloudflare to point to your server on port 8080

## Troubleshooting

### ModuleNotFoundError: No module named 'sniffio'

This error has been fixed by explicitly including `sniffio` in requirements.txt. The `httpx-socks` package requires `sniffio` as a dependency.

If you still encounter this issue:
1. Rebuild the Docker image: `docker-compose build --no-cache`
2. Restart the containers: `docker-compose up -d`

## License

This project is based on SearXNG.