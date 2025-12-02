<script>
  let query = '';
  let loading = false;
  let results = [];
  let error = null;
  let connectionStatus = 'INITIALIZING';
  let packetCount = 0;
  let encryptionLevel = 'AES-256';
  
  // Search history
  let searchHistory = [
    "TOR NETWORK",
    "ONION ROUTING",
    "END-TO-END ENCRYPTION",
    "ZERO-KNOWLEDGE PROOFS",
    "QUANTUM RESISTANCE"
  ];
  
  // Connection simulation
  function simulateConnection() {
    const protocols = ['TCP_HANDSHAKE', 'TLS_NEGOTIATION', 'ENCRYPTION_LAYER', 'ROUTING_ESTABLISHED'];
    let i = 0;
    
    const interval = setInterval(() => {
      connectionStatus = protocols[i];
      packetCount += Math.floor(Math.random() * 50) + 10;
      i++;
      
      if (i >= protocols.length) {
        clearInterval(interval);
        connectionStatus = 'SECURE_CONNECTION_ESTABLISHED';
      }
    }, 400);
  }
  
  // Execute search
  async function executeSearch() {
    if (!query.trim()) return;
    
    loading = true;
    error = null;
    results = [];
    packetCount = 0;
    
    // Start connection simulation
    simulateConnection();
    
    try {
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-Request-ID': generateId(),
          'X-Encryption': encryptionLevel
        },
        body: JSON.stringify({ 
          query: query.trim(),
          protocol: 'TORv3',
          timestamp: Date.now()
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      if (data.error) {
        throw new Error(`SERVER: ${data.error}`);
      }
      
      results = data.results || [];
      
      // Update history
      if (!searchHistory.includes(query.trim().toUpperCase())) {
        searchHistory = [query.trim().toUpperCase(), ...searchHistory.slice(0, 7)];
      }
      
    } catch (err) {
      error = `[ERROR] ${err.message}`;
      connectionStatus = 'CONNECTION_FAILED';
    } finally {
      loading = false;
      if (!error) {
        connectionStatus = 'READY';
      }
    }
  }
  
  // Utility functions
  function generateId() {
    const chars = '0123456789ABCDEF';
    let id = '';
    for (let i = 0; i < 16; i++) {
      id += chars[Math.floor(Math.random() * chars.length)];
    }
    return id;
  }
  
  function loadFromHistory(item) {
    query = item;
    executeSearch();
  }
  
  function clearInterface() {
    query = '';
    results = [];
    error = null;
    connectionStatus = 'STANDBY';
  }
  
  function handleKeyPress(e) {
    if (e.key === 'Enter' && !loading && query.trim()) {
      executeSearch();
    }
    if (e.key === 'Escape') {
      clearInterface();
    }
    if (e.key === 'Tab' && query.trim()) {
      e.preventDefault();
      // Simple auto-complete
      const match = searchHistory.find(h => 
        h.toLowerCase().startsWith(query.toLowerCase())
      );
      if (match) query = match;
    }
  }
  
  // Initialize
  setTimeout(() => {
    connectionStatus = 'SYSTEM_READY';
  }, 1000);
</script>

<div class="terminal-interface">
  <!-- System Header -->
  <header class="system-header">
    <div class="header-left">
      <div class="system-id">
        <span class="prompt">&gt;&gt;</span>
        <span class="system-name">DARKWEB_BROWSER</span>
        <span class="system-version">[v1.0.3]</span>
      </div>
      <div class="system-status">
        <span class="status-label">STATUS:</span>
        <span class="status-value {connectionStatus === 'READY' ? 'active' : ''}">
          {connectionStatus}
        </span>
      </div>
    </div>
    
    <div class="header-right">
      <div class="system-metrics">
        <div class="metric">
          <span class="metric-label">PACKETS:</span>
          <span class="metric-value">{packetCount}</span>
        </div>
        <div class="metric">
          <span class="metric-label">ENCRYPTION:</span>
          <span class="metric-value">{encryptionLevel}</span>
        </div>
        <div class="metric">
          <span class="metric-label">TIME:</span>
          <span class="metric-value">{new Date().toLocaleTimeString('de-DE', {hour12: false})}</span>
        </div>
      </div>
    </div>
  </header>
  
  <!-- Connection Monitor -->
  <div class="connection-monitor">
    <div class="monitor-bar">
      <div class="progress-track">
        <div 
          class="progress-indicator" 
          class:active={loading}
          style={`width: ${loading ? '100%' : '0%'}`}
        ></div>
      </div>
      <div class="protocol-info">
        <span>PROTOCOL: TOR/ONION</span>
        <span>LATENCY: {loading ? '<CALCULATING>' : '<STANDBY>'}</span>
        <span>NODES: {loading ? '3' : '0'}</span>
      </div>
    </div>
  </div>
  
  <!-- Main Interface -->
  <main class="main-interface">
    <!-- Query Section -->
    <section class="query-section">
      <div class="section-header">
        <span class="section-title">[QUERY_INTERFACE]</span>
        <span class="section-help">[TAB: AUTOCOMPLETE | ESC: CLEAR | ENTER: EXECUTE]</span>
      </div>
      
      <div class="input-container">
        <div class="input-prompt">
          <span class="cursor">_</span>
          <span class="prompt-text">SEARCH&gt;</span>
        </div>
        
        <input
          type="text"
          bind:value={query}
          on:keydown={handleKeyPress}
          placeholder="ENTER SEARCH PARAMETERS..."
          class="terminal-input"
          disabled={loading}
          spellcheck="false"
          autocorrect="off"
          autocomplete="off"
        />
        
        <div class="input-actions">
          <button
            on:click={executeSearch}
            class="action-button execute"
            disabled={loading || !query.trim()}
            title="Execute Query"
          >
            <span class="button-label">EXECUTE</span>
            <span class="button-hint">[ENTER]</span>
          </button>
          
          <button
            on:click={clearInterface}
            class="action-button clear"
            title="Clear Interface"
          >
            <span class="button-label">CLEAR</span>
            <span class="button-hint">[ESC]</span>
          </button>
        </div>
      </div>
      
      <!-- Search History -->
      {#if searchHistory.length > 0}
        <div class="history-section">
          <div class="history-header">
            <span class="history-title">[QUERY_HISTORY]</span>
            <span class="history-count">({searchHistory.length} ENTRIES)</span>
          </div>
          <div class="history-grid">
            {#each searchHistory as item}
              <button
                on:click={() => loadFromHistory(item)}
                class="history-item"
                title={`Load: ${item}`}
              >
                <span class="item-prefix">&gt;</span>
                <span class="item-text">{item}</span>
              </button>
            {/each}
          </div>
        </div>
      {/if}
    </section>
    
    <!-- Results Section -->
    <section class="results-section">
      <div class="section-header">
        <span class="section-title">[RESULTS_OUTPUT]</span>
        <span class="section-stats">
          {#if results.length > 0}
            FOUND: {results.length} MATCHES | QUERY: "{query}"
          {:else if query && !loading}
            NO MATCHES FOUND | QUERY: "{query}"
          {:else}
            AWAITING INPUT...
          {/if}
        </span>
      </div>
      
      <!-- Error Display -->
      {#if error}
        <div class="error-container">
          <div class="error-header">
            <span class="error-icon">[X]</span>
            <span class="error-title">SYSTEM ALERT</span>
          </div>
          <div class="error-message">
            {error}
          </div>
        </div>
      {/if}
      
      <!-- Results Grid -->
      {#if results.length > 0}
        <div class="results-grid">
          {#each results as result, i}
            <div class="result-card">
              <div class="result-header">
                <span class="result-id">RESULT_{String(i + 1).padStart(3, '0')}</span>
                <span class="result-source">[{result.source || 'UNKNOWN_SOURCE'}]</span>
              </div>
              
              <div class="result-title">
                {result.title || 'UNTITLED_RESOURCE'}
              </div>
              
              {#if result.description}
                <div class="result-description">
                  {result.description}
                </div>
              {/if}
              
              <div class="result-footer">
                <span class="result-timestamp">
                  {result.timestamp ? new Date(result.timestamp).toLocaleString('de-DE') : 'TIMESTAMP_UNAVAILABLE'}
                </span>
                {#if result.relevance}
                  <span class="result-relevance">
                    RELEVANCE: {(result.relevance * 100).toFixed(1)}%
                  </span>
                {/if}
              </div>
              
              {#if result.url}
                <div class="result-actions">
                  <a 
                    href={result.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    class="result-link"
                  >
                    ACCESS_RESOURCE [EXTERNAL]
                  </a>
                </div>
              {/if}
            </div>
          {/each}
        </div>
      {:else if loading}
        <div class="loading-container">
          <div class="loading-animation">
            <div class="loading-dots">
              {#each Array(3) as _, i}
                <div class="loading-dot" style={`animation-delay: ${i * 0.2}s`}></div>
              {/each}
            </div>
            <div class="loading-text">
              ESTABLISHING SECURE CONNECTION...
            </div>
          </div>
        </div>
      {/if}
    </section>
  </main>
  
  <!-- System Footer -->
  <footer class="system-footer">
    <div class="footer-left">
      <span class="footer-text">
        DARKWEB BROWSER v1.0 | SECURE SEARCH INTERFACE
      </span>
    </div>
    <div class="footer-right">
      <span class="footer-warning">
        [!] FOR AUTHORIZED RESEARCH ONLY [!]
      </span>
    </div>
  </footer>
</div>

<style>
  /* Terminal Interface Container */
  .terminal-interface {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: var(--bg-primary);
    border: 1px solid var(--border-dim);
    margin: 0;
    position: relative;
  }
  
  /* System Header */
  .system-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem 1.5rem;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-primary);
    box-shadow: var(--glow);
  }
  
  .header-left, .header-right {
    display: flex;
    align-items: center;
    gap: 2rem;
  }
  
  .system-id {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .prompt {
    color: var(--accent-primary);
    font-weight: bold;
  }
  
  .system-name {
    color: var(--text-primary);
    font-weight: bold;
    letter-spacing: 1px;
  }
  
  .system-version {
    color: var(--text-dim);
    font-size: 0.9em;
  }
  
  .system-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .status-label {
    color: var(--text-dim);
  }
  
  .status-value {
    color: var(--text-secondary);
    padding: 0.2rem 0.6rem;
    border: 1px solid var(--border-dim);
    background: var(--bg-tertiary);
    min-width: 150px;
    text-align: center;
  }
  
  .status-value.active {
    color: var(--accent-primary);
    border-color: var(--accent-primary);
    box-shadow: var(--terminal-glow);
  }
  
  .system-metrics {
    display: flex;
    gap: 1.5rem;
  }
  
  .metric {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
  }
  
  .metric-label {
    color: var(--text-dim);
    font-size: 0.8em;
  }
  
  .metric-value {
    color: var(--text-primary);
    font-family: 'Courier New', monospace;
    font-weight: bold;
  }
  
  /* Connection Monitor */
  .connection-monitor {
    background: var(--bg-tertiary);
    border-bottom: 1px solid var(--border-dim);
    padding: 0.5rem 1.5rem;
  }
  
  .monitor-bar {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .progress-track {
    height: 4px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-dim);
    position: relative;
    overflow: hidden;
  }
  
  .progress-indicator {
    height: 100%;
    background: linear-gradient(90deg, var(--accent-dark), var(--accent-primary));
    transition: width 0.3s ease;
  }
  
  .progress-indicator.active {
    background: linear-gradient(90deg, var(--accent-dark), var(--accent-primary), var(--accent-dark));
    background-size: 200% 100%;
    animation: progress-glow 2s linear infinite;
  }
  
  @keyframes progress-glow {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }
  
  .protocol-info {
    display: flex;
    justify-content: space-between;
    color: var(--text-dim);
    font-size: 0.85em;
  }
  
  /* Main Interface */
  .main-interface {
    flex: 1;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    overflow-y: auto;
  }
  
  /* Query Section */
  .query-section {
    border: 1px solid var(--border-dim);
    background: var(--bg-secondary);
    padding: 1rem;
  }
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 0.8rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--border-dim);
  }
  
  .section-title {
    color: var(--accent-primary);
    font-weight: bold;
    letter-spacing: 0.5px;
  }
  
  .section-help {
    color: var(--text-dim);
    font-size: 0.85em;
  }
  
  .input-container {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .input-prompt {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    min-width: 120px;
  }
  
  .cursor {
    color: var(--accent-primary);
    animation: blink 1s infinite;
  }
  
  .prompt-text {
    color: var(--text-primary);
    font-weight: bold;
  }
  
  .terminal-input {
    flex: 1;
    padding: 0.8rem 1rem;
    background: var(--bg-primary);
    border: 1px solid var(--border-dim);
    color: var(--text-primary);
    font-family: inherit;
    font-size: 1em;
    letter-spacing: 0.5px;
  }
  
  .terminal-input:focus {
    outline: none;
    border-color: var(--accent-primary);
    box-shadow: var(--terminal-glow);
  }
  
  .terminal-input::placeholder {
    color: var(--text-dim);
  }
  
  .input-actions {
    display: flex;
    gap: 0.8rem;
  }
  
  .action-button {
    padding: 0.8rem 1.5rem;
    border: 1px solid var(--border-dim);
    background: var(--bg-tertiary);
    color: var(--text-primary);
    font-family: inherit;
    font-size: 0.9em;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.2s ease;
  }
  
  .action-button:hover:not(:disabled) {
    border-color: var(--accent-primary);
    box-shadow: var(--terminal-glow);
  }
  
  .action-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .action-button.execute {
    background: var(--accent-dark);
    border-color: var(--accent-secondary);
  }
  
  .action-button.clear {
    background: var(--bg-tertiary);
  }
  
  .button-label {
    font-weight: bold;
  }
  
  .button-hint {
    color: var(--text-dim);
    font-size: 0.8em;
  }
  
  /* History Section */
  .history-section {
    border-top: 1px solid var(--border-dim);
    padding-top: 1rem;
  }
  
  .history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.8rem;
  }
  
  .history-title {
    color: var(--text-secondary);
  }
  
  .history-count {
    color: var(--text-dim);
    font-size: 0.9em;
  }
  
  .history-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .history-item {
    padding: 0.5rem 1rem;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-dim);
    color: var(--text-secondary);
    font-family: inherit;
    font-size: 0.9em;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.2s ease;
  }
  
  .history-item:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }
  
  .item-prefix {
    color: var(--accent-secondary);
  }
  
  .item-text {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 200px;
  }
  
  /* Results Section */
  .results-section {
    border: 1px solid var(--border-dim);
    background: var(--bg-secondary);
    padding: 1rem;
    flex: 1;
  }
  
  .section-stats {
    color: var(--text-dim);
    font-size: 0.9em;
  }
  
  /* Error Container */
  .error-container {
    border: 1px solid var(--error);
    background: rgba(255, 0, 0, 0.05);
    padding: 1rem;
    margin: 1rem 0;
  }
  
  .error-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  .error-icon {
    color: var(--error);
    font-weight: bold;
  }
  
  .error-title {
    color: var(--error);
    font-weight: bold;
  }
  
  .error-message {
    color: var(--text-primary);
    font-family: 'Courier New', monospace;
    white-space: pre-wrap;
  }
  
  /* Results Grid */
  .results-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .result-card {
    border: 1px solid var(--border-dim);
    background: var(--bg-card);
    padding: 1.2rem;
    transition: all 0.3s ease;
  }
  
  .result-card:hover {
    border-color: var(--accent-primary);
    box-shadow: var(--glow);
  }
  
  .result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border-dim);
  }
  
  .result-id {
    color: var(--accent-primary);
    font-weight: bold;
    font-family: 'Courier New', monospace;
  }
  
  .result-source {
    color: var(--text-dim);
    font-size: 0.9em;
  }
  
  .result-title {
    color: var(--text-primary);
    font-size: 1.1em;
    margin-bottom: 0.8rem;
    font-weight: bold;
  }
  
  .result-description {
    color: var(--text-secondary);
    line-height: 1.5;
    margin-bottom: 1rem;
  }
  
  .result-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 0.8rem;
    border-top: 1px solid var(--border-dim);
    color: var(--text-dim);
    font-size: 0.9em;
  }
  
  .result-relevance {
    color: var(--accent-primary);
    font-weight: bold;
  }
  
  .result-actions {
    margin-top: 1rem;
    padding-top: 0.8rem;
    border-top: 1px solid var(--border-dim);
  }
  
  .result-link {
    color: var(--accent-primary);
    text-decoration: none;
    font-weight: bold;
    display: inline-block;
    padding: 0.5rem 1rem;
    border: 1px solid var(--accent-secondary);
    background: rgba(0, 255, 0, 0.05);
    transition: all 0.2s ease;
  }
  
  .result-link:hover {
    background: rgba(0, 255, 0, 0.1);
    box-shadow: var(--terminal-glow);
  }
  
  /* Loading Animation */
  .loading-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 3rem;
  }
  
  .loading-animation {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
  
  .loading-dots {
    display: flex;
    gap: 0.5rem;
  }
  
  .loading-dot {
    width: 8px;
    height: 8px;
    background: var(--accent-primary);
    border-radius: 50%;
    animation: blink 1.4s infinite;
  }
  
  .loading-text {
    color: var(--text-dim);
    letter-spacing: 1px;
  }
  
  /* System Footer */
  .system-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem 1.5rem;
    background: var(--bg-secondary);
    border-top: 1px solid var(--border-primary);
    border-bottom: 1px solid var(--accent-dark);
  }
  
  .footer-text {
    color: var(--text-dim);
    font-size: 0.9em;
  }
  
  .footer-warning {
    color: var(--warning);
    font-weight: bold;
    font-size: 0.9em;
    letter-spacing: 0.5px;
  }
  
  /* Responsive Design */
  @media (max-width: 1024px) {
    .system-header, .header-left, .header-right {
      flex-direction: column;
      gap: 0.8rem;
      align-items: flex-start;
    }
    
    .input-container {
      flex-direction: column;
      align-items: stretch;
    }
    
    .input-prompt {
      justify-content: center;
    }
    
    .input-actions {
      justify-content: center;
    }
    
    .protocol-info {
      flex-direction: column;
      gap: 0.3rem;
    }
  }
  
  @media (max-width: 768px) {
    .main-interface {
      padding: 1rem;
    }
    
    .system-footer {
      flex-direction: column;
      gap: 0.5rem;
      text-align: center;
    }
    
    .history-grid {
      flex-direction: column;
    }
    
    .item-text {
      max-width: 100%;
    }
  }
</style>