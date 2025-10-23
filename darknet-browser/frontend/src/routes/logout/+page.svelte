<script lang="ts">
  import { supabase } from '$lib/supabaseClient';
  import { goto } from '$app/navigation';

  supabase.auth.signOut().then(() => {
    goto('/login');
  });
</script>

<p>Logging out...</p>
