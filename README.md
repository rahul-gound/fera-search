# fera-summarizeAI

A Docker-based text summarization and search application powered by AI.

## Features

- **Text Summarization**: Summarize long texts into concise paragraphs
- **Search & Answer**: Ask questions about provided content and get AI-powered answers
- **Docker Deployment**: Easy localhost deployment with Docker Compose
- **Modern UI**: Clean, responsive interface with dark theme

## Quick Start

### Prerequisites

- Docker and Docker Compose installed on your machine
- Cohere API key (get one at https://cohere.com)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/rahul-gound/fera-search.git
   cd fera-search
   ```

2. Create a `.env` file with your Cohere API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your COHERE_API_KEY
   ```

3. Start the application:
   ```bash
   docker-compose up --build
   ```

4. Open your browser and navigate to:
   - Frontend: http://localhost
   - Backend API: http://localhost:5000

## API Endpoints

### Health Check
```
GET /api/health
```

### Summarize Text
```
POST /api/summarize
Content-Type: application/json

{
  "text": "Your long text here (minimum 250 characters)"
}
```

### Search & Answer
```
POST /api/search
Content-Type: application/json

{
  "content": "Your content here",
  "query": "Your question about the content"
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

- **Backend**: Python, Flask, Cohere API
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Docker, Nginx
- **AI**: Cohere API for summarization and text generation

## License

MIT License