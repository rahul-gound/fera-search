import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import cohere
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Cohere client
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
co = None

def get_cohere_client():
    """Get or initialize the Cohere client."""
    global co
    if co is None and COHERE_API_KEY:
        co = cohere.Client(COHERE_API_KEY)
    return co


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'fera-summarizeAI'})


@app.route('/api/summarize', methods=['POST'])
def summarize():
    """Summarize the provided text using Cohere API."""
    try:
        client = get_cohere_client()
        if client is None:
            return jsonify({'error': 'Cohere API key not configured'}), 500
        
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if len(text) < 250:
            return jsonify({'error': 'Text must be at least 250 characters for summarization'}), 400
        
        # Use Cohere summarize endpoint
        response = client.summarize(
            text=text,
            length='medium',
            format='paragraph',
            model='summarize-xlarge',
            extractiveness='medium',
            temperature=0.3
        )
        
        return jsonify({
            'summary': response.summary,
            'service': 'fera-summarizeAI'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['POST'])
def search_and_summarize():
    """Search through provided content and summarize results."""
    try:
        client = get_cohere_client()
        if client is None:
            return jsonify({'error': 'Cohere API key not configured'}), 500
        
        data = request.get_json()
        query = data.get('query', '')
        content = data.get('content', '')
        
        if not query or not content:
            return jsonify({'error': 'Both query and content are required'}), 400
        
        # Use Cohere to generate a response based on the query and content
        response = client.generate(
            model='command',
            prompt=f"Based on the following content, answer this question: {query}\n\nContent: {content}\n\nAnswer:",
            max_tokens=300,
            temperature=0.5
        )
        
        return jsonify({
            'answer': response.generations[0].text.strip(),
            'query': query,
            'service': 'fera-summarizeAI'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
