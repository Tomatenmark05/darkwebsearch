<script>
  import { goto } from '$app/navigation'
  import { supabase, logSearch } from '$lib/supabase'
  import { onMount } from 'svelte'
  
  // Authentication state
  let session = null
  let authLoading = true
  
  // Search state
  let query = ''
  let loading = false
  let results = []
  let error = null

  // Copy feedback
  let copiedUrl = null
  let copiedTimer = null
  
  // Session refresh function
  async function refreshSession() {
    try {
      const { data, error } = await supabase.auth.getSession()
      
      if (error) {
        console.error('Session refresh error:', error)
        return null
      }
      
      if (!data.session) {
        return null
      }
      
      return data.session
    } catch (error) {
      console.error('Failed to refresh session:', error)
      return null
    }
  }

  // Sanitize noisy HTML-ish strings
  function cleanText(s) {
    if (!s) return ''
    return String(s)
      .replace(/<!DOCTYPE[^>]*>/gi, '')
      .replace(/<script[\s\S]*?<\/script>/gi, '')
      .replace(/<style[\s\S]*?<\/style>/gi, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/\s+/g, ' ')
      .trim()
  }

  function truncate(s, n = 180) {
    if (!s) return ''
    return s.length > n ? s.slice(0, n) + '…' : s
  }
  
  // On mount - check authentication
  onMount(async () => {
    console.log('=== PAGE MOUNT ===')
    
    const { data } = await supabase.auth.getSession()
    console.log('Session data:', data)
    
    if (!data.session) {
      console.log('No session, redirecting to login')
      goto('/login')
      return
    }
    
    console.log('User authenticated:', data.session.user.email)
    session = data.session
    authLoading = false
    
    // Auth state listener (besser als Interval)
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, currentSession) => {
        console.log('Auth state changed:', event)
        
        if (event === 'SIGNED_OUT' || event === 'USER_DELETED' || !currentSession) {
          console.log('User signed out or session expired')
          session = null
          goto('/login')
        } else if (event === 'TOKEN_REFRESHED') {
          console.log('Token refreshed')
          session = currentSession
        }
      }
    )
    
    return () => {
      console.log('Cleaning up auth listener')
      if (subscription) {
        subscription.unsubscribe()
      }
      if (copiedTimer) {
        clearTimeout(copiedTimer)
      }
    }
  })
  
  // Execute search
  async function executeSearch() {
    if (!query.trim()) return
    
    // Refresh session before search (WICHTIG für Token-Refresh!)
    const freshSession = await refreshSession()
    
    if (!freshSession) {
      error = '[AUTH ERROR] SESSION EXPIRED'
      setTimeout(() => goto('/login'), 1500)
      return
    }
    
    session = freshSession
    loading = true
    error = null
    results = []
    copiedUrl = null
    
    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`
        },
        body: JSON.stringify({ 
          query: query.trim(),
          timestamp: Date.now()
        })
      })
      
      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('AUTHENTICATION FAILED')
        }
        throw new Error(`HTTP ${response.status}`)
      }
      
      const data = await response.json()
      
      if (data.error) {
        throw new Error(`SERVER: ${data.error}`)
      }
      
      results = data.results || []
      
      // Log search to database
      await logSearch(session.user.id, query.trim(), results.length)
      
    } catch (err) {
      error = `[ERROR] ${err.message}`
      
      if (err.message.includes('AUTHENTICATION') || err.message.includes('SESSION')) {
        setTimeout(() => goto('/login'), 2000)
      }
    } finally {
      loading = false
    }
  }

  // Robust copy (clipboard API + fallback)
  async function copyToClipboard(text) {
    try {
      if (!text) return

      if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
        await navigator.clipboard.writeText(text)
      } else {
        const ta = document.createElement('textarea')
        ta.value = text
        ta.setAttribute('readonly', '')
        ta.style.position = 'absolute'
        ta.style.left = '-9999px'
        document.body.appendChild(ta)
        ta.select()
        const ok = document.execCommand('copy')
        document.body.removeChild(ta)
        if (!ok) throw new Error('Clipboard blocked')
      }

      copiedUrl = text
      if (copiedTimer) clearTimeout(copiedTimer)
      copiedTimer = setTimeout(() => {
        copiedUrl = null
      }, 1500)
    } catch (e) {
      error = `[ERROR] Could not copy link: ${e.message}`
    }
  }
  
  function clearInterface() {
    query = ''
    results = []
    error = null
    copiedUrl = null
    if (copiedTimer) {
      clearTimeout(copiedTimer)
      copiedTimer = null
    }
  }
  
  async function handleLogout() {
    console.log('Logout initiated')
    
    try {
      // Sign out from Supabase
      const { error } = await supabase.auth.signOut()
      
      if (error) {
        console.error('Logout error:', error)
        throw error
      }
      
      console.log('Logout successful')
      
      // Clear local storage
      if (typeof window !== 'undefined') {
        localStorage.clear()
      }
      
      // Clear session state
      session = null
      
      // Redirect to login page
      goto('/login')
      
    } catch (err) {
      console.error('Logout failed:', err)
      error = `[ERROR] Logout failed: ${err.message}`
      // Trotzdem zu Login redirecten
      goto('/login')
    }
  }
  
  function handleKeyPress(e) {
    if (e.key === 'Enter' && !loading && query.trim()) {
      executeSearch()
    }
    if (e.key === 'Escape') {
      clearInterface()
    }
  }
</script>

{#if authLoading}
  <div class="auth-loading">
    <div class="terminal-loading">
      <div class="loading-dots">
        {#each Array(3) as _, i}
          <div class="loading-dot" style={`animation-delay: ${i * 0.2}s`}></div>
        {/each}
      </div>
      <div class="loading-text">INITIALIZING...</div>
    </div>
  </div>
{:else if !session}
  <div class="access-denied">
    <div class="denied-terminal">
      <div class="denied-message">
        [ACCESS DENIED] REDIRECTING...
      </div>
    </div>
  </div>
{:else}
  <div class="terminal-interface">
    <header class="header">
      <div class="system-id">
        <span class="prompt">&gt;&gt;</span>
        <span class="system-name">darknet_BROWSER</span>
      </div>
      <div class="user-display">
        <span class="user-name">{session.user.email.split('@')[0]}</span>
        <button on:click={handleLogout} class="logout-button" title="Click to logout">
          LOGOUT
        </button>
      </div>
    </header>
    
    <!-- Main Interface -->
    <main class="main-interface">
      <!-- Search Section -->
      <section class="search-section">
        <div class="search-container">
          <div class="search-input-group">
            <div class="input-prompt">
              <span class="cursor">_</span>
              <span class="prompt-text">SEARCH&gt;</span>
            </div>
            
            <input
              type="text"
              bind:value={query}
              on:keydown={handleKeyPress}
              placeholder="ENTER SEARCH QUERY..."
              class="terminal-input"
              disabled={loading}
              spellcheck="false"
              autocorrect="off"
              autocomplete="off"
            />
          </div>
          
          <div class="search-buttons">
            <button
              on:click={executeSearch}
              class="action-button execute"
              disabled={loading || !query.trim()}
              title="Execute Search (ENTER)"
            >
              <span class="button-text">
                {loading ? 'SEARCHING...' : 'EXECUTE'}
              </span>
              <span class="button-hint">[ENTER]</span>
            </button>
            
            <button
              on:click={clearInterface}
              class="action-button clear"
              title="Clear (ESC)"
            >
              <span class="button-text">CLEAR</span>
              <span class="button-hint">[ESC]</span>
            </button>
          </div>
        </div>
        
        <!-- Error Display -->
        {#if error}
          <div class="error-container">
            <div class="error-icon">[!]</div>
            <div class="error-text">{error}</div>
          </div>
        {/if}

        <!-- Copy feedback -->
        {#if copiedUrl}
          <div class="copy-container">
            <div class="copy-icon">[✓]</div>
            <div class="copy-text">LINK COPIED</div>
          </div>
        {/if}
      </section>
      
      <!-- Results Section -->
      <section class="results-section">
        {#if results.length > 0}
          <div class="results-header">
            <span class="results-title">SEARCH RESULTS ({results.length})</span>
          </div>
          
          <div class="results-grid">
            {#each results as result, i}
              <div class="result-card">
                <div class="result-title">
                  {truncate(cleanText(result.title || 'UNTITLED'), 140)}
                </div>
                
                {#if result.description}
                  <div class="result-description">
                    {truncate(cleanText(result.description), 280)}
                  </div>
                {/if}

                {#if result.url}
                  <div class="result-url-row">
                    <div class="result-url-text">
                      <span class="url-label">LINK:</span>
                      <span class="url-value">{result.url}</span>
                    </div>
                    <button
                      class="copy-btn"
                      on:click={() => copyToClipboard(result.url)}
                      title="Copy link to clipboard"
                    >
                      COPY LINK
                    </button>
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
                PROCESSING REQUEST...
              </div>
            </div>
          </div>
        {:else if query && !loading}
          <div class="no-results">
            NO RESULTS FOUND FOR "{query}"
          </div>
        {/if}
      </section>
    </main>
    
    <!-- Footer -->
    <footer class="footer">
      <span class="footer-text">
        darknet BROWSER | SECURE SEARCH INTERFACE
      </span>
    </footer>
  </div>
{/if}

<style>
  .terminal-interface {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: var(--bg-primary);
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-primary);
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
  
  .user-display {
    display: flex;
    align-items: center;
    gap: 1.5rem;
  }
  
  .user-name {
    color: var(--text-dim);
    font-size: 0.9em;
    text-transform: lowercase;
  }
    
  .logout-button {
    padding: 0.4rem 1rem;
    background: transparent;
    border: 1px solid var(--border-dim);
    color: var(--text-dim);
    font-family: inherit;
    font-size: 0.8em;
    cursor: pointer;
    transition: all 0.2s ease;
    outline: none;
  }

  .logout-button:hover {
    border-color: var(--error);
    color: var(--error);
    background: rgba(255, 0, 0, 0.1);
    box-shadow: 0 0 5px rgba(255, 0, 0, 0.3);
  }

  .logout-button:active {
    transform: scale(0.95);
  }

  .logout-button:focus {
    border-color: var(--accent-primary);
  }
  
  /* Main Interface */
  .main-interface {
    flex: 1;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }
  
  /* Search Section */
  .search-section {
    border: 1px solid var(--border-dim);
    background: var(--bg-secondary);
    padding: 1.5rem;
  }
  
  .search-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-input-group {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .input-prompt {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    min-width: 100px;
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
  
  .search-buttons {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
  }
  
  .action-button {
    padding: 0.8rem 2rem;
    border: 1px solid var(--border-dim);
    background: var(--bg-tertiary);
    color: var(--text-primary);
    font-family: inherit;
    font-size: 1em;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.8rem;
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
  
  .button-text {
    font-weight: bold;
  }
  
  .button-hint {
    color: var(--text-dim);
    font-size: 0.8em;
  }
  
  /* Error Container */
  .error-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    margin-top: 1rem;
    background: rgba(255, 0, 0, 0.05);
    border: 1px solid var(--error);
  }
  
  .error-icon {
    color: var(--error);
    font-weight: bold;
  }
  
  .error-text {
    color: var(--text-primary);
    font-family: 'Courier New', monospace;
  }

  /* Copy feedback container */
  .copy-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    margin-top: 1rem;
    background: rgba(0, 255, 0, 0.05);
    border: 1px solid rgba(0, 255, 0, 0.35);
  }

  .copy-icon {
    font-weight: bold;
    color: var(--text-primary);
  }

  .copy-text {
    color: var(--text-primary);
    font-family: 'Courier New', monospace;
  }
  
  .results-section {
    flex: 1;
    border: 1px solid var(--border-dim);
    background: var(--bg-secondary);
    padding: 1.5rem;
  }
  
  .results-header {
    margin-bottom: 1.5rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--border-dim);
  }
  
  .results-title {
    color: var(--accent-primary);
    font-weight: bold;
    letter-spacing: 0.5px;
  }
  
  .results-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
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
  
  .result-title {
    color: var(--text-primary);
    font-size: 1.1em;
    margin-bottom: 0.8rem;
    font-weight: bold;
  }
  
  .result-description {
    color: var(--text-secondary);
    line-height: 1.5;
  }
  
  /* Loading Container */
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
  
  /* No Results */
  .no-results {
    text-align: center;
    padding: 3rem;
    color: var(--text-dim);
    font-style: italic;
  }
  
  /* Footer */
  .footer {
    padding: 1rem 1.5rem;
    background: var(--bg-secondary);
    border-top: 1px solid var(--border-primary);
    text-align: center;
  }
  
  .footer-text {
    color: var(--text-dim);
    font-size: 0.9em;
  }
  
  /* Auth Loading */
  .auth-loading {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: var(--bg-primary);
  }
  
  .terminal-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
  
  .loading-text {
    color: var(--text-dim);
    letter-spacing: 1px;
  }
  
  .access-denied {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: var(--bg-primary);
  }
  
  .denied-terminal {
    padding: 2rem;
    border: 1px solid var(--error);
    background: var(--bg-secondary);
  }
  
  .denied-message {
    color: var(--error);
    font-family: 'Courier New', monospace;
    font-size: 1.2em;
    text-align: center;
  }
  
  /* Animations */
  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
  }
  
  /* Responsive */
  @media (max-width: 768px) {
    .header {
      flex-direction: column;
      gap: 1rem;
      text-align: center;
    }
    
    .user-display {
      flex-direction: column;
      gap: 0.5rem;
    }
    
    .search-input-group {
      flex-direction: column;
      align-items: stretch;
    }
    
    .input-prompt {
      justify-content: center;
    }
    
    .search-buttons {
      flex-direction: column;
    }
    
    .main-interface {
      padding: 1rem;
    }
  }

  /* URL row + copy button (text color like rest) */
  .result-url-row {
    margin-top: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
  }

  .result-url-text {
    font-family: 'Courier New', monospace;
    font-size: 12px;
    word-break: break-all;
    color: var(--text-primary);
    display: flex;
    gap: 8px;
    align-items: baseline;
  }

  .url-label {
    opacity: 0.85;
  }

  .url-value {
    color: var(--text-primary);
  }

  .copy-btn {
    padding: 6px 10px;
    border: 1px solid var(--border-dim);
    background: transparent;
    color: var(--text-primary);
    font-family: 'Courier New', monospace;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .copy-btn:hover {
    border-color: var(--accent-primary);
    box-shadow: var(--terminal-glow);
  }
</style>
