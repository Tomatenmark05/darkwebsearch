<script>
  import { page } from '$app/stores';
  
  // Temporär: Überspringe Authentifizierung für Test
  let user = { name: "Test User" }; // Dummy user
  let loading = false;
</script>

{#if loading}
  <div>Loading...</div>
{:else if !user && $page.url.pathname !== '/login'}
  <script>
    import { goto } from '$app/navigation';
    goto('/login');
  </script>
{:else}
  <slot />
{/if}