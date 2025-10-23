<script lang="ts">
  import { supabase } from '$lib/supabaseClient';
  let email = '';
  let password = '';
  let message = '';

  async function signUp() {
    const { error } = await supabase.auth.signUp({ email, password });
    message = error ? error.message : 'Check your email for confirmation link.';
  }
</script>

<h1>Sign Up</h1>
<input bind:value={email} placeholder="Email" />
<input type="password" bind:value={password} placeholder="Password" />
<button on:click={signUp}>Sign Up</button>
<p>{message}</p>
