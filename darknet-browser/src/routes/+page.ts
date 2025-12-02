import type { PageLoad } from './$types';

export const load: PageLoad = async () => {
  return {
    meta: {
      title: 'DarkWeb Browser',
      description: 'Secure search interface for authorized research'
    }
  };
};