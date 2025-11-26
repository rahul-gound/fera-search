# Fera Search

Fera Search is a privacy-respecting metasearch engine based on [SearXNG](https://github.com/searxng/searxng).

## About

This project is a fork of SearXNG, a free internet metasearch engine that aggregates results from various search services and databases. Users are neither tracked nor profiled.

## Features

- Privacy-respecting metasearch engine
- No tracking or profiling of users
- Aggregates results from multiple search engines
- Self-hostable
- Highly configurable

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

## Documentation

For comprehensive documentation, refer to the [SearXNG Documentation](https://docs.searxng.org/).

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.rst](CONTRIBUTING.rst) file for guidelines.

## License

This project is licensed under the GNU Affero General Public License (AGPL-3.0). See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [SearXNG](https://github.com/searxng/searxng) - The original project this fork is based on
- All the contributors to SearXNG