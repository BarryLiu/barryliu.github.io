export function json(body: unknown, init: ResponseInit = {}) {
  const headers = new Headers(init.headers);
  headers.set('content-type', headers.get('content-type') ?? 'application/json; charset=utf-8');
  headers.set('cache-control', headers.get('cache-control') ?? 'no-store');
  return new Response(JSON.stringify(body), {
    ...init,
    headers,
  });
}

export function redirect(location: string, init: ResponseInit = {}) {
  const headers = new Headers(init.headers);
  headers.set('location', location);
  headers.set('cache-control', headers.get('cache-control') ?? 'no-store');
  return new Response(null, {
    status: 302,
    ...init,
    headers,
  });
}
