<script lang="ts">
  import { supabase } from '$lib/supabaseClient';
  import { goto } from '$app/navigation';
  let email = '';
  let password = '';
  let message = '';

  async function login() {
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      message = error.message;
    } else {
      goto('/dashboard');
    }
  }
</script>

<h1>Login</h1>
<input bind:value={email} placeholder="Email" />
<input type="password" bind:value={password} placeholder="Password" />
<button on:click={login}>Login</button>
<p>{message}</p>
