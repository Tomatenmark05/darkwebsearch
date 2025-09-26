<script>
	import { onMount } from 'svelte';
	import { supabase } from '$lib/supabase.js';
	import { writable } from 'svelte/store';
	
	export const user = writable(null);
	
	onMount(() => {
		// Get initial session
		supabase.auth.getSession().then(({ data: { session } }) => {
			user.set(session?.user ?? null);
		});
		
		// Listen for auth changes
		const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
			user.set(session?.user ?? null);
		});
		
		return () => subscription.unsubscribe();
	});
</script>

<style>
	:global(body) {
		margin: 0;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
		background: #f8f9fa;
	}
	
	:global(*) {
		box-sizing: border-box;
	}
	
	nav {
		background: #fff;
		padding: 1rem 2rem;
		box-shadow: 0 2px 4px rgba(0,0,0,0.1);
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	nav h1 {
		margin: 0;
		color: #333;
		font-size: 1.5rem;
	}
	
	nav .auth-section {
		display: flex;
		gap: 1rem;
		align-items: center;
	}
	
	nav button {
		background: #007bff;
		color: white;
		border: none;
		padding: 0.5rem 1rem;
		border-radius: 4px;
		cursor: pointer;
		font-size: 0.9rem;
	}
	
	nav button:hover {
		background: #0056b3;
	}
	
	nav button.secondary {
		background: #6c757d;
	}
	
	nav button.secondary:hover {
		background: #545b62;
	}
	
	.user-info {
		color: #666;
		font-size: 0.9rem;
	}
	
	main {
		max-width: 1200px;
		margin: 2rem auto;
		padding: 0 2rem;
	}
</style>

<nav>
	<h1>🕸️ Darkwebsearch</h1>
	<div class="auth-section">
		{#if $user}
			<span class="user-info">Welcome, {$user.email}</span>
			<button class="secondary" on:click={() => supabase.auth.signOut()}>Sign Out</button>
		{:else}
			<button on:click={() => window.location.href = '/login'}>Sign In</button>
		{/if}
	</div>
</nav>

<main>
	<slot />
</main>