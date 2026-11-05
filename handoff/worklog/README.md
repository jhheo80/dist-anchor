# 연장·휴일 근무 신청서 / 결과보고서 — 운영 통합관리 사이트에 붙이기 (Cowork 작업지시)

대상 사이트: https://dist-lifelong-schedule.pages.dev/ (평생직업교육 통합관리, Cloudflare Pages + D1)
원본 서식: `( 연장 / 휴일 ) 근무 사전신청서` + `근무 결과보고서` (앞뒤 한 장)

## 1. 하는 일

| 화면 | 동작 |
|---|---|
| **근무 신청** 탭 (로그인한 관리자·담당자) | 내 신청서 목록 (관리자는 전체) |
| **+ 사전신청서 작성** | 구분(연장/휴일)·소속·직위·예정일시·근무시간·근무계획 입력. 신청자 = 로그인 계정 이름 (서버가 넣음, 고칠 수 없음) |
| **+ 결과보고서 작성** | **결과보고서를 아직 안 낸 신청서만** 고르는 창 → 고르면 예정일시·근무계획이 실제일시·근무내용 칸에 그대로 채워짐 → 고쳐서 저장 → 그 신청서는 고르는 목록에서 빠짐 |
| 산정 실근무시간 (관리자) | 목록에서 숫자 입력 → 처리내역의 "산정 실근무시간·담당(이름)"으로 기록 |
| 인쇄 | 종이 서식과 같은 A4 모양 (1쪽 사전신청서, 결과보고서가 있으면 2쪽). 브라우저 인쇄에서 PDF 저장도 됨 |
| 엑셀(CSV) | 그 해 신청 전체 |

잠금 규칙 (서버에서 검사): 결과보고서를 낸 뒤에는 담당자가 신청서를 고치거나 지울 수 없음 / 관리자가 산정한 뒤에는 결과보고서도 고칠 수 없음 / 관리자는 언제나 고칠 수 있음 / 남의 신청서는 보이지도 않음.

## 2. 파일

| 파일 | 붙이는 곳 |
|---|---|
| `schema.sql` | 운영 D1 콘솔에서 한 번 실행 (`worklogs` 표 추가, 기존 표는 그대로) |
| `worker-worklogs.js` | 운영 `src/worker.src.js` — 아래 3-② 참고 |
| `root-worklogs.html` | 운영 `src/root.html` — 탭 버튼·section·dialog 2개·style (파일 맨 위 주석에 위치 표시) |
| `root-worklogs.js` | 운영 `src/root.html` `<script>` 끝 |
| `test-worklogs.mjs`, `fake-env.mjs` | 검사용 (배포 안 함) |
| `preview-server.mjs` | 미리보기용 (배포 안 함) |

## 3. 붙이는 순서

① **백업 먼저**: 운영 D1 내보내기 (Actions의 export 워크플로 또는 대시보드). `reset-db` 워크플로는 운영 DB에 절대 연결하지 말 것.

② **서버** (`src/worker.src.js`)
- `worker-worklogs.js` 전체를 도우미 함수들(`json`, `bad`, `body`, `str`, `isDate`, `kstToday`) 아래에 붙여 넣음.
- 관리자 로그인 확인이 끝나고 **로그인한 계정 객체**를 알게 된 직후에 한 줄:
  ```js
  const wl = await worklogRoute(req, env, me, p, m, url); if (wl) return wl;
  ```
  `me`는 `{ name, role }` (role: `admin` / `staff` / `viewer`). 운영 코드에서 이 객체를 부르는 이름이 다르면 그 이름으로 넘길 것.
  ※ 테스트 저장소(dist-lifelong-schedule-test)는 비밀번호 하나 방식이라 `me`가 없음. **계정별 로그인이 있는 운영 소스에 붙여야 함.**
- 운영에 **감사기록(`/api/admin/audit`, 되살리기)** 이 있으므로, 신청서 삭제(DELETE) 때 응답의 `deleted` 행을 기존 감사기록 함수로 남기도록 연결 (다른 삭제와 같은 방식).

③ **화면** (`src/root.html`)
- `root-worklogs.html`의 조각 4개를 표시된 위치에 붙여 넣기.
- `root-worklogs.js`를 `<script>` 끝에 붙여 넣기.
- 연결:
  ```js
  // showTab(t) 안
  for(const k of ['courses','schedule','applicants','budget','accounts','worklog']) ...   // 'worklog' 추가
  if(t==='worklog') loadWorklogs();
  // signOut() 안
  WL=[];
  ```
- 연도 선택(`#fYear`)을 바꿀 때 근무 신청 탭이 열려 있으면 `loadWorklogs()`도 부르기.
- 운영 화면의 휴대폰 카드 보기(`.mcards`) 목록 `['#tCourses','#tLedger','#cx_table']`에 `'#tWorklog'` 추가.

④ `python src/build.py` → 테스트 사이트에서 먼저 확인 → 운영 배포.

## 4. 확인 방법

```bash
node handoff/worklog/test-worklogs.mjs        # 서버 권한·잠금·시간 계산 검사 (Node 22+, 설치 없음)
node handoff/worklog/preview-server.mjs       # http://localhost:8788 — 계정을 바꿔 가며 화면 전체 흐름 확인
```

운영에 붙인 뒤 사람이 확인할 것:
1. 담당자 A로 사전신청서 작성 → 담당자 B 계정에는 안 보이는지
2. A로 "+ 결과보고서 작성" → 방금 신청서가 목록에 뜨고, 고르면 내용이 채워지는지 → 저장 후 다시 누르면 목록에서 빠지는지
3. 관리자로 산정 실근무시간 입력 → A 계정에서 결과보고서 수정 버튼이 사라지는지
4. 인쇄 → A4 2쪽, 결재란·처리내역이 서식과 같은지

## 5. 정해 둔 것 / 남은 결정

- 근무시간 기본값: 시작~끝이 9시간 이상이면 **휴게 1시간을 빼서** 제안 (서식 예: 08:30~17:30 → 8시간, 17:30~21:30 → 4시간). 칸에서 직접 고칠 수 있음. 기관 규정이 다르면 `root-worklogs.js`의 `wlHourOf`만 고치면 됨.
- 결재란(담당·실장·앵커사업단장)은 인쇄 후 수기 서명. 온라인 결재 흐름은 만들지 않음.
- 신청자는 계정 이름으로 묶음. 계정 이름을 바꾸면 `UPDATE worklogs SET user_name=새이름 WHERE user_name=옛이름`도 함께 실행.
- 서명 이미지, 알림(메일·문자), 월별 시간외 합계 화면은 넣지 않음.

---

## Cowork에 붙여 넣을 시작 문장

```
첨부한 worklog 폴더는 "연장·휴일 근무 사전신청서 + 결과보고서" 기능을
운영 평생직업교육 통합관리 사이트(dist-lifelong-schedule)에 붙이기 위한 코드 조각이야.
README.md를 끝까지 읽고 그 순서대로 해 줘.

1. 먼저 운영 소스에서 로그인한 계정 객체(me, role)를 얻는 곳, showTab, signOut, 감사기록 함수 위치를 찾아서 알려 줘.
2. 운영 D1 백업을 받은 뒤 schema.sql 실행.
3. 서버·화면 조각을 붙이고 node worklog/test-worklogs.mjs 가 통과하는지 확인.
4. 테스트 사이트에 먼저 배포해 README 4번 확인 항목 4가지를 확인한 뒤, 내가 확인하면 운영에 배포.

지켜야 할 것: 운영 DB는 바꾸기 전에 백업, reset-db 워크플로 운영 연결 금지,
권한 검사는 화면이 아니라 서버(worker)에서 — worker-worklogs.js의 검사를 지우지 말 것.
```
