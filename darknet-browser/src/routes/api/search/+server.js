import { json } from '@sveltejs/kit'
import { env as privateEnv } from '$env/dynamic/private'
import { env as publicEnv } from '$env/dynamic/public'

// Manager Service URL (in the shared-net NW)
const MANAGER_SERVICE_URL = 'http://manager:8000'

// Hilfsfunktion, um Manager-Ergebnisse zu normalisieren
function normalizeManagerResults(payload) {
  // Fall 1: Top-Level-Array
  if (Array.isArray(payload)) {
    return payload
  }

  // Fall 2: Objekt mit möglichen Ergebnis-Schlüsseln
  if (payload && typeof payload === 'object') {
    const candidateKeys = ['results', 'data', 'items', 'hits', 'documents', 'docs']
    for (const key of candidateKeys) {
      if (Array.isArray(payload[key])) {
        return payload[key]
      }
    }
  }

  // Nichts Passendes gefunden
  return []
}

export async function POST({ request }) {
  try {
    // 1. Authorization
    const authHeader = request.headers.get('Authorization')
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return json({ 
        error: 'Missing or invalid authorization token',
        code: 'AUTH_MISSING'
      }, { status: 401 })
    }
    
    const token = authHeader.split('Bearer ')[1]
    
    // 2. Supabase Token Verification
    const supabaseUrl = privateEnv.SUPABASE_URL || publicEnv.PUBLIC_SUPABASE_URL
    const supabaseKey = privateEnv.SUPABASE_SERVICE_ROLE_KEY

    if (!supabaseUrl || !supabaseKey) {
      return json({ error: 'Server misconfiguration' }, { status: 500 })
    }
    
    const verifyResponse = await fetch(`${supabaseUrl}/auth/v1/user`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'apikey': supabaseKey
      }
    })
    
    if (!verifyResponse.ok) {
      return json({ 
        error: 'Invalid authentication token',
        code: 'AUTH_INVALID'
      }, { status: 401 })
    }
    
    const userData = await verifyResponse.json()
    
    if (!userData || !userData.id) {
      return json({ 
        error: 'User not found in token',
        code: 'USER_NOT_FOUND'
      }, { status: 401 })
    }
    
    // 3. Query from Request
    const { query } = await request.json()
    
    if (!query || typeof query !== 'string' || query.trim().length === 0) {
      return json({ 
        error: 'Query is required and must be a non-empty string',
        code: 'QUERY_INVALID'
      }, { status: 400 })
    }
    
    const trimmedQuery = query.trim()
    
    // 4. Forward to manager (if running)
    console.log(`=== DEBUG: Vorbereitung für Manager Request ===`)
    console.log(`Search query: ${trimmedQuery}`)
    console.log(`User: ${userData.email} (ID: ${userData.id})`)
    console.log(`Manager URL: ${MANAGER_SERVICE_URL}`)
    
    try {
      // Try to reach manager
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000) // 5s timeout
      
      // REQUEST BODY for debugging
      const requestBody = {
        query: trimmedQuery,
        user: {
          id: userData.id,
          email: userData.email
        }
      }
      
      console.log(`=== DEBUG: Sende Request an Manager ===`)
      console.log(`URL: ${MANAGER_SERVICE_URL}/search`)
      console.log(`Method: POST`)
      console.log(`Headers: Content-Type: application/json, Accept: application/json`)
      console.log(`Body: ${JSON.stringify(requestBody, null, 2)}`)
      console.log(`========================================`)
      
      const managerResponse = await fetch(`${MANAGER_SERVICE_URL}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal
      })
      
      clearTimeout(timeoutId)
      
      console.log(`=== DEBUG: Response vom Manager ===`)
      console.log(`Status: ${managerResponse.status} ${managerResponse.statusText}`)
      
      if (managerResponse.ok) {
        const managerData = await managerResponse.json()
        const normalizedResults = normalizeManagerResults(managerData)
        console.log(`Response Data (normalized length): ${normalizedResults.length}`)
        console.log(`Preview: ${JSON.stringify(normalizedResults[0] || {}).substring(0, 200)}...`)
        console.log(`========================================`)
        
        // Return results from manager (normalisiert)
        return json({
          success: true,
          query: trimmedQuery,
          user_id: userData.id,
          results: normalizedResults,
          metadata: {
            search_id: crypto.randomUUID(),
            timestamp: new Date().toISOString(),
            results_count: normalizedResults.length,
            source: 'manager-service',
            raw_shape: Array.isArray(managerData) ? 'array' : 'object'
          }
        })
      } else {
        // Manager responds with error
        const errorText = await managerResponse.text()
        console.log(`Error Response: ${errorText}`)
        console.log(`========================================`)
        throw new Error(`Manager responded with ${managerResponse.status}: ${errorText}`)
      }
      
    } catch (managerError) {
      // Manager not reachable or error
      console.log(`=== DEBUG: Manager Fehler ===`)
      console.log(`Error: ${managerError.message}`)
      console.log(`Using fallback results`)
      console.log(`========================================`)
      
      // FALLBACK: Static results (as before)
      return json({
        success: true,
        query: trimmedQuery,
        user_id: userData.id,
        results: getFallbackResults(trimmedQuery),
        metadata: {
          search_id: crypto.randomUUID(),
          timestamp: new Date().toISOString(),
          results_count: 5,
          source: 'fallback',
          manager_error: managerError.message
        }
      })
    }
    
  } catch (error) {
    console.error('=== DEBUG: API Error ===')
    console.error(error)
    
    return json({
      success: false,
      error: 'Internal server error',
      code: 'INTERNAL_ERROR',
      results: []
    }, { status: 500 })
  }
}

// Fallback function (previous static results)
function getFallbackResults(query) {
  return [
    {
      title: `Search result: ${query}`,
      description: 'Analysis of encrypted network patterns and darknet intelligence for the provided search query.',
      source: 'fallback'
    },
    {
      title: 'Encrypted Communications',
      description: 'Intercepted encrypted communications matching your search parameters across multiple onion networks.',
      source: 'fallback'
    },
    {
      title: 'Network Intelligence',
      description: 'Compiled intelligence report based on network traffic analysis and pattern recognition algorithms.',
      source: 'fallback'
    },
    {
      title: 'Security Analysis',
      description: 'Security assessment and vulnerability analysis for systems mentioned in the search context.',
      source: 'fallback'
    },
    {
      title: 'Data Correlation',
      description: 'Cross-referenced data from multiple darknet sources showing significant correlation with search terms.',
      source: 'fallback'
    }
  ]
}