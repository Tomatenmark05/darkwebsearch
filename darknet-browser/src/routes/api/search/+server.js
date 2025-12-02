import { json } from '@sveltejs/kit'

export async function POST({ request }) {
  try {
    // Get authorization header
    const authHeader = request.headers.get('Authorization')
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return json({ 
        error: 'Missing or invalid authorization token',
        code: 'AUTH_MISSING'
      }, { status: 401 })
    }
    
    const token = authHeader.split('Bearer ')[1]
    
    // Korrekte Supabase URL und ANON KEY
    const supabaseUrl = 'https://owddlfgtopfeqbkmwsox.supabase.co'
    const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im93ZGRsZmd0b3BmZXFia213c294Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ2ODg1MTAsImV4cCI6MjA4MDI2NDUxMH0.mMKdgjR0bItJ3Kxrcn6FDWWnlSPAOq1IxodwFb2C0Ak'
    
    // Token direkt mit Supabase REST API validieren
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
    
    const { query } = await request.json()
    
    if (!query) {
      return json({ error: 'Query is required' }, { status: 400 })
    }
    
    // Vereinfachte Mock Response - nur Title und Description
    return json({
      success: true,
      query,
      results: [
        {
          title: `Search result: ${query}`,
          description: 'Analysis of encrypted network patterns and darkweb intelligence for the provided search query.'
        },
        {
          title: 'Encrypted Communications',
          description: 'Intercepted encrypted communications matching your search parameters across multiple onion networks.'
        },
        {
          title: 'Network Intelligence',
          description: 'Compiled intelligence report based on network traffic analysis and pattern recognition algorithms.'
        },
        {
          title: 'Security Analysis',
          description: 'Security assessment and vulnerability analysis for systems mentioned in the search context.'
        },
        {
          title: 'Data Correlation',
          description: 'Cross-referenced data from multiple darkweb sources showing significant correlation with search terms.'
        }
      ],
      metadata: {
        search_id: crypto.randomUUID(),
        timestamp: new Date().toISOString()
      }
    })
    
  } catch (error) {
    console.error('API Error:', error)
    
    return json({
      success: false,
      error: error.message,
      results: []
    }, { status: 500 })
  }
}