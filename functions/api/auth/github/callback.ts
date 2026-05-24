import {
  clearCookie,
  createSessionCookie,
  getGitHubOAuthConfig,
  readSignedValue,
  sanitizeReturnTo,
  stateCookieName,
  type AuthEnv,
  type GitHubUser,
} from '../../../_lib/auth';
import { json, redirect } from '../../../_lib/http';

type StatePayload = {
  state: string;
  returnTo: string;
};

type GitHubTokenResponse = {
  access_token?: string;
  error?: string;
  error_description?: string;
};

function withAuthStatus(returnTo: string, status: string, request: Request) {
  const target = new URL(sanitizeReturnTo(returnTo), new URL(request.url).origin);
  target.searchParams.set('auth', status);
  return `${target.pathname}${target.search}${target.hash}`;
}

function failureRedirect(request: Request, returnTo: string, status = 'failed') {
  return redirect(withAuthStatus(returnTo, status, request), {
    headers: {
      'set-cookie': clearCookie(stateCookieName, request),
    },
  });
}

export const onRequestGet = async ({ request, env }: { request: Request; env: AuthEnv }) => {
  const config = getGitHubOAuthConfig(env);
  if (!config) return json({ error: 'github_oauth_unavailable' }, { status: 503 });

  const url = new URL(request.url);
  const code = url.searchParams.get('code');
  const state = url.searchParams.get('state');
  const savedState = await readSignedValue<StatePayload>(request, stateCookieName, config.authCookieSecret);
  const returnTo = sanitizeReturnTo(savedState?.returnTo ?? '/');

  if (!code || !state || !savedState || savedState.state !== state) {
    return failureRedirect(request, returnTo, 'state');
  }

  const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      'user-agent': 'barryliu-github-io',
    },
    body: JSON.stringify({
      client_id: config.clientId,
      client_secret: config.clientSecret,
      code,
      redirect_uri: new URL('/api/auth/github/callback', url.origin).toString(),
    }),
  });
  const token = (await tokenResponse.json().catch(() => ({}))) as GitHubTokenResponse;
  if (!tokenResponse.ok || !token.access_token || token.error) {
    return failureRedirect(request, returnTo, 'token');
  }

  const userResponse = await fetch('https://api.github.com/user', {
    headers: {
      accept: 'application/vnd.github+json',
      authorization: `Bearer ${token.access_token}`,
      'user-agent': 'barryliu-github-io',
      'x-github-api-version': '2022-11-28',
    },
  });
  const user = (await userResponse.json().catch(() => ({}))) as Partial<GitHubUser>;
  if (!userResponse.ok || !user.id || !user.login) {
    return failureRedirect(request, returnTo, 'user');
  }

  const headers = new Headers();
  headers.set('location', returnTo);
  headers.set('cache-control', 'no-store');
  headers.append('set-cookie', clearCookie(stateCookieName, request));
  headers.append('set-cookie', await createSessionCookie({
    provider: 'github',
    user: {
      id: user.id,
      login: user.login,
      name: user.name ?? null,
      avatar_url: user.avatar_url ?? null,
      html_url: user.html_url ?? null,
    },
    iat: Math.floor(Date.now() / 1000),
  }, config.authCookieSecret, request));

  return new Response(null, { status: 302, headers });
};
