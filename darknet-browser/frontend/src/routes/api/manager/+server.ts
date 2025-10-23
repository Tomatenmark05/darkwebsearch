import type { RequestHandler } from '@sveltejs/kit';

export const GET: RequestHandler = async ({ request }) => {
  const authHeader = request.headers.get('authorization');
  if (!authHeader) {
    return new Response('Unauthorized', { status: 401 });
  }

  // Simulate manager response
  return new Response('Hello from the manager API!');
};
