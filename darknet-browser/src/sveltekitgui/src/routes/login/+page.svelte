<script>
  import { supabase } from '$lib/supabase';
  import { goto } from '$app/navigation';
  
  let email = '';
  let password = '';
  let loading = false;
  let error = '';

  async function handleLogin() {
    loading = true;
    error = '';

    const { error: signInError } = await supabase.auth.signInWithPassword({
      email,
      password
    });

    if (signInError) {
      error = signInError.message;
    } else {
      goto('/search');
    }
    
    loading = false;
  }
</script>

<div class="login-container">
  <h1>Login</h1>
  
  {#if error}
    <div class="error">{error}</div>
  {/if}
  
  <form on:submit|preventDefault={handleLogin}>
    <input 
      type="email" 
      bind:value={email}
      placeholder="Email" 
      required
    />
    
    <input 
      type="password" 
      bind:value={password}
      placeholder="Password" 
      required
    />
    
    <button type="submit" disabled={loading}>
      {loading ? 'Loading...' : 'Login'}
    </button>
  </form>
</div>

<style>
  .login-container {
    max-width: 400px;
    margin: 100px auto;
    padding: 20px;
  }
  
  input {
    display: block;
    width: 100%;
    margin: 10px 0;
    padding: 10px;
  }
  
  button {
    width: 100%;
    padding: 10px;
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
    margin-bottom: 10px;
  }
</style>