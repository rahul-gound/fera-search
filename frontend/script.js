const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : '/api';

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).classList.add('active');
    });
});

// Loading state
function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

// Summarize functionality
document.getElementById('summarize-btn').addEventListener('click', async () => {
    const text = document.getElementById('summarize-input').value.trim();
    
    if (!text) {
        alert('Please enter some text to summarize.');
        return;
    }
    
    if (text.length < 250) {
        alert('Please enter at least 250 characters for summarization.');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/summarize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('summary-text').textContent = data.summary;
            document.getElementById('summarize-result').classList.remove('hidden');
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        hideLoading();
    }
});

// Search & Answer functionality
document.getElementById('search-btn').addEventListener('click', async () => {
    const content = document.getElementById('content-input').value.trim();
    const query = document.getElementById('query-input').value.trim();
    
    if (!content || !query) {
        alert('Please enter both content and a question.');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content, query }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('answer-text').textContent = data.answer;
            document.getElementById('search-result').classList.remove('hidden');
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        hideLoading();
    }
});
