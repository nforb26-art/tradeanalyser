// API Base URL
const API_BASE = 'http://127.0.0.1:8000';

// DOM Elements
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
const analyzeBtn = document.getElementById('analyzeBtn');
const analysisSection = document.getElementById('analysisSection');
const errorMessage = document.getElementById('errorMessage');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    setupSearchListeners();
    setupAnalyzeButton();
});

// Setup analyze button
function setupAnalyzeButton() {
    analyzeBtn.addEventListener('click', () => {
        const query = searchInput.value.trim();
        if (query.length > 0) {
            handleAnalyze(query);
        } else {
            showError('Please enter a trading pair (e.g., BTC/USDT or BTC)');
        }
    });
}

// Setup search listeners
function setupSearchListeners() {
    searchInput.addEventListener('input', debounce(handleSearch, 300));
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const query = searchInput.value.trim();
            if (query.length > 0) {
                handleAnalyze(query);
            }
        }
    });
}

// Debounce function
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

// Handle analyze (new function)
async function handleAnalyze(query) {
    searchResults.innerHTML = '';
    
    try {
        // First get the crypto details
        const searchResponse = await fetch(`${API_BASE}/api/search/${encodeURIComponent(query)}`);
        const searchData = await searchResponse.json();

        if (!searchResponse.ok) {
            showError(`Pair not found: ${searchData.detail || 'Unknown error'}`);
            return;
        }

        if (searchData.results && searchData.results.length > 0) {
            // Use first result
            const result = searchData.results[0];
            selectCryptocurrency(result.id, query);
        } else {
            showError(`No results found for "${query}". Try BTC, ETH, or SOL.`);
        }
    } catch (error) {
        showError(`Error: ${error.message}`);
    }
}

// Handle search (for dropdown)
async function handleSearch() {
    const query = searchInput.value.trim();
    if (query.length < 1) {
        searchResults.innerHTML = '';
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/search/${encodeURIComponent(query)}`);
        const data = await response.json();

        if (!response.ok) {
            showError(`Search failed: ${data.detail || data.error || 'Unknown error'}`);
            searchResults.innerHTML = '';
            return;
        }

        if (data.success && data.results && data.results.length > 0) {
            displaySearchResults(data.results);
        } else {
            searchResults.innerHTML = '<div class="search-result-item">No results found - try "BTC", "ETH", "Bitcoin"</div>';
        }
    } catch (error) {
        console.error('Search error:', error);
        showError(`Search failed: ${error.message}`);
    }
}

// Display search results
function displaySearchResults(results) {
    searchResults.innerHTML = results.map(result => `
        <div class="search-result-item" onclick="selectCryptocurrency('${result.id}', '${result.symbol}')">
            <div class="search-result-name">${result.name}</div>
            <div class="search-result-symbol">${result.symbol}</div>
        </div>
    `).join('');
}

// Select cryptocurrency and analyze
async function selectCryptocurrency(cryptoId, symbol) {
    searchResults.innerHTML = '';
    searchInput.value = '';
    hideError();

    try {
        const response = await fetch(`${API_BASE}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                crypto_id: cryptoId,
                symbol: symbol
            })
        });

        const data = await response.json();

        if (!response.ok) {
            // Detailed error from backend
            const errorDetail = data.detail || data.error || 'Unknown error occurred';
            showError(`❌ Analysis Failed:\n\n${errorDetail}`);
            return;
        }

        if (data.success) {
            displayAnalysis(data);
            analysisSection.style.display = 'block';
            analysisSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            showError(`Analysis failed: ${data.detail || data.error || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Analysis error:', error);
        showError(`⚠️ Network Error:\n\n${error.message}\n\nMake sure:\n1. Backend server is running\n2. API is available at ${API_BASE}`);
    }
}

// Display analysis results
function displayAnalysis(data) {
    // Pair header
    document.getElementById('pairName').textContent = data.pair;
    document.getElementById('pairPrice').textContent = `$${data.current_price}`;
    
    const changeEl = document.getElementById('pairChange');
    const changeValue = parseFloat(data.change_24h);
    changeEl.textContent = `${changeValue >= 0 ? '+' : ''}${data.change_24h}`;
    changeEl.className = 'pair-change ' + (changeValue >= 0 ? 'positive' : 'negative');

    // Trading levels
    document.getElementById('entryPrice').textContent = `$${data.entry}`;
    document.getElementById('stoplossPrice').textContent = `$${data.stoploss}`;
    document.getElementById('takeprofitPrice').textContent = `$${data.takeprofit}`;

    // Volatility info
    document.getElementById('volatilityLevel').textContent = data.volatility || 'UNKNOWN';
    document.getElementById('volatilityPercent').textContent = `${data.volatility_percent}%`;
    document.getElementById('slPercentage').textContent = `${data.sl_percentage}%`;
    document.getElementById('tpPercentage').textContent = `${data.tp_percentage}%`;

    // Risk/Reward
    document.getElementById('rrRatio').textContent = data.risk_reward_ratio;

    // Sentiment consensus
    const sentiment = data.sentiment;
    const consensusEl = document.getElementById('consensusSentiment');
    if (sentiment.consensus) {
        consensusEl.textContent = sentiment.consensus;
        consensusEl.className = 'sentiment-value ' + sentiment.consensus.toLowerCase();
    }
    document.getElementById('consensusConfidence').textContent = `Confidence: ${sentiment.confidence}/10 (${sentiment.available_models} AI models)`;

    // Individual AI models
    displayAIModels(sentiment.models);

    // Market data
    const market = data.market_data;
    document.getElementById('marketCap').textContent = market.market_cap;
    document.getElementById('volume24h').textContent = market.volume_24h;
    document.getElementById('high24h').textContent = market.high_24h;
    document.getElementById('low24h').textContent = market.low_24h;
}

// Display individual AI model results
function displayAIModels(models) {
    const modelsContainer = document.getElementById('aiModels');
    if (!modelsContainer) return;
    
    let html = '<div class="ai-models-grid">';
    
    for (const [model, result] of Object.entries(models)) {
        const available = result.available !== false;
        const sentiment = result.sentiment || result.signal || 'N/A';
        const statusClass = available ? 'available' : 'unavailable';
        
        html += `
            <div class="ai-model ${statusClass}">
                <div class="model-name">${model.toUpperCase()}</div>
                <div class="model-status">${available ? '✓ Active' : '⊘ Unavailable'}</div>
                ${available ? `<div class="model-sentiment">${sentiment}</div>` : '<div class="model-error">API key not configured</div>'}
            </div>
        `;
    }
    
    html += '</div>';
    modelsContainer.innerHTML = html;
}

// Show error
function showError(message) {
    errorMessage.innerHTML = message.replace(/\n/g, '<br>');
    errorMessage.style.display = 'block';
    errorMessage.scrollIntoView({ behavior: 'smooth' });
}

// Hide error
function hideError() {
    errorMessage.style.display = 'none';
}
