// Server-only GitHub Contents storage. No token is returned to clients.
const ROOT = 'https://api.github.com/repos/zodo15/';
export async function gh(path, method = 'GET', body) {
  const token = process.env.CARDS_GITHUB_TOKEN;
  if (!token) throw new Error('State storage credential unavailable');
  const r = await fetch(ROOT + path, { method, headers: { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json', 'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28' }, body: body === undefined ? undefined : JSON.stringify(body), cache: 'no-store', signal: AbortSignal.timeout(15000) });
  if (!r.ok) { const e = new Error('State storage request failed'); e.statusCode = r.status === 409 || r.status === 422 ? 409 : 503; throw e; }
  return r.json();
}
export async function getJSON(repo, path, branch) {
  const f = await gh(repo + '/contents/' + path + '?ref=' + encodeURIComponent(branch));
  if (!f.content || !f.sha) throw new Error('State content unavailable');
  return { value: JSON.parse(Buffer.from(f.content, 'base64').toString('utf8')), sha: f.sha };
}
export async function putJSON(repo, path, branch, value, sha, message) {
  if (!sha) throw new Error('State revision required');
  return gh(repo + '/contents/' + path, 'PUT', { branch, message, sha, content: Buffer.from(JSON.stringify(value)).toString('base64') });
}
let privateCheckedAt = 0;
export async function privateState() {
  if (Date.now() - privateCheckedAt > 60000) {
    const r = await gh('morning-paper-state');
    if (r.private !== true) throw new Error('Subscription repository must be private');
    privateCheckedAt = Date.now();
  }
}
export async function readSubs() {
  await privateState();
  const r = await getJSON('morning-paper-state', 'subscriptions.json', 'main');
  if (!Array.isArray(r.value)) throw new Error('Subscription state invalid');
  return r;
}
export async function mutateSubs(change) {
  for (let n = 0; n < 3; n++) {
    const r = await readSubs(); const next = change(r.value);
    if (JSON.stringify(next) === JSON.stringify(r.value)) return;
    try { await putJSON('morning-paper-state','subscriptions.json','main',next,r.sha,'Update private push state'); return; }
    catch (e) { if (e.statusCode !== 409 || n === 2) throw e; }
  }
}
