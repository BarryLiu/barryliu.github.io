export type AuthEnv = {
  AUTH_COOKIE_SECRET?: string;
  GITHUB_OAUTH_CLIENT_ID?: string;
  GITHUB_OAUTH_CLIENT_SECRET?: string;
  CF_GITHUB_OAUTH_CLIENT_ID?: string;
  CF_GITHUB_OAUTH_CLIENT_SECRET?: string;
};

export type GitHubUser = {
  id: number;
  login: string;
  name?: string | null;
  avatar_url?: string | null;
  html_url?: string | null;
};

export type AuthSession = {
  provider: 'github';
  user: GitHubUser;
  iat: number;
};

export const authCookieName = 'ff_auth';
export const stateCookieName = 'ff_oauth_state';
const encoder = new TextEncoder();
const decoder = new TextDecoder();
const sessionMaxAge = 60 * 60 * 24 * 30;
const stateMaxAge = 60 * 10;

export function getGitHubOAuthConfig(env: AuthEnv) {
  const clientId = env.GITHUB_OAUTH_CLIENT_ID ?? env.CF_GITHUB_OAUTH_CLIENT_ID;
  const clientSecret = env.GITHUB_OAUTH_CLIENT_SECRET ?? env.CF_GITHUB_OAUTH_CLIENT_SECRET;
  if (!env.AUTH_COOKIE_SECRET || !clientId || !clientSecret) return null;
  return {
    authCookieSecret: env.AUTH_COOKIE_SECRET,
    clientId,
    clientSecret,
  };
}

export function createOAuthState() {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  return [...bytes].map((byte) => byte.toString(16).padStart(2, '0')).join('');
}

function base64UrlEncode(value: string | ArrayBuffer) {
  const bytes = typeof value === 'string' ? encoder.encode(value) : new Uint8Array(value);
  let binary = '';
  bytes.forEach((byte) => {
    binary += String.fromCharCode(byte);
  });
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
}

function base64UrlDecode(value: string) {
  const normalized = value.replace(/-/g, '+').replace(/_/g, '/');
  const padded = normalized.padEnd(Math.ceil(normalized.length / 4) * 4, '=');
  const binary = atob(padded);
  const bytes = new Uint8Array(binary.length);
  for (let index = 0; index < binary.length; index += 1) {
    bytes[index] = binary.charCodeAt(index);
  }
  return decoder.decode(bytes);
}

async function signingKey(secret: string) {
  return crypto.subtle.importKey('raw', encoder.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
}

async function signPayload(payload: string, secret: string) {
  const key = await signingKey(secret);
  const signature = await crypto.subtle.sign('HMAC', key, encoder.encode(payload));
  return base64UrlEncode(signature);
}

async function safeEqual(left: string, right: string) {
  if (left.length !== right.length) return false;
  let diff = 0;
  for (let index = 0; index < left.length; index += 1) {
    diff |= left.charCodeAt(index) ^ right.charCodeAt(index);
  }
  return diff === 0;
}

export function parseCookies(request: Request) {
  const header = request.headers.get('cookie') ?? '';
  const cookies = new Map<string, string>();
  for (const chunk of header.split(';')) {
    const [name, ...rest] = chunk.trim().split('=');
    if (!name || !rest.length) continue;
    cookies.set(name, decodeURIComponent(rest.join('=')));
  }
  return cookies;
}

export function buildCookie(name: string, value: string, maxAge: number, request?: Request) {
  const encodedValue = encodeURIComponent(value);
  const secure = request ? new URL(request.url).protocol === 'https:' : true;
  return `${name}=${encodedValue}; Max-Age=${maxAge}; Path=/; HttpOnly; ${secure ? 'Secure; ' : ''}SameSite=Lax`;
}

export function clearCookie(name: string, request?: Request) {
  const secure = request ? new URL(request.url).protocol === 'https:' : true;
  return `${name}=; Max-Age=0; Path=/; HttpOnly; ${secure ? 'Secure; ' : ''}SameSite=Lax`;
}

export function sanitizeReturnTo(raw: string | null) {
  if (!raw) return '/';
  if (!raw.startsWith('/')) return '/';
  if (raw.startsWith('//')) return '/';
  return raw;
}

export async function createSignedValue(payload: unknown, secret: string) {
  const encodedPayload = base64UrlEncode(JSON.stringify(payload));
  const signature = await signPayload(encodedPayload, secret);
  return `${encodedPayload}.${signature}`;
}

export async function readSignedValue<T>(request: Request, cookieName: string, secret: string) {
  const raw = parseCookies(request).get(cookieName);
  if (!raw) return null;
  const [payload, signature] = raw.split('.');
  if (!payload || !signature) return null;
  const expected = await signPayload(payload, secret);
  if (!(await safeEqual(signature, expected))) return null;
  try {
    return JSON.parse(base64UrlDecode(payload)) as T;
  } catch {
    return null;
  }
}

export async function createSessionCookie(session: AuthSession, secret: string, request?: Request) {
  return buildCookie(authCookieName, await createSignedValue(session, secret), sessionMaxAge, request);
}

export async function createStateCookie(state: string, returnTo: string, secret: string, request?: Request) {
  return buildCookie(stateCookieName, await createSignedValue({ state, returnTo }, secret), stateMaxAge, request);
}

export async function readSession(request: Request, env: AuthEnv) {
  if (!env.AUTH_COOKIE_SECRET) return null;
  const session = await readSignedValue<AuthSession>(request, authCookieName, env.AUTH_COOKIE_SECRET);
  if (!session || session.provider !== 'github' || !session.user?.id || !session.user?.login) return null;
  return session;
}
