const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : '/api';

// Safe Mode state
let safeMode = 'on'; // 'off', 'on', 'strict'

// DOM Elements
const homeContainer = document.getElementById('home-container');
const resultsContainer = document.getElementById('results-container');
const searchInput = document.getElementById('search-input');
const resultsSearchInput = document.getElementById('results-search-input');
const searchBtn = document.getElementById('search-btn');
const clearBtn = document.getElementById('clear-btn');
const suggestionsBox = document.getElementById('suggestions');
const searchResults = document.getElementById('search-results');
const resultsQuery = document.getElementById('results-query');
const backHome = document.getElementById('back-home');
const loading = document.getElementById('loading');

// Settings Modal Elements
const settingsBtn = document.getElementById('settings-btn');
const resultsSettingsBtn = document.getElementById('results-settings-btn');
const settingsModal = document.getElementById('settings-modal');
const modalOverlay = document.getElementById('modal-overlay');
const modalClose = document.getElementById('modal-close');
const safeModeOptions = document.querySelectorAll('.safe-mode-option');
const safeModeStatus = document.getElementById('safe-mode-status');
const resultsSafeModeStatus = document.getElementById('results-safe-mode-status');

// Load saved settings
function loadSettings() {
    const savedSafeMode = localStorage.getItem('safeMode');
    if (savedSafeMode) {
        safeMode = savedSafeMode;
    }
    updateSafeModeUI();
}

// Update Safe Mode UI
function updateSafeModeUI() {
    // Update status indicators
    const statusText = safeMode.charAt(0).toUpperCase() + safeMode.slice(1);
    safeModeStatus.textContent = statusText;
    resultsSafeModeStatus.textContent = statusText;
    
    // Update modal buttons
    safeModeOptions.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === safeMode);
    });
}

// Show/hide settings modal
function showSettings() {
    settingsModal.classList.remove('hidden');
}

function hideSettings() {
    settingsModal.classList.add('hidden');
}

// Show/hide loading
function showLoading() {
    loading.classList.remove('hidden');
}

function hideLoading() {
    loading.classList.add('hidden');
}

// Switch to results view
function showResults(query, result) {
    homeContainer.classList.add('hidden');
    resultsContainer.classList.remove('hidden');
    resultsSearchInput.value = query;
    resultsQuery.textContent = `Results for: "${query}"`;
    
    // Format the result with markdown-like parsing
    searchResults.innerHTML = formatResult(result);
}

// Switch to home view
function showHome() {
    resultsContainer.classList.add('hidden');
    homeContainer.classList.remove('hidden');
    searchInput.value = '';
    searchInput.focus();
}

// Format result text with basic markdown support
function formatResult(text) {
    // Escape HTML
    let formatted = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    
    // Headers
    formatted = formatted.replace(/^### (.*$)/gm, '<h3>$1</h3>');
    formatted = formatted.replace(/^## (.*$)/gm, '<h2>$1</h2>');
    formatted = formatted.replace(/^# (.*$)/gm, '<h1>$1</h1>');
    
    // Bold
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Code
    formatted = formatted.replace(/`(.*?)`/g, '<code>$1</code>');
    
    // Lists
    formatted = formatted.replace(/^\* (.*$)/gm, '<li>$1</li>');
    formatted = formatted.replace(/^- (.*$)/gm, '<li>$1</li>');
    formatted = formatted.replace(/^\d+\. (.*$)/gm, '<li>$1</li>');
    
    // Paragraphs
    formatted = formatted.replace(/\n\n/g, '</p><p>');
    formatted = '<p>' + formatted + '</p>';
    
    // Clean up empty paragraphs
    formatted = formatted.replace(/<p><\/p>/g, '');
    formatted = formatted.replace(/<p>(<h[123]>)/g, '$1');
    formatted = formatted.replace(/(<\/h[123]>)<\/p>/g, '$1');
    formatted = formatted.replace(/<p>(<li>)/g, '<ul>$1');
    formatted = formatted.replace(/(<\/li>)<\/p>/g, '$1</ul>');
    
    return formatted;
}

// Perform search
async function performSearch(query) {
    if (!query.trim()) {
        alert('Please enter a search query.');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query, safeMode }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showResults(query, data.result);
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        hideLoading();
    }
}

// Get suggestions
let suggestionTimeout;
async function getSuggestions(query) {
    if (!query || query.length < 2) {
        suggestionsBox.classList.add('hidden');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/suggest`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
        });
        
        const data = await response.json();
        
        if (data.suggestions && data.suggestions.length > 0) {
            suggestionsBox.innerHTML = data.suggestions.map(s => {
                // Escape HTML in suggestion text to prevent XSS
                const escaped = s.replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;')
                    .replace(/'/g, '&#039;');
                return `
                <div class="suggestion-item">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"></circle>
                        <path d="M21 21l-4.35-4.35"></path>
                    </svg>
                    <span>${escaped}</span>
                </div>
            `}).join('');
            suggestionsBox.classList.remove('hidden');
            
            // Add click handlers to suggestions
            document.querySelectorAll('.suggestion-item').forEach(item => {
                item.addEventListener('click', () => {
                    searchInput.value = item.querySelector('span').textContent;
                    suggestionsBox.classList.add('hidden');
                    performSearch(searchInput.value);
                });
            });
        } else {
            suggestionsBox.classList.add('hidden');
        }
    } catch (error) {
        suggestionsBox.classList.add('hidden');
    }
}

// Event Listeners - Settings
settingsBtn.addEventListener('click', showSettings);
resultsSettingsBtn.addEventListener('click', showSettings);
modalOverlay.addEventListener('click', hideSettings);
modalClose.addEventListener('click', hideSettings);

safeModeOptions.forEach(btn => {
    btn.addEventListener('click', () => {
        safeMode = btn.dataset.mode;
        localStorage.setItem('safeMode', safeMode);
        updateSafeModeUI();
    });
});

// Event Listeners - Search
searchInput.addEventListener('input', (e) => {
    const value = e.target.value;
    clearBtn.classList.toggle('hidden', !value);
    
    clearTimeout(suggestionTimeout);
    suggestionTimeout = setTimeout(() => getSuggestions(value), 300);
});

searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        suggestionsBox.classList.add('hidden');
        performSearch(searchInput.value);
    }
});

searchInput.addEventListener('focus', () => {
    if (searchInput.value.length >= 2) {
        getSuggestions(searchInput.value);
    }
});

document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-box')) {
        suggestionsBox.classList.add('hidden');
    }
});

clearBtn.addEventListener('click', () => {
    searchInput.value = '';
    clearBtn.classList.add('hidden');
    suggestionsBox.classList.add('hidden');
    searchInput.focus();
});

searchBtn.addEventListener('click', () => {
    suggestionsBox.classList.add('hidden');
    performSearch(searchInput.value);
});

resultsSearchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        performSearch(resultsSearchInput.value);
    }
});

backHome.addEventListener('click', showHome);

// Initialize
loadSettings();
searchInput.focus();
