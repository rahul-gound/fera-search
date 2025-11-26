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

### Deployment with Caddy (for fera-search.tech)

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