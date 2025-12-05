import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Gemini client
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
model = None

def get_gemini_model():
    """Get or initialize the Gemini model."""
    global model
    if model is None and GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
    return model


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'fera-search'})


@app.route('/api/search', methods=['POST'])
def search():
    """Search using Gemini API - Google-like search experience."""
    try:
        gemini = get_gemini_model()
        if gemini is None:
            return jsonify({'error': 'Gemini API key not configured'}), 500
        
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'No search query provided'}), 400
        
        # Use Gemini to generate a comprehensive search response
        prompt = f"""You are a helpful search assistant. Provide a comprehensive, well-structured answer to this search query. 
Include relevant information, facts, and explanations. Format your response clearly with sections if needed.

Search Query: {query}

Provide a helpful and informative response:"""

        response = gemini.generate_content(prompt)
        
        return jsonify({
            'query': query,
            'result': response.text,
            'service': 'fera-search'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/suggest', methods=['POST'])
def suggest():
    """Get search suggestions using Gemini API."""
    try:
        gemini = get_gemini_model()
        if gemini is None:
            return jsonify({'error': 'Gemini API key not configured'}), 500
        
        data = request.get_json()
        query = data.get('query', '')
        
        if not query or len(query) < 2:
            return jsonify({'suggestions': []})
        
        # Use Gemini to generate search suggestions
        prompt = f"""Generate 5 relevant search suggestions for this partial query: "{query}"
Return only the suggestions, one per line, no numbering or bullet points."""

        response = gemini.generate_content(prompt)
        suggestions = [s.strip() for s in response.text.strip().split('\n') if s.strip()][:5]
        
        return jsonify({
            'suggestions': suggestions
        })
    
    except Exception as e:
        return jsonify({'suggestions': []})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
