// 서버 코드 검사: node handoff/worklog/test-worklogs.mjs  (Node 22 이상, 설치할 것 없음)
import assert from 'node:assert/strict';
import { makeEnv } from './fake-env.mjs';

const { env, worklogRoute } = makeEnv('2026-11-05');
const DB = env.DB;

const A = { name: '곽남훈', role: 'admin' }, S1 = { name: '문은영', role: 'staff' }, S2 = { name: '이미람', role: 'staff' }, V = { name: '보기', role: 'viewer' };
async function call(me, m, path, b) {
  const url = new URL('https://x' + path);
  const req = new Request(url, { method: m, body: b ? JSON.stringify(b) : undefined });
  const r = await worklogRoute(req, { DB }, me, url.pathname, m, url);
  return { s: r.status, j: await r.json() };
}
const plan = { kind: '휴일', dept: '동원앵커사업단', position: '전담직원', plan_date: '2026-10-10', plan_start: '08:30', plan_end: '17:30', plan_text: '교육과정 운영' };
const report = { actual_date: '2026-10-10', actual_start: '08:30', actual_end: '17:30', report_text: '교육과정 운영\n참여 15명' };

assert.equal(await worklogRoute(new Request('https://x/api/admin/expenses'), { DB }, S1, '/api/admin/expenses', 'GET', new URL('https://x/')), null, '다른 주소는 건드리지 않음');
assert.equal((await call(S1, 'POST', '/api/admin/worklogs', { ...plan, kind: '야간' })).s, 400, '구분 검사');
assert.equal((await call(S1, 'POST', '/api/admin/worklogs', { ...plan, plan_text: ' ' })).s, 400, '근무계획 필수');
assert.equal((await call(V, 'POST', '/api/admin/worklogs', plan)).s, 403, '보기 전용은 작성 불가');

const id1 = (await call(S1, 'POST', '/api/admin/worklogs', { ...plan, user_name: '남의이름' })).j.id;
const id2 = (await call(S2, 'POST', '/api/admin/worklogs', { ...plan, kind: '연장', plan_date: '2026-10-16', plan_start: '17:30', plan_end: '21:30' })).j.id;
let mine = (await call(S1, 'GET', '/api/admin/worklogs?year=2026')).j;
assert.deepEqual(mine.map(r => r.id), [id1], '담당자는 내 것만 봄');
assert.equal(mine[0].user_name, '문은영', '신청자 이름은 로그인 계정으로 고정');
assert.equal(mine[0].plan_hours, 9);
assert.equal((await call(A, 'GET', '/api/admin/worklogs?year=2026')).j.length, 2, '관리자는 전체');
assert.equal((await call(S1, 'GET', `/api/admin/worklogs?year=2025`)).j.length, 1, '결과보고서 미제출 건은 해가 달라도 보임');

assert.equal((await call(S1, 'PUT', `/api/admin/worklogs/${id2}`, plan)).s, 404, '남의 신청서 수정 불가');
assert.equal((await call(S1, 'PUT', `/api/admin/worklogs/${id2}/report`, report)).s, 404, '남의 결과보고서 작성 불가');
assert.equal((await call(A, 'PUT', `/api/admin/worklogs/${id1}/approve`, { approved_hours: 8 })).s, 409, '결과보고서 전에는 산정 불가');

assert.equal((await call(S1, 'PUT', `/api/admin/worklogs/${id1}/report`, report)).s, 200);
mine = (await call(S1, 'GET', '/api/admin/worklogs?year=2026')).j;
assert.ok(mine[0].reported_at && mine[0].actual_hours === 9, '결과보고서 저장 → reported_at 기록');
assert.equal((await call(S1, 'GET', '/api/admin/worklogs?year=2025')).j.length, 0, '제출한 건은 다른 해 목록에서 빠짐');
assert.equal((await call(S1, 'PUT', `/api/admin/worklogs/${id1}`, plan)).s, 409, '제출 뒤 신청서 수정 잠금');
assert.equal((await call(S1, 'DELETE', `/api/admin/worklogs/${id1}`)).s, 409, '제출 뒤 삭제 잠금');

assert.equal((await call(S1, 'PUT', `/api/admin/worklogs/${id1}/approve`, { approved_hours: 8 })).s, 403, '담당자는 산정 불가');
assert.equal((await call(A, 'PUT', `/api/admin/worklogs/${id1}/approve`, { approved_hours: 30 })).s, 400);
assert.equal((await call(A, 'PUT', `/api/admin/worklogs/${id1}/approve`, { approved_hours: 8 })).s, 200);
mine = (await call(S1, 'GET', '/api/admin/worklogs?year=2026')).j[0];
assert.equal(mine.approved_hours, 8); assert.equal(mine.checker, '곽남훈');
assert.equal((await call(S1, 'PUT', `/api/admin/worklogs/${id1}/report`, report)).s, 409, '산정 뒤 결과보고서 잠금');

const night = (await call(S2, 'POST', '/api/admin/worklogs', { ...plan, plan_start: '18:00', plan_end: '02:00' })).j.id;
assert.equal((await call(S2, 'GET', '/api/admin/worklogs?year=2026')).j.find(r => r.id === night).plan_hours, 8, '자정 넘김');
const brk = (await call(S2, 'POST', '/api/admin/worklogs', { ...plan, plan_hours: '8' })).j.id;
assert.equal((await call(S2, 'GET', '/api/admin/worklogs?year=2026')).j.find(r => r.id === brk).plan_hours, 8, '휴게 뺀 근무시간을 직접 넣으면 그 값');
assert.equal((await call(S2, 'DELETE', `/api/admin/worklogs/${night}`)).s, 200, '미제출 건은 본인이 삭제 가능');
console.log('근무 신청 API 검사 통과');
