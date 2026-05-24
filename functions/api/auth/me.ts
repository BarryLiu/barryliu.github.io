import { readSession, type AuthEnv } from '../../_lib/auth';
import { json } from '../../_lib/http';

export const onRequestGet = async ({ request, env }: { request: Request; env: AuthEnv }) => {
  const session = await readSession(request, env);
  if (!session) return json({ authenticated: false, user: null });
  return json({ authenticated: true, user: session.user });
};
