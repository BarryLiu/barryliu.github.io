import { createOAuthState, createStateCookie, getGitHubOAuthConfig, sanitizeReturnTo, type AuthEnv } from '../../../_lib/auth';
import { json, redirect } from '../../../_lib/http';

export const onRequestGet = async ({ request, env }: { request: Request; env: AuthEnv }) => {
  const config = getGitHubOAuthConfig(env);
  if (!config) return json({ error: 'github_oauth_unavailable' }, { status: 503 });

  const url = new URL(request.url);
  const state = createOAuthState();
  const returnTo = sanitizeReturnTo(url.searchParams.get('returnTo'));
  const callbackUrl = new URL('/api/auth/github/callback', url.origin);
  const authorizeUrl = new URL('https://github.com/login/oauth/authorize');

  authorizeUrl.searchParams.set('client_id', config.clientId);
  authorizeUrl.searchParams.set('redirect_uri', callbackUrl.toString());
  authorizeUrl.searchParams.set('scope', 'read:user');
  authorizeUrl.searchParams.set('state', state);
  authorizeUrl.searchParams.set('allow_signup', 'true');

  return redirect(authorizeUrl.toString(), {
    headers: {
      'set-cookie': await createStateCookie(state, returnTo, config.authCookieSecret, request),
    },
  });
};
