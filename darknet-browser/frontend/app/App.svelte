<script>
  let query = ''
  let loading = false
  let result = null
  let error = null

  // Router base is /analyze
  const API_BASE = import.meta.env.VITE_API_BASE || '/analyze'

  async function doSearch(e) {
    e.preventDefault()
    error = null
    result = null
    const q = query.trim()
    if (!q) {
      error = 'Enter a query.'
      return
    }
    loading = true
    try {
      const resp = await fetch(`${API_BASE}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q })
      })
      if (!resp.ok) {
        throw new Error(`Backend error ${resp.status}: ${await resp.text()}`)
      }
      result = await resp.json()
    } catch (err) {
      error = err.message
    } finally {
      loading = false
    }
  }
</script>

<style>
  :global(body) {
    margin: 0;
    font-family: system-ui, sans-serif;
    background: #101317;
    color: #e4e7eb;
  }
  .wrap {
    max-width: 760px;
    margin: 40px auto;
    padding: 0 20px;
  }
  h1 { margin: 0 0 8px; }
  input {
    width: 100%; padding: 12px; border-radius: 8px;
    border: 1px solid #2d3440; background:#1b2026; color:#fff;
  }
  button {
    margin-top: 12px; padding:10px 16px; border:none;
    border-radius:8px; background:#2563eb; color:#fff; cursor:pointer;
  }
  button:disabled { opacity:.6; cursor:not-allowed; }
  .panel {
    margin-top:24px; background:#1b2026; border:1px solid #2d3440;
    padding:16px; border-radius:8px; overflow-x:auto;
  }
  .error { margin-top:12px; color:#ff6363; font-weight:600; }
  .footer { margin-top:48px; font-size:.75rem; opacity:.55; text-align:center; }
</style>

<div class="wrap">
  <h1>Analyze Search</h1>
  <p>Prototype – enter a query; this router may forward it downstream.</p>

  <form on:submit={doSearch}>
    <input type="text" bind:value={query} placeholder="Type your query..." autocomplete="off" />
    <button type="submit" disabled={loading}>{loading ? 'Working...' : 'Send'}</button>
  </form>

  {#if error}
    <div class="error">{error}</div>
  {/if}

  {#if result}
    <div class="panel">
      <strong>Response:</strong>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  {/if}

  <div class="footer">
    Single Microservice – Analyze Router
  </div>
</div>