// 테스트·미리보기 전용: 진짜 D1 대신 Node 내장 sqlite(메모리)로 같은 모양(prepare/bind/all/first/run)을 흉내 내고,
// 운영 코드에 이미 있는 도우미(json, bad, body, str, isDate, kstToday)를 넣어 worker-worklogs.js를 불러옴.
import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';

const dir = new URL('.', import.meta.url);
export function makeEnv(today = new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10)) {
  const sql = new DatabaseSync(':memory:');
  sql.exec(readFileSync(new URL('schema.sql', dir), 'utf8'));
  const DB = { prepare: q => { let a = []; const st = sql.prepare(q); return {
    bind(...x) { a = x; return this; },
    async all() { return { results: st.all(...a) }; },
    async first() { return st.get(...a) ?? null; },
    async run() { const r = st.run(...a); return { meta: { last_row_id: Number(r.lastInsertRowid) } }; } }; } };
  // 아래 도우미는 dist-lifelong-schedule-test/src/worker.src.js 와 같음
  const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'content-type': 'application/json; charset=utf-8' } });
  const bad = (error, status = 400) => json({ error }, status);
  const body = req => req.json().catch(() => null);
  const str = (v, max = 2000) => (v === undefined || v === null || String(v).trim() === '') ? null : String(v).trim().slice(0, max);
  const isDate = v => typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v);
  const kstToday = () => today;
  const worklogRoute = new Function('json', 'bad', 'body', 'str', 'isDate', 'kstToday',
    readFileSync(new URL('worker-worklogs.js', dir), 'utf8') + '\nreturn worklogRoute;')(json, bad, body, str, isDate, kstToday);
  return { env: { DB }, worklogRoute };
}
