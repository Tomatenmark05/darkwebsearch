<script>
	import { supabase } from '$lib/supabase.js';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	
	let email = '';
	let password = '';
	let loading = false;
	let error = '';
	let isSignUp = false;
	
	onMount(() => {
		// Check if user is already logged in
		supabase.auth.getSession().then(({ data: { session } }) => {
			if (session) {
				goto('/');
			}
		});
	});
	
	async function handleAuth() {
		if (!email || !password) {
			error = 'Please fill in all fields';
			return;
		}
		
		loading = true;
		error = '';
		
		try {
			let result;
			if (isSignUp) {
				result = await supabase.auth.signUp({
					email,
					password
				});
			} else {
				result = await supabase.auth.signInWithPassword({
					email,
					password
				});
			}
			
			if (result.error) {
				error = result.error.message;
			} else {
				if (isSignUp) {
					error = 'Check your email for the confirmation link!';
				} else {
					goto('/');
				}
			}
		} catch (e) {
			error = 'Authentication failed. Please try again.';
		} finally {
			loading = false;
		}
	}
	
	async function handleGoogleAuth() {
		loading = true;
		error = '';
		
		try {
			const { error: authError } = await supabase.auth.signInWithOAuth({
				provider: 'google',
				options: {
					redirectTo: window.location.origin
				}
			});
			
			if (authError) {
				error = authError.message;
			}
		} catch (e) {
			error = 'Google authentication failed.';
		} finally {
			loading = false;
		}
	}
</script>

<style>
	.login-container {
		max-width: 400px;
		margin: 4rem auto;
		background: white;
		padding: 2rem;
		border-radius: 8px;
		box-shadow: 0 4px 20px rgba(0,0,0,0.1);
	}
	
	.login-title {
		text-align: center;
		margin-bottom: 2rem;
		color: #333;
		font-size: 1.8rem;
	}
	
	.form-group {
		margin-bottom: 1rem;
	}
	
	.form-group label {
		display: block;
		margin-bottom: 0.5rem;
		color: #555;
		font-weight: 500;
	}
	
	.form-group input {
		width: 100%;
		padding: 0.75rem;
		border: 2px solid #ddd;
		border-radius: 4px;
		font-size: 1rem;
		transition: border-color 0.3s;
	}
	
	.form-group input:focus {
		outline: none;
		border-color: #007bff;
	}
	
	.auth-button {
		width: 100%;
		padding: 0.75rem;
		border: none;
		border-radius: 4px;
		font-size: 1rem;
		cursor: pointer;
		margin-bottom: 1rem;
		transition: all 0.3s;
	}
	
	.auth-button.primary {
		background: #007bff;
		color: white;
	}
	
	.auth-button.primary:hover {
		background: #0056b3;
	}
	
	.auth-button.google {
		background: #db4437;
		color: white;
	}
	
	.auth-button.google:hover {
		background: #c23321;
	}
	
	.auth-button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}
	
	.toggle-auth {
		text-align: center;
		margin-top: 1rem;
		color: #666;
	}
	
	.toggle-auth button {
		background: none;
		border: none;
		color: #007bff;
		cursor: pointer;
		text-decoration: underline;
	}
	
	.error {
		background: #f8d7da;
		color: #721c24;
		padding: 0.75rem;
		border-radius: 4px;
		margin-bottom: 1rem;
		border: 1px solid #f5c6cb;
	}
	
	.demo-note {
		background: #d1ecf1;
		color: #0c5460;
		padding: 1rem;
		border-radius: 4px;
		margin-bottom: 1rem;
		border: 1px solid #bee5eb;
		font-size: 0.9rem;
	}
	
	.demo-note strong {
		display: block;
		margin-bottom: 0.5rem;
	}
</style>

<div class="login-container">
	<h1 class="login-title">🔐 {isSignUp ? 'Sign Up' : 'Sign In'}</h1>
	
	<div class="demo-note">
		<strong>Demo Mode:</strong>
		This is a prototype application. Supabase authentication is configured but may require setup. 
		You can explore the interface and use the search functionality.
	</div>
	
	{#if error}
		<div class="error">
			{error}
		</div>
	{/if}
	
	<form on:submit|preventDefault={handleAuth}>
		<div class="form-group">
			<label for="email">Email</label>
			<input 
				type="email" 
				id="email" 
				bind:value={email}
				placeholder="Enter your email"
				disabled={loading}
				required
			/>
		</div>
		
		<div class="form-group">
			<label for="password">Password</label>
			<input 
				type="password" 
				id="password" 
				bind:value={password}
				placeholder="Enter your password"
				disabled={loading}
				required
			/>
		</div>
		
		<button 
			type="submit" 
			class="auth-button primary"
			disabled={loading}
		>
			{loading ? 'Processing...' : isSignUp ? 'Sign Up' : 'Sign In'}
		</button>
	</form>
	
	<button 
		class="auth-button google"
		on:click={handleGoogleAuth}
		disabled={loading}
	>
		{loading ? 'Processing...' : '🔗 Continue with Google'}
	</button>
	
	<div class="toggle-auth">
		{isSignUp ? 'Already have an account?' : "Don't have an account?"}
		<button on:click={() => isSignUp = !isSignUp}>
			{isSignUp ? 'Sign In' : 'Sign Up'}
		</button>
	</div>
	
	<div class="toggle-auth" style="margin-top: 2rem;">
		<button on:click={() => goto('/')}>
			← Back to Search
		</button>
	</div>
</div>