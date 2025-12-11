import { createClient } from '@supabase/supabase-js'
import { env as publicEnv } from '$env/dynamic/public'

const supabaseUrl = publicEnv.PUBLIC_SUPABASE_URL
const supabaseKey = publicEnv.PUBLIC_SUPABASE_KEY

// DEBUG: Logging hinzufügen
console.log('=== SUPABASE INIT DEBUG ===')
console.log('PUBLIC_SUPABASE_URL:', supabaseUrl ? '✓ Present' : '✗ MISSING')
console.log('PUBLIC_SUPABASE_KEY:', supabaseKey ? `✓ Present (${supabaseKey.substring(0, 10)}...)` : '✗ MISSING')

if (!supabaseUrl || !supabaseKey) {
  console.error('CRITICAL: Missing Supabase environment variables!')
  console.error('PUBLIC_SUPABASE_URL:', supabaseUrl)
  console.error('PUBLIC_SUPABASE_KEY:', supabaseKey)
  console.warn('Supabase will not work properly!')
} else {
  console.log('✓ Supabase credentials OK')
}
console.log('===========================')

export const supabase = createClient(supabaseUrl, supabaseKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: false,
    storage: {
      getItem: (key) => {
        if (typeof window !== 'undefined') {
          return window.localStorage.getItem(key)
        }
        return null
      },
      setItem: (key, value) => {
        if (typeof window !== 'undefined') {
          window.localStorage.setItem(key, value)
        }
      },
      removeItem: (key) => {
        if (typeof window !== 'undefined') {
          window.localStorage.removeItem(key)
        }
      }
    }
  }
})

// Helper function to check auth and get fresh session
export async function requireAuth() {
  console.log('requireAuth() called')
  const { data: { session }, error } = await supabase.auth.getSession()
  
  if (error || !session) {
    console.error('Auth error:', error)
    console.log('No session found, throwing error')
    throw new Error('Not authenticated')
  }
  
  console.log('Session found for user:', session.user.email)
  return session
}

// Get current user with fresh check
export async function getCurrentUser() {
  console.log('getCurrentUser() called')
  const { data: { user }, error } = await supabase.auth.getUser()
  
  if (error) {
    console.error('Get user error:', error)
    return null
  }
  
  console.log('User found:', user?.email)
  return user
}

// Log search to database
export async function logSearch(userId, query, resultsCount = 0) {
  console.log('logSearch() called:', { userId, query, resultsCount })
  
  try {
    const { error } = await supabase
      .from('search_logs')
      .insert({
        user_id: userId,
        query: query,
        results_count: resultsCount,
        metadata: {
          user_agent: typeof window !== 'undefined' ? window.navigator.userAgent : 'server',
          timestamp: new Date().toISOString()
        }
      })
    
    if (error) {
      console.error('Failed to log search:', error.message)
      return false
    }
    
    console.log('Search logged successfully')
    return true
  } catch (error) {
    console.error('Error logging search:', error.message)
    return false
  }
}