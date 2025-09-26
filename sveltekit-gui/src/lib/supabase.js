import { createClient } from '@supabase/supabase-js'
import { env } from '$env/dynamic/public'

// Supabase configuration
const supabaseUrl = env.PUBLIC_SUPABASE_URL || 'https://your-project.supabase.co'
const supabaseAnonKey = env.PUBLIC_SUPABASE_ANON_KEY || 'your-anon-key'

// Create and export Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey)