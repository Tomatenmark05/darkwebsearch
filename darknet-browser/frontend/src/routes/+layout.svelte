<script lang="ts">
  import { onMount } from 'svelte';
  import { supabase } from '$lib/supabaseClient';
  import { page } from '$app/stores';

  let user = null;

  onMount(async () => {
    const { data } = await supabase.auth.getUser();
    user = data.user;
  });
</script>

<slot />