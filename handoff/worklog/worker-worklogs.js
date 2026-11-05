// ===== 근무 신청(연장·휴일) API — 운영 _worker.js(=src/worker.src.js)에 붙여 넣기 =====
// 붙이는 곳: 관리자 로그인 확인이 끝나 "로그인한 계정(me = {name, role})"을 알게 된 바로 뒤.
//   const r = await worklogRoute(req, env, me, p, m, url); if (r) return r;
// 기존 도우미 json, bad, body, str, isDate, kstToday 를 그대로 씀 (운영 코드에 이미 있음).
//
// 권한 (서버에서 검사 — 화면에서 숨기는 것만으로는 막히지 않음)
//   admin  : 전체 신청서 보기·수정·삭제, 산정 실근무시간 입력
//   staff  : 내 신청서만 보기·작성. 결과보고서를 낸 뒤에는 신청서 수정·삭제 불가, 산정된 뒤에는 결과보고서도 수정 불가
//   viewer : 내 것 보기만 (작성 불가)
//
// GET    /api/admin/worklogs?year=2026        그 해 신청서 + 해를 넘긴 결과보고서 미제출 건
// POST   /api/admin/worklogs                  신청서 작성
// PUT    /api/admin/worklogs/:id              신청서 수정
// DELETE /api/admin/worklogs/:id              신청서 삭제
// PUT    /api/admin/worklogs/:id/report       결과보고서 작성·수정 (처음 저장할 때 reported_at 기록 → 목록에서 빠짐)
// PUT    /api/admin/worklogs/:id/approve      산정 실근무시간 (관리자)

const WL_KIND = ['연장', '휴일'];
const isHm = v => typeof v === 'string' && /^([01]\d|2[0-3]):[0-5]\d$/.test(v);
// 끝 시각이 시작보다 이르면 자정을 넘긴 것으로 봄 (예: 18:00~02:00 = 8시간)
const wlHours = (s, e) => {
  const mins = t => +t.slice(0, 2) * 60 + +t.slice(3);
  let d = mins(e) - mins(s); if (d <= 0) d += 1440;
  return Math.round(d / 6) / 10;
};
// 화면에서 근무시간(휴게 제외)을 고쳐 보냈으면 그 값, 없으면 시각으로 계산한 값
const wlHrs = (v, s, e) => { const n = Number(v); return v !== '' && v != null && n > 0 && n <= 24 ? Math.round(n * 10) / 10 : wlHours(s, e); };
const wlSet = f => Object.keys(f).map(k => `${k} = ?`).join(', ');

function wlPlan(b) {
  if (!WL_KIND.includes(b.kind)) return '구분(연장/휴일)을 고르세요.';
  if (!isDate(b.plan_date) || !isHm(b.plan_start) || !isHm(b.plan_end)) return '예정 근무일시를 확인하세요.';
  const plan_text = str(b.plan_text, 5000); if (!plan_text) return '근무계획을 입력하세요.';
  return { kind: b.kind, dept: str(b.dept, 100), position: str(b.position, 50),
    plan_date: b.plan_date, plan_start: b.plan_start, plan_end: b.plan_end, plan_hours: wlHrs(b.plan_hours, b.plan_start, b.plan_end),
    plan_text, apply_date: isDate(b.apply_date) ? b.apply_date : kstToday() };
}
function wlReport(b) {
  if (!isDate(b.actual_date) || !isHm(b.actual_start) || !isHm(b.actual_end)) return '실제 근무일시를 확인하세요.';
  const report_text = str(b.report_text, 5000); if (!report_text) return '근무내용을 입력하세요.';
  return { actual_date: b.actual_date, actual_start: b.actual_start, actual_end: b.actual_end,
    actual_hours: wlHrs(b.actual_hours, b.actual_start, b.actual_end), report_text, attach: str(b.attach, 500),
    report_date: isDate(b.report_date) ? b.report_date : kstToday() };
}

async function worklogRoute(req, env, me, p, m, url) {
  if (p !== '/api/admin/worklogs' && !p.startsWith('/api/admin/worklogs/')) return null;
  if (!me || !me.name) return bad('다시 로그인하세요.', 401);
  const DB = env.DB, admin = me.role === 'admin';
  if (me.role === 'viewer' && m !== 'GET') return bad('보기 전용 계정은 작성할 수 없습니다.', 403);

  if (p === '/api/admin/worklogs') {
    if (m === 'GET') {
      const y = url.searchParams.get('year'), year = /^\d{4}$/.test(y || '') ? y : kstToday().slice(0, 4);
      const where = '(substr(plan_date, 1, 4) = ? OR reported_at IS NULL)' + (admin ? '' : ' AND user_name = ?');
      const rows = await DB.prepare(`SELECT * FROM worklogs WHERE ${where} ORDER BY plan_date DESC, id DESC`)
        .bind(...(admin ? [year] : [year, me.name])).all();
      return json(rows.results);
    }
    if (m === 'POST') {
      const f = wlPlan(await body(req) || {}); if (typeof f === 'string') return bad(f);
      f.user_name = me.name;
      const r = await DB.prepare(`INSERT INTO worklogs (${Object.keys(f).join(', ')}) VALUES (${Object.keys(f).map(() => '?').join(', ')})`)
        .bind(...Object.values(f)).run();
      return json({ ok: true, id: r.meta.last_row_id });
    }
    return bad('없는 주소입니다.', 404);
  }

  const mm = /^\/api\/admin\/worklogs\/(\d+)(\/report|\/approve)?$/.exec(p);
  if (!mm) return bad('없는 주소입니다.', 404);
  const id = +mm[1], row = await DB.prepare('SELECT * FROM worklogs WHERE id = ?').bind(id).first();
  if (!row || (!admin && row.user_name !== me.name)) return bad('없는 신청서입니다.', 404); // 남의 것은 있는지도 알리지 않음

  if (!mm[2]) {
    if (!admin && row.reported_at) return bad('결과보고서를 낸 신청서는 고치거나 지울 수 없습니다. 담당자에게 요청하세요.', 409);
    if (m === 'PUT') {
      const f = wlPlan(await body(req) || {}); if (typeof f === 'string') return bad(f);
      await DB.prepare(`UPDATE worklogs SET ${wlSet(f)} WHERE id = ?`).bind(...Object.values(f), id).run();
      return json({ ok: true });
    }
    if (m === 'DELETE') {
      await DB.prepare('DELETE FROM worklogs WHERE id = ?').bind(id).run();
      return json({ ok: true, deleted: row }); // 운영의 감사기록(되살리기)에 row를 남기도록 연결할 것
    }
  }
  if (mm[2] === '/report' && m === 'PUT') {
    if (!admin && row.approved_hours != null) return bad('실근무시간이 산정된 결과보고서는 고칠 수 없습니다. 담당자에게 요청하세요.', 409);
    const f = wlReport(await body(req) || {}); if (typeof f === 'string') return bad(f);
    await DB.prepare(`UPDATE worklogs SET ${wlSet(f)}, reported_at = COALESCE(reported_at, datetime('now')) WHERE id = ?`)
      .bind(...Object.values(f), id).run();
    return json({ ok: true });
  }
  if (mm[2] === '/approve' && m === 'PUT') {
    if (!admin) return bad('관리자만 산정할 수 있습니다.', 403);
    if (!row.reported_at) return bad('결과보고서를 먼저 받아야 합니다.', 409);
    const v = (await body(req) || {}).approved_hours;
    const h = v === null || v === '' || v === undefined ? null : Number(v);
    if (h !== null && !(h >= 0 && h <= 24)) return bad('실근무시간은 0~24 사이 숫자로 입력하세요.');
    await DB.prepare('UPDATE worklogs SET approved_hours = ?, checker = ? WHERE id = ?').bind(h, h === null ? null : me.name, id).run();
    return json({ ok: true });
  }
  return bad('없는 주소입니다.', 404);
}
