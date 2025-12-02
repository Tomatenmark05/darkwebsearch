import { json } from '@sveltejs/kit';

export async function POST({ request }) {
  try {
    const { query } = await request.json();
    
    if (!query) {
      return json({ error: 'Query is required' }, { status: 400 });
    }
    
    // Mock response - in production, this would connect to manager
    console.log(`Search query received: ${query}`);
    
    return json({
      success: true,
      query,
      results: [
        {
          title: `Search result for: ${query}`,
          description: 'This is a mock result from the GUI service. In production, this would come from the Manager service.',
          timestamp: new Date().toISOString(),
          source: 'Mock Service'
        },
        {
          title: 'Test Result 2',
          description: 'Another example result for testing the GUI interface.',
          timestamp: new Date().toISOString(),
          source: 'Test Source'
        },
        {
          title: 'Test Result 3',
          description: 'Demonstrating search functionality in the DarkWeb Browser GUI.',
          timestamp: new Date().toISOString(),
          source: 'Demo Source'
        }
      ]
    });
    
  } catch (error) {
    console.error('Search error:', error);
    return json({ 
      error: 'Internal server error',
      details: error.message 
    }, { status: 500 });
  }
}