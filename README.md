# fera-search

A Google-like AI-powered search engine using Google Gemini API.

## Features

- **AI Search**: Get comprehensive answers to any search query
- **Search Suggestions**: Real-time AI-powered search suggestions
- **Google-like Interface**: Clean, familiar search experience
- **Docker Deployment**: Easy localhost deployment with Docker Compose
- **Modern UI**: Beautiful dark theme with responsive design

## Quick Start

See [QUICKSTART.md](QUICKSTART.md) for a step-by-step guide to get running in 3 minutes!

### Prerequisites

- Docker and Docker Compose installed on your machine
- Google Gemini API key (get one at https://makersuite.google.com/app/apikey)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/rahul-gound/fera-search.git
   cd fera-search
   ```

2. Create a `.env` file with your Gemini API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```
   
   **Note**: If you don't configure the API key, the containers will still start but search functionality won't work. The application will return an error when you try to search.

3. Start the application:
   ```bash
   docker-compose up --build
   ```

4. Open your browser and navigate to:
   - Frontend: http://localhost
   - Backend API: http://localhost:5000

## Troubleshooting

If you experience any issues with Docker containers (e.g., containers restarting repeatedly), please see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed debugging steps.

## API Endpoints

### Health Check
```
GET /api/health
```

### Search
```
POST /api/search
Content-Type: application/json

{
  "query": "Your search query"
}
```

### Get Suggestions
```
POST /api/suggest
Content-Type: application/json

{
  "query": "Partial search query"
}
```

## Project Structure

```
fera-search/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend Docker image
├── frontend/
│   ├── index.html          # Main HTML page
│   ├── styles.css          # Styling
│   ├── script.js           # Frontend JavaScript
│   ├── nginx.conf          # Nginx configuration
│   └── Dockerfile          # Frontend Docker image
├── docker-compose.yml      # Docker Compose configuration
├── .env.example            # Example environment variables
└── README.md               # This file
```

## Technology Stack

- **Backend**: Python, Flask, Google Gemini API
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Docker, Nginx
- **AI**: Google Gemini Pro for search and suggestions

## License

MIT License