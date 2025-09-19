// Dark Web Search Tool - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchResults = document.getElementById('searchResults');
    const resultsContainer = document.getElementById('resultsContainer');
    const loadingSpinner = document.getElementById('loadingSpinner');

    if (searchForm) {
        searchForm.addEventListener('submit', handleSearch);
    }
});

async function handleSearch(event) {
    event.preventDefault();
    
    const searchQuery = document.getElementById('searchQuery').value.trim();
    if (!searchQuery) {
        alert('Please enter a search query');
        return;
    }

    // Show loading spinner
    showLoading();
    hideResults();

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `query=${encodeURIComponent(searchQuery)}`
        });

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Search error:', error);
        displayError('An error occurred while searching. Please try again.');
    } finally {
        hideLoading();
    }
}

function showLoading() {
    const loadingSpinner = document.getElementById('loadingSpinner');
    if (loadingSpinner) {
        loadingSpinner.style.display = 'block';
    }
}

function hideLoading() {
    const loadingSpinner = document.getElementById('loadingSpinner');
    if (loadingSpinner) {
        loadingSpinner.style.display = 'none';
    }
}

function showResults() {
    const searchResults = document.getElementById('searchResults');
    if (searchResults) {
        searchResults.style.display = 'block';
    }
}

function hideResults() {
    const searchResults = document.getElementById('searchResults');
    if (searchResults) {
        searchResults.style.display = 'none';
    }
}

function displayResults(data) {
    const resultsContainer = document.getElementById('resultsContainer');
    if (!resultsContainer) return;

    showResults();

    if (data.results && data.results.length > 0) {
        resultsContainer.innerHTML = data.results.map(result => `
            <div class="search-result">
                <h5><a href="${result.url}" class="search-result-title" target="_blank">${result.title}</a></h5>
                <div class="search-result-url">${result.url}</div>
                <p class="search-result-snippet">${result.snippet}</p>
            </div>
        `).join('');
    } else {
        resultsContainer.innerHTML = `
            <div class="alert alert-info">
                <h6>No results found</h6>
                <p>${data.message || 'No results found for your search query. Try different keywords.'}</p>
            </div>
        `;
    }
}

function displayError(message) {
    const resultsContainer = document.getElementById('resultsContainer');
    if (!resultsContainer) return;

    showResults();
    resultsContainer.innerHTML = `
        <div class="alert alert-danger">
            <h6>Search Error</h6>
            <p>${message}</p>
        </div>
    `;
}

// Utility function to escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}