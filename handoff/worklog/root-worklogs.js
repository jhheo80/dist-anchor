// ===== 근무 신청(연장·휴일) 화면 코드 — 운영 루트 화면(src/root.html)의 <script> 끝에 붙여 넣기 =====
// 운영 화면에 이미 있는 것을 그대로 씀: $, esc, call(url, method, body), me {name, role}, canWrite, YEAR, TODAY
// 연결 2곳 (README 참고):
//   showTab(t): 탭 목록 배열에 'worklog' 추가, 그리고  if(t==='worklog') loadWorklogs();
//   signOut():  WL=[]; 추가 (로그아웃하면 남의 화면에 안 남게)
let WL = [], wlEdit = null, wlMode = 'plan';

const wlHourOf = (s, e) => { // 기본값 제안: 9시간 이상이면 휴게 1시간 뺌 (서식 예: 08:30~17:30 → 8시간). 다르면 직접 고침
  if (!s || !e) return '';
  const m = t => +t.slice(0, 2) * 60 + +t.slice(3);
  let d = (m(e) - m(s) + 1440) % 1440 || 1440; d /= 60;
  return d >= 9 ? d - 1 : d;
};
const WD = ['일', '월', '화', '수', '목', '금', '토'];
const wlDay = d => d ? `${d.slice(0, 4)}. ${+d.slice(5, 7)}. ${+d.slice(8)}.(${WD[new Date(d + 'T00:00:00Z').getUTCDay()]})` : '';
const wlSpan = (d, s, e, h) => d ? `${wlDay(d)} ${s} ~ ${e}(${h}시간)` : '';
const wlLong = d => d ? `${d.slice(0, 4)}년 ${+d.slice(5, 7)}월 ${+d.slice(8)}일` : '';
const wlMine = r => r.user_name === me?.name;

async function loadWorklogs() {
  if (!me) return;
  try { WL = await call(`/api/admin/worklogs?year=${YEAR}`, 'GET'); } catch (err) { $('#tWorklog').innerHTML = `<caption class="err">${esc(err.message)}</caption>`; return; }
  renderWorklogs();
}

function renderWorklogs() {
  const admin = me?.role === 'admin', openOnly = $('#wlOpenOnly').checked;
  const rows = WL.filter(r => !openOnly || !r.reported_at);
  $('#tWorklog').innerHTML = '<thead><tr><th>구분</th><th>신청자</th><th>예정 근무일시</th><th>신청일</th><th>결과보고서</th><th>산정 실근무시간</th><th></th></tr></thead><tbody>'
    + (rows.length ? rows.map(r => {
      const lockPlan = r.reported_at && !admin, lockRep = r.approved_hours != null && !admin;
      return `<tr>
        <td>${esc(r.kind)}</td><td>${esc(r.user_name)}</td>
        <td>${esc(wlSpan(r.plan_date, r.plan_start, r.plan_end, r.plan_hours))}</td>
        <td>${esc(r.apply_date)}</td>
        <td>${r.reported_at ? `<span class="wl-done">제출 ${esc(r.report_date || '')}</span>` : '<span class="wl-open">미제출</span>'}</td>
        <td>${admin && r.reported_at
          ? `<input type="number" class="wl-hours" min="0" max="24" step="0.5" value="${r.approved_hours ?? ''}" data-wlhours="${r.id}" aria-label="${esc(r.user_name)} 산정 실근무시간"> 시간`
          : r.approved_hours != null ? `${r.approved_hours}시간 (${esc(r.checker || '')})` : ''}</td>
        <td>
          <button type="button" data-wlprint="${r.id}">인쇄</button>
          ${lockPlan ? '' : `<button type="button" data-wlplan="${r.id}">신청서 수정</button>`}
          ${lockRep ? '' : `<button type="button" data-wlrep="${r.id}">${r.reported_at ? '결과보고서 수정' : '결과보고서 작성'}</button>`}
        </td></tr>`;
    }).join('') : `<tr><td colspan="7">${openOnly ? '결과보고서를 안 낸 신청서가 없습니다.' : '이 해에 낸 근무 신청서가 없습니다.'}</td></tr>`)
    + '</tbody>';
}

function wlOpen(mode, r) {
  wlMode = mode; wlEdit = r || null;
  const rep = mode === 'report', v = r || {};
  let saved = {}; try { saved = JSON.parse(localStorage.getItem('wlProfile') || '{}'); } catch {} // 소속·직위는 지난번 값 (이 브라우저에만)
  $('#fWl').reset(); $('#w_err').textContent = '';
  $('#wlTitle').textContent = rep ? `( ${v.kind} ) 근무 결과보고서` : r ? `( ${v.kind} ) 근무 사전신청서 수정` : '근무 사전신청서';
  $('#w_kind').value = v.kind || '연장';
  $('#w_name').value = v.user_name || me.name;
  $('#w_dept').value = v.dept ?? saved.dept ?? '';
  $('#w_position').value = v.position ?? saved.position ?? '';
  $('#w_pdate').value = v.plan_date || ''; $('#w_pstart').value = v.plan_start || ''; $('#w_pend').value = v.plan_end || '';
  $('#w_phours').value = v.plan_hours ?? '';
  $('#w_ptext').value = v.plan_text || '';
  $('#w_adate').value = v.apply_date || TODAY;
  // 결과보고서: 처음 쓸 때는 신청서 내용을 그대로 가져와 고치기만 하면 되게
  $('#w_rdate').value = v.actual_date || v.plan_date || '';
  $('#w_rstart').value = v.actual_start || v.plan_start || '';
  $('#w_rend').value = v.actual_end || v.plan_end || '';
  $('#w_rhours').value = v.actual_hours ?? v.plan_hours ?? '';
  $('#w_rtext').value = v.report_text || v.plan_text || '';
  $('#w_attach').value = v.attach || '';
  $('#w_repdate').value = v.report_date || TODAY;
  // 결과보고서 모드에서는 신청서 칸을 잠가 보여 주기만
  ['#w_kind', '#w_dept', '#w_position', '#w_pdate', '#w_pstart', '#w_pend', '#w_phours', '#w_ptext', '#w_adate'].forEach(s => $(s).disabled = rep);
  ['#w_rdate', '#w_rstart', '#w_rend', '#w_rhours', '#w_rtext'].forEach(s => $(s).required = rep);
  $('#wlRep').classList.toggle('hide', !rep);
  $('#w_del').classList.toggle('hide', rep || !r);
  $('#wlDlg').showModal();
  (rep ? $('#w_rtext') : $('#w_kind')).focus();
}

function wlPick() {
  const open = WL.filter(r => !r.reported_at && (me.role === 'admin' || wlMine(r)));
  $('#wlPickList').innerHTML = open.length
    ? open.map(r => `<li><button type="button" data-wlpick="${r.id}">( ${esc(r.kind)} ) ${esc(wlSpan(r.plan_date, r.plan_start, r.plan_end, r.plan_hours))}
        <small>${esc(r.user_name)} · 신청일 ${esc(r.apply_date)} · ${esc((r.plan_text || '').split('\n').find(l => l.trim()) || '')}</small></button></li>`).join('')
    : '<li>결과보고서를 쓸 신청서가 없습니다. 먼저 사전신청서를 작성하세요.</li>';
  $('#wlPick').showModal();
}

// 근무시간 기본값: 시각을 바꾸면 다시 제안
[['#w_pstart', '#w_pend', '#w_phours'], ['#w_rstart', '#w_rend', '#w_rhours']].forEach(([s, e, h]) =>
  [s, e].forEach(x => $(x).addEventListener('change', () => { const v = wlHourOf($(s).value, $(e).value); if (v !== '') $(h).value = v; })));

$('#wlNew').onclick = () => wlOpen('plan');
$('#wlNewReport').onclick = wlPick;
$('#wlOpenOnly').onchange = renderWorklogs;
$('#w_close').onclick = () => $('#wlDlg').close();
$('#wlPickList').onclick = e => { const b = e.target.closest('[data-wlpick]'); if (!b) return; $('#wlPick').close(); wlOpen('report', WL.find(r => r.id === +b.dataset.wlpick)); };
$('#tWorklog').addEventListener('click', e => {
  const b = e.target.closest('button'); if (!b) return;
  const r = WL.find(x => x.id === +(b.dataset.wlprint || b.dataset.wlplan || b.dataset.wlrep));
  if (!r) return;
  if (b.dataset.wlprint) wlPrint(r);
  else wlOpen(b.dataset.wlplan ? 'plan' : 'report', r);
});
$('#tWorklog').addEventListener('change', async e => {
  const el = e.target.closest('[data-wlhours]'); if (!el) return;
  try { await call(`/api/admin/worklogs/${el.dataset.wlhours}/approve`, 'PUT', { approved_hours: el.value }); await loadWorklogs(); }
  catch (err) { alert(err.message); }
});

$('#fWl').addEventListener('submit', async e => {
  e.preventDefault();
  const plan = { kind: $('#w_kind').value, dept: $('#w_dept').value, position: $('#w_position').value,
    plan_date: $('#w_pdate').value, plan_start: $('#w_pstart').value, plan_end: $('#w_pend').value, plan_hours: $('#w_phours').value,
    plan_text: $('#w_ptext').value, apply_date: $('#w_adate').value };
  const report = { actual_date: $('#w_rdate').value, actual_start: $('#w_rstart').value, actual_end: $('#w_rend').value, actual_hours: $('#w_rhours').value,
    report_text: $('#w_rtext').value, attach: $('#w_attach').value, report_date: $('#w_repdate').value };
  $('#w_save').disabled = true;
  try {
    if (wlMode === 'report') await call(`/api/admin/worklogs/${wlEdit.id}/report`, 'PUT', report);
    else await call(wlEdit ? `/api/admin/worklogs/${wlEdit.id}` : '/api/admin/worklogs', wlEdit ? 'PUT' : 'POST', plan);
    try { localStorage.setItem('wlProfile', JSON.stringify({ dept: plan.dept, position: plan.position })); } catch {}
    $('#wlDlg').close();
    await loadWorklogs();
  } catch (err) { $('#w_err').textContent = err.message; }
  finally { $('#w_save').disabled = false; }
});
$('#w_del').onclick = async () => {
  if (!wlEdit || !confirm('이 사전신청서를 지울까요?')) return;
  try { await call(`/api/admin/worklogs/${wlEdit.id}`, 'DELETE'); $('#wlDlg').close(); await loadWorklogs(); }
  catch (err) { $('#w_err').textContent = err.message; }
};

$('#wlCsv').onclick = () => {
  const head = ['구분', '신청자', '소속', '직위', '예정일', '예정시작', '예정끝', '예정시간', '신청일', '실제일', '실제시작', '실제끝', '실제시간', '결과보고서 작성일', '산정 실근무시간', '산정 담당'];
  const keys = ['kind', 'user_name', 'dept', 'position', 'plan_date', 'plan_start', 'plan_end', 'plan_hours', 'apply_date', 'actual_date', 'actual_start', 'actual_end', 'actual_hours', 'report_date', 'approved_hours', 'checker'];
  const q = v => `"${String(v ?? '').replace(/"/g, '""')}"`;
  const csv = '﻿' + [head, ...WL.map(r => keys.map(k => r[k]))].map(row => row.map(q).join(',')).join('\r\n');
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
  a.download = `근무신청_${YEAR}.csv`; a.click(); URL.revokeObjectURL(a.href);
};

// 인쇄: 종이 서식과 같은 모양 (1쪽 사전신청서, 결과보고서가 있으면 2쪽)
function wlPrint(r) {
  const nm = esc(r.user_name.split('').join(' ')), dp = `${esc(r.dept || '')}${r.position ? '/' + esc(r.position) : ''}`;
  const plan = `
  <section class="pg">
    <table class="sign"><tr><th rowspan="2" class="v">결<br>재</th><th>담 당</th><th>실 장</th><th>앵커사업단장</th></tr><tr><td></td><td></td><td></td></tr></table>
    <h1>( ${esc(r.kind)} ) 근무 사전신청서</h1>
    <table class="f">
      <tr><th style="width:16%">소속 / 직위</th><td style="width:40%">${dp}</td><th style="width:14%">신청자</th><td>${esc(r.user_name)}</td></tr>
      <tr><th>예정근무일시</th><td colspan="3" class="c">${esc(wlSpan(r.plan_date, r.plan_start, r.plan_end, r.plan_hours))}</td></tr>
      <tr class="big"><th>근무계획</th><td colspan="3" class="txt">${esc(r.plan_text)}</td></tr>
      <tr><th>참고사항</th><td colspan="3" class="note">1. 예정근무일시는 시간단위로 책정하여 기재(휴게 및 식사시간 모두 포함).<br>2. 근무 후 지체없이 행정지원팀으로 근무 결과보고서를 제출.<br>3. 월별 시간외 근로시간이 본인의 근로계약서 상 수당기준 시간을 초과할 경우 추가 수당 지급.</td></tr>
      <tr><td colspan="4" class="decl">위와 같이 ( ${esc(r.kind)} ) 근무를 신청하오니 허가하여 주시기 바랍니다.<p class="c">${esc(wlLong(r.apply_date))}</p><p class="r">신청자: ${nm} (서명)</p></td></tr>
    </table>
    <table class="f proc"><tr><th rowspan="2" style="width:16%">처리내역</th><td style="width:24%" class="c">결과보고서 제출여부</td><td style="width:18%" class="c">${r.reported_at ? '제출(후면첨부)' : ''}</td><th rowspan="2" style="width:12%">담당</th><td rowspan="2" class="c">${esc((r.checker || '').split('').join(' '))} (인)</td></tr>
      <tr><td class="c">산정 실근무시간</td><td class="c">${r.approved_hours != null ? r.approved_hours + '시간' : ''}</td></tr></table>
  </section>`;
  const rep = !r.reported_at ? '' : `
  <section class="pg">
    <h1>( ${esc(r.kind)} ) 근무 결과보고서</h1>
    <table class="f">
      <tr><th rowspan="2" style="width:12%">작성자</th><th style="width:14%">성 명</th><td class="c" style="width:22%">${esc(r.user_name)}</td><th style="width:16%">예정 근무일시</th><td class="c">${esc(wlSpan(r.plan_date, r.plan_start, r.plan_end, r.plan_hours))}</td></tr>
      <tr><th>소속 / 직위</th><td class="c">${dp}</td><th>실제 근무일시</th><td class="c">${esc(wlSpan(r.actual_date, r.actual_start, r.actual_end, r.actual_hours))}</td></tr>
      <tr class="big"><th>근무내용</th><td colspan="4" class="txt">${esc(r.report_text)}</td></tr>
      <tr><th>붙임</th><td colspan="4"><b>${r.attach ? '- ' + esc(r.attach) : ''}</b></td></tr>
      <tr><td colspan="5" class="decl">위와 같이 근무 결과보고서를 제출합니다.<p class="c">${esc(wlLong(r.report_date))}</p><p class="r">작성자: ${nm} (서명)</p></td></tr>
    </table>
  </section>`;
  const w = window.open('', '_blank');
  if (!w) { alert('팝업이 막혀 인쇄 창을 열지 못했습니다. 이 사이트의 팝업을 허용하세요.'); return; }
  w.document.write(`<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>${esc(r.kind)} 근무 ${esc(r.user_name)} ${esc(r.plan_date)}</title><style>
    @page{size:A4;margin:18mm 15mm}
    body{font-family:'Noto Sans KR','Malgun Gothic',sans-serif;color:#000;margin:0;font-size:10.5pt}
    .pg{page-break-after:always;padding-top:4mm}.pg:last-child{page-break-after:auto}
    h1{text-align:center;font-size:22pt;letter-spacing:2px;margin:6mm 0 5mm}
    table{border-collapse:collapse;width:100%}
    th,td{border:1px solid #000;padding:5px 8px;vertical-align:middle}
    th{background:#eee;font-weight:700;text-align:center}
    .sign{width:46%;margin-left:auto}.sign td{height:16mm}.sign .v{width:8%}
    .f{border:2px solid #000}.c{text-align:center}.r{text-align:right}
    .big td.txt{height:120mm;white-space:pre-wrap;vertical-align:middle;line-height:1.7}
    .note{font-size:9.5pt;line-height:1.7}
    .decl{border-top:1px solid #000;padding:10px}
    .proc{border-top:0}
    @media screen{body{background:#888}.pg{background:#fff;width:180mm;min-height:260mm;margin:10px auto;padding:12mm}}
  </style></head><body>${plan}${rep}<script>onload=()=>print()<\/script></body></html>`);
  w.document.close();
}
