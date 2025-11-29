<script>
  import { supabase } from '$lib/supabase';
  import { goto } from '$app/navigation';
  
  let searchQuery = '';
  let results = [];
  let loading = false;
  let error = '';

  async function handleSearch() {
    if (!searchQuery.trim()) return;
    
    loading = true;
    error = '';
    results = [];

    try {
      const response = await fetch('/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: searchQuery })
      });

      if (response.ok) {
        const data = await response.json();
        results = data.results || [];
      } else {
        error = 'Search failed';
      }
    } catch (err) {
      error = 'Network error';
    }
    
    loading = false;
  }

  async function handleLogout() {
    await supabase.auth.signOut();
    goto('/login');
  }
</script>

<div class="search-container">
  <header>
    <h1>Dark Web Search</h1>
    <button on:click={handleLogout}>Logout</button>
  </header>

  <div class="search-box">
    <input 
      type="text" 
      bind:value={searchQuery}
      placeholder="Enter search query..."
      on:keydown={(e) => e.key === 'Enter' && handleSearch()}
    />
    <button on:click={handleSearch} disabled={loading}>
      {loading ? 'Searching...' : 'Search'}
    </button>
  </div>

  {#if error}
    <div class="error">{error}</div>
  {/if}

  {#if results.length > 0}
    <div class="results">
      <h2>Results:</h2>
      {#each results as result}
        <div class="result-item">
          {result}
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .search-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
  }
  
  .search-box {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  input {
    flex: 1;
    padding: 10px;
    font-size: 16px;
  }
  
  button {
    padding: 10px 20px;
    background: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:disabled {
    background: #ccc;
  }
  
  .error {
    color: red;
    margin: 10px 0;
  }
  
  .result-item {
    padding: 10px;
    border: 1px solid #ddd;
    margin: 5px 0;
  }
</style>