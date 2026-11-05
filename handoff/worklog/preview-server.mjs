// 미리보기: node handoff/worklog/preview-server.mjs → http://localhost:8788
// 운영 루트 화면 대신 아주 작은 껍데기(아래 SHELL)에 근무 신청 탭만 붙여, 진짜 서버 코드(worker-worklogs.js)와 메모리 DB로 돌려 봄.
// 위쪽 '계정' 칸에서 관리자/담당자를 바꿔 가며 권한을 확인할 수 있음. 데이터는 끄면 사라짐.
import { createServer } from 'node:http';
import { readFileSync } from 'node:fs';
import { makeEnv } from './fake-env.mjs';

const dir = new URL('.', import.meta.url);
const { env, worklogRoute } = makeEnv();
const USERS = { 곽남훈: 'admin', 문은영: 'staff', 이미람: 'staff' };

// 운영 root.html에 이미 있는 것만 흉내 냄: CSS 변수, .tab/.card/.hide, $, esc, call, me, canWrite, YEAR, TODAY
const SHELL = snippet => `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>근무 신청 미리보기</title><style>
:root{--bg:#f6f4ef;--card:#fff;--ink:#1f2328;--sub:#5d646d;--line:#e3dfd6;--accent:#1f5fa8;--accent-bg:#e8f0fa;--warn:#b5481d;--ok:#2f7d5b}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 'Noto Sans KR',system-ui,sans-serif}
header{display:flex;gap:12px;align-items:center;padding:12px 16px;background:var(--card);border-bottom:1px solid var(--line);flex-wrap:wrap}
nav{display:flex;gap:4px}.tab{border:0;background:none;padding:10px 14px;min-height:44px;font:inherit;cursor:pointer}.tab.on{border-bottom:3px solid var(--accent);font-weight:700}
main{padding:16px;max-width:1100px;margin:auto}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;overflow-x:auto}
.hide{display:none!important}button,select,input,textarea{font:inherit}button{min-height:40px;padding:6px 12px;border:1px solid var(--line);border-radius:6px;background:#fff;cursor:pointer}
.primary{background:var(--accent);color:#fff;border-color:var(--accent)}.danger{color:var(--warn)}.err{color:var(--warn)}
table{border-collapse:collapse;width:100%}th,td{border-bottom:1px solid var(--line);padding:8px;text-align:left;vertical-align:top}
dialog{border:0;border-radius:12px;max-width:760px;width:calc(100% - 32px);padding:20px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.grid label{display:flex;flex-direction:column;gap:4px;font-size:14px;color:var(--sub)}.grid .full{grid-column:1/-1}.grid input,.grid select,.grid textarea{padding:8px;border:1px solid var(--line);border-radius:6px;color:var(--ink)}
.btns{display:flex;gap:8px;justify-content:flex-end;margin-top:12px}
@media(max-width:600px){.grid{grid-template-columns:1fr}}
</style></head><body>
<header><b>평생직업교육 통합관리 (미리보기)</b><nav>${snippet.tab}</nav>
<label style="margin-left:auto">계정 <select id="who">${Object.entries(USERS).map(([n, r]) => `<option value="${n}">${n} (${r})</option>`).join('')}</select></label></header>
<main>${snippet.body}</main>
<script>
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch]));
const TODAY=new Date(Date.now()+9*3600e3).toISOString().slice(0,10); let YEAR=TODAY.slice(0,4);
const USERS=${JSON.stringify(USERS)}; let me, canWrite;
async function call(url,method,body){
  const r=await fetch(url,{method,headers:{'Content-Type':'application/json','X-Preview-User':encodeURIComponent(me.name)},body:body?JSON.stringify(body):undefined});
  const j=await r.json().catch(()=>({})); if(!r.ok) throw new Error(j.error||('오류 '+r.status)); return j;
}
function setMe(n){ me={name:n,role:USERS[n]}; canWrite=me.role!=='viewer';
  document.querySelectorAll('.admin-only').forEach(e=>e.classList.toggle('hide',!canWrite)); $('#tab-worklog').classList.remove('hide');
  document.querySelector('[data-tab=worklog]').classList.add('on'); loadWorklogs(); }
</script>
<script>${readFileSync(new URL('root-worklogs.js', dir), 'utf8')}</script>
<script>$('#who').onchange=e=>setMe(e.target.value); setMe($('#who').value);</script>
</body></html>`;

function snippetParts() {
  const h = readFileSync(new URL('root-worklogs.html', dir), 'utf8');
  return { tab: h.match(/<button class="tab[^>]*>.*?<\/button>/)[0], body: h.slice(h.indexOf('<section id="tab-worklog" class')) };
}

createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  if (url.pathname.startsWith('/api/')) {
    const name = decodeURIComponent(req.headers['x-preview-user'] || '');
    const chunks = []; for await (const c of req) chunks.push(c);
    const r = await worklogRoute(new Request(url, { method: req.method, body: chunks.length ? Buffer.concat(chunks) : undefined }),
      env, USERS[name] ? { name, role: USERS[name] } : null, url.pathname, req.method, url);
    res.writeHead(r ? r.status : 404, { 'content-type': 'application/json; charset=utf-8' });
    return res.end(r ? await r.text() : '{"error":"없는 주소"}');
  }
  res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
  res.end(SHELL(snippetParts()));
}).listen(8788, () => console.log('미리보기: http://localhost:8788'));
