<script>
  import { supabase } from '$lib/supabase'
  import { goto } from '$app/navigation'
  
  let email = ''
  let password = ''
  let loading = false
  let error = ''
  let message = ''
  
  async function handleLogin() {
    if (!email || !password) {
      error = 'EMAIL AND PASSWORD REQUIRED'
      return
    }
    
    loading = true
    error = ''
    message = ''
    
    try {
      const { error: authError } = await supabase.auth.signInWithPassword({
        email,
        password
      })
      
      if (authError) throw authError
      
      message = 'AUTHENTICATION SUCCESSFUL'
      setTimeout(() => {
        goto('/')
      }, 1000)
      
    } catch (err) {
      error = `AUTH ERROR: ${err.message}`
    } finally {
      loading = false
    }
  }
  
  function handleKeyPress(e) {
    if (e.key === 'Enter' && !loading) {
      handleLogin()
    }
  }
</script>

<div class="auth-page">
  <div class="auth-terminal">
    <!-- Terminal Header -->
    <div class="terminal-header">
      <div class="terminal-title">
        <span class="prompt">&gt;&gt;</span>
        <span class="title-text">SECURE ACCESS</span>
      </div>
      <div class="terminal-status">
        <span class="status-label">ACCESS:</span>
        <span class="status-value">AWAITING CREDENTIALS</span>
      </div>
    </div>
    
    <!-- Auth Form -->
    <div class="auth-form">
      <div class="form-header">
        <span class="form-title">[SYSTEM ACCESS]</span>
        <span class="form-subtitle">AUTHENTICATION REQUIRED</span>
      </div>
      
      {#if message}
        <div class="message-container">
          <div class="message-icon">[✓]</div>
          <div class="message-text">{message}</div>
        </div>
      {/if}
      
      {#if error}
        <div class="error-container">
          <div class="error-icon">[X]</div>
          <div class="error-text">{error}</div>
        </div>
      {/if}
      
      <div class="form-group">
        <div class="form-label">
          <span class="label-prompt">&gt;</span>
          <span class="label-text">EMAIL ADDRESS</span>
        </div>
        <input
          type="email"
          bind:value={email}
          on:keydown={handleKeyPress}
          placeholder="user@domain.com"
          class="form-input"
          disabled={loading}
          spellcheck="false"
          autocomplete="email"
        />
      </div>
      
      <div class="form-group">
        <div class="form-label">
          <span class="label-prompt">&gt;</span>
          <span class="label-text">PASSWORD</span>
        </div>
        <input
          type="password"
          bind:value={password}
          on:keydown={handleKeyPress}
          placeholder="••••••••"
          class="form-input"
          disabled={loading}
          autocomplete="current-password"
        />
      </div>
      
      <div class="form-actions">
        <button
          on:click={handleLogin}
          class="auth-button login"
          disabled={loading || !email || !password}
        >
          <span class="button-text">
            {loading ? 'PROCESSING...' : 'LOGIN'}
          </span>
          <span class="button-hint">[ENTER]</span>
        </button>
      </div>
      
      <div class="form-footer">
        <span class="footer-text">
          [!] AUTHORIZED ACCESS ONLY [!]
        </span>
      </div>
    </div>
  </div>
</div>

<style>
  .auth-page {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: var(--bg-primary);
    padding: 2rem;
  }
  
  .auth-terminal {
    width: 100%;
    max-width: 500px;
    border: 1px solid var(--border-dim);
    background: var(--bg-secondary);
    box-shadow: var(--glow-strong);
  }
  
  .terminal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background: var(--bg-tertiary);
    border-bottom: 1px solid var(--border-primary);
  }
  
  .terminal-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .prompt {
    color: var(--accent-primary);
    font-weight: bold;
  }
  
  .title-text {
    color: var(--text-primary);
    font-weight: bold;
    letter-spacing: 0.5px;
  }
  
  .terminal-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .status-label {
    color: var(--text-dim);
  }
  
  .status-value {
    color: var(--accent-secondary);
    font-family: 'Courier New', monospace;
  }
  
  .auth-form {
    padding: 2rem;
  }
  
  .form-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  .form-title {
    display: block;
    color: var(--accent-primary);
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }
  
  .form-subtitle {
    color: var(--text-dim);
    font-size: 0.9em;
  }
  
  .message-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    margin-bottom: 1.5rem;
    background: rgba(0, 255, 0, 0.05);
    border: 1px solid var(--accent-primary);
  }
  
  .message-icon {
    color: var(--accent-primary);
    font-weight: bold;
  }
  
  .message-text {
    color: var(--text-primary);
  }
  
  .error-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    margin-bottom: 1.5rem;
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
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  .form-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  .label-prompt {
    color: var(--accent-primary);
  }
  
  .label-text {
    color: var(--text-primary);
    font-weight: bold;
  }
  
  .form-input {
    width: 100%;
    padding: 0.8rem 1rem;
    background: var(--bg-primary);
    border: 1px solid var(--border-dim);
    color: var(--text-primary);
    font-family: inherit;
    font-size: 1em;
  }
  
  .form-input:focus {
    outline: none;
    border-color: var(--accent-primary);
    box-shadow: var(--terminal-glow);
  }
  
  .form-input::placeholder {
    color: var(--text-dim);
  }
  
  .form-actions {
    display: flex;
    gap: 1rem;
    margin: 2rem 0;
  }
  
  .auth-button {
    flex: 1;
    padding: 1rem;
    border: 1px solid var(--border-dim);
    background: var(--accent-dark);
    color: var(--text-primary);
    font-family: inherit;
    font-size: 1em;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.2s ease;
  }
  
  .auth-button:hover:not(:disabled) {
    border-color: var(--accent-primary);
    box-shadow: var(--terminal-glow);
  }
  
  .auth-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .button-text {
    font-weight: bold;
  }
  
  .button-hint {
    color: var(--text-dim);
    font-size: 0.8em;
  }
  
  .form-footer {
    text-align: center;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border-dim);
  }
  
  .footer-text {
    color: var(--warning);
    font-weight: bold;
    font-size: 0.9em;
  }
</style>