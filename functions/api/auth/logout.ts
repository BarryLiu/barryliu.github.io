import { authCookieName, clearCookie, sanitizeReturnTo } from '../../_lib/auth';
import { redirect } from '../../_lib/http';

function logout(request: Request) {
  const url = new URL(request.url);
  return redirect(sanitizeReturnTo(url.searchParams.get('returnTo')), {
    headers: {
      'set-cookie': clearCookie(authCookieName, request),
    },
  });
}

export const onRequestGet = async ({ request }: { request: Request }) => logout(request);
export const onRequestPost = async ({ request }: { request: Request }) => logout(request);
