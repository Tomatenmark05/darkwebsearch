<script>
	import { onMount } from 'svelte';
	import { user } from './+layout.svelte';
	
	let searchQuery = '';
	let results = [];
	let loading = false;
	let error = '';
	
	const MANAGER_URL = 'http://localhost:5000';
	
	async function performSearch() {
		if (!searchQuery.trim()) return;
		
		loading = true;
		error = '';
		results = [];
		
		try {
			const response = await fetch(`${MANAGER_URL}/api/search`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ query: searchQuery })
			});
			
			if (!response.ok) {
				throw new Error('Search failed');
			}
			
			const data = await response.json();
			results = data.results || [];
			
			if (results.length === 0) {
				error = 'No results found. Try different keywords or start a crawl to gather more data.';
			}
		} catch (e) {
			error = 'Search service unavailable. Please try again later.';
			console.error('Search error:', e);
		} finally {
			loading = false;
		}
	}
	
	async function startCrawl() {
		if (!searchQuery.trim()) return;
		
		try {
			const response = await fetch(`${MANAGER_URL}/api/crawl/start`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ query: searchQuery })
			});
			
			if (response.ok) {
				alert('Crawl started! Results will appear in future searches.');
			} else {
				alert('Failed to start crawl. Please try again.');
			}
		} catch (e) {
			alert('Crawler service unavailable.');
		}
	}
	
	function handleKeyPress(event) {
		if (event.key === 'Enter') {
			performSearch();
		}
	}
</script>

<style>
	.search-container {
		background: white;
		padding: 2rem;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0,0,0,0.1);
		margin-bottom: 2rem;
		text-align: center;
	}
	
	.search-title {
		font-size: 2.5rem;
		margin-bottom: 0.5rem;
		color: #333;
		font-weight: 300;
	}
	
	.search-subtitle {
		color: #666;
		margin-bottom: 2rem;
		font-size: 1.1rem;
	}
	
	.search-box {
		display: flex;
		gap: 1rem;
		max-width: 600px;
		margin: 0 auto;
		align-items: center;
	}
	
	.search-input {
		flex: 1;
		padding: 1rem;
		border: 2px solid #ddd;
		border-radius: 25px;
		font-size: 1rem;
		outline: none;
		transition: border-color 0.3s;
	}
	
	.search-input:focus {
		border-color: #007bff;
	}
	
	.search-btn, .crawl-btn {
		padding: 1rem 1.5rem;
		border: none;
		border-radius: 25px;
		font-size: 1rem;
		cursor: pointer;
		font-weight: 500;
		transition: all 0.3s;
	}
	
	.search-btn {
		background: #007bff;
		color: white;
	}
	
	.search-btn:hover {
		background: #0056b3;
		transform: translateY(-1px);
	}
	
	.crawl-btn {
		background: #28a745;
		color: white;
	}
	
	.crawl-btn:hover {
		background: #1e7e34;
		transform: translateY(-1px);
	}
	
	.search-btn:disabled, .crawl-btn:disabled {
		opacity: 0.6;
		cursor: not-allowed;
		transform: none;
	}
	
	.results-container {
		background: white;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0,0,0,0.1);
		overflow: hidden;
	}
	
	.results-header {
		padding: 1rem 1.5rem;
		background: #f8f9fa;
		border-bottom: 1px solid #dee2e6;
		font-weight: 600;
		color: #495057;
	}
	
	.result-item {
		padding: 1.5rem;
		border-bottom: 1px solid #eee;
		transition: background-color 0.2s;
	}
	
	.result-item:hover {
		background: #f8f9fa;
	}
	
	.result-item:last-child {
		border-bottom: none;
	}
	
	.result-title {
		font-size: 1.2rem;
		font-weight: 600;
		color: #007bff;
		margin-bottom: 0.5rem;
		text-decoration: none;
	}
	
	.result-title:hover {
		text-decoration: underline;
	}
	
	.result-url {
		color: #28a745;
		font-size: 0.9rem;
		margin-bottom: 0.5rem;
		word-break: break-all;
	}
	
	.result-content {
		color: #666;
		line-height: 1.5;
		margin-bottom: 0.5rem;
	}
	
	.result-meta {
		font-size: 0.8rem;
		color: #888;
		display: flex;
		gap: 1rem;
	}
	
	.loading {
		text-align: center;
		padding: 3rem;
		color: #666;
		font-size: 1.1rem;
	}
	
	.error {
		text-align: center;
		padding: 2rem;
		color: #dc3545;
		background: #f8d7da;
		border: 1px solid #f5c6cb;
		border-radius: 4px;
		margin: 1rem 0;
	}
	
	.no-auth {
		text-align: center;
		padding: 3rem;
		background: white;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0,0,0,0.1);
	}
	
	.no-auth h2 {
		color: #666;
		margin-bottom: 1rem;
	}
	
	.no-auth p {
		color: #888;
		margin-bottom: 2rem;
	}
	
	.no-auth button {
		background: #007bff;
		color: white;
		border: none;
		padding: 1rem 2rem;
		border-radius: 4px;
		font-size: 1rem;
		cursor: pointer;
	}
	
	.features {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		gap: 1rem;
		margin-top: 2rem;
	}
	
	.feature {
		background: white;
		padding: 1.5rem;
		border-radius: 8px;
		box-shadow: 0 2px 10px rgba(0,0,0,0.1);
		text-align: center;
	}
	
	.feature h3 {
		color: #333;
		margin-bottom: 1rem;
	}
	
	.feature p {
		color: #666;
		line-height: 1.5;
	}
</style>

<div class="search-container">
	<h1 class="search-title">🔍 Darkweb Search</h1>
	<p class="search-subtitle">Search and analyze data from the dark web</p>
	
	<div class="search-box">
		<input 
			type="text" 
			class="search-input"
			placeholder="Enter your search query..."
			bind:value={searchQuery}
			on:keypress={handleKeyPress}
			disabled={loading}
		/>
		<button 
			class="search-btn" 
			on:click={performSearch}
			disabled={loading || !searchQuery.trim()}
		>
			{loading ? 'Searching...' : 'Search'}
		</button>
		<button 
			class="crawl-btn" 
			on:click={startCrawl}
			disabled={loading || !searchQuery.trim()}
		>
			Start Crawl
		</button>
	</div>
</div>

{#if error}
	<div class="error">
		{error}
	</div>
{/if}

{#if loading}
	<div class="results-container">
		<div class="loading">
			🔄 Searching the dark web...
		</div>
	</div>
{:else if results.length > 0}
	<div class="results-container">
		<div class="results-header">
			Found {results.length} results for "{searchQuery}"
		</div>
		{#each results as result}
			<div class="result-item">
				<a href={result.url} target="_blank" class="result-title">
					{result.title || 'Untitled'}
				</a>
				<div class="result-url">{result.url}</div>
				<div class="result-content">
					{result.content ? result.content.substring(0, 300) + '...' : 'No content preview available'}
				</div>
				<div class="result-meta">
					<span>Crawled: {new Date(result.crawled_at).toLocaleDateString()}</span>
					{#if result.category}
						<span>Category: {result.category}</span>
					{/if}
				</div>
			</div>
		{/each}
	</div>
{/if}

{#if !loading && results.length === 0 && !error && !searchQuery}
	<div class="features">
		<div class="feature">
			<h3>🕷️ Web Crawling</h3>
			<p>Advanced crawling capabilities with respect for robots.txt and rate limiting</p>
		</div>
		<div class="feature">
			<h3>📊 Data Analysis</h3>
			<p>AI-powered analysis including sentiment analysis and content categorization</p>
		</div>
		<div class="feature">
			<h3>🔍 Smart Search</h3>
			<p>Intelligent search with caching and comprehensive result ranking</p>
		</div>
		<div class="feature">
			<h3>🔐 Secure Access</h3>
			<p>Authentication powered by Supabase for secure access to search results</p>
		</div>
	</div>
{/if}