import { API_URL } from '$env/static/private';

/** @type {import('./$types').Actions} */
export const actions = {
  default: async ({ request }) => {
    const formData = await request.formData();
    const query = formData.get('query');

    try {
      const response = await fetch(`${API_URL}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query })
      });

      if (response.ok) {
        const data = await response.json();
        return { success: true, results: data.results };
      } else {
        return { success: false, error: 'Search failed' };
      }
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  }
};