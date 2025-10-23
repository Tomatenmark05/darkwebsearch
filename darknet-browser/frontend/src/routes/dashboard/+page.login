<script lang="ts">
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabaseClient';

  let user = null;
  let managerResponse = '';

  onMount(async () => {
    const { data } = await supabase.auth.getUser();
    user = data.user;

    if (user) {
      const token = (await supabase.auth.getSession()).data.session?.access_token;
      const res = await fetch('/api/manager', {
        method: 'GET',
        headers: { Authorization: `Bearer ${token}` }
      });
      managerResponse = await res.text();
    }
  });
</script>

<h1>Dashboard</h1>
{#if user}
  <p>Welcome, {user.email}</p>
  <p>Manager says: {managerResponse}</p>
  <a href="/logout">Logout</a>
{:else}
  <p>Please <a href="/login">login</a>.</p>
{/if}
