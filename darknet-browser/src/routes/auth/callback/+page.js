import { redirect } from '@sveltejs/kit'

export async function load({ url }) {
  // This route handles the OAuth callback from Supabase
  // After auth, redirect to home
  throw redirect(303, '/')
}