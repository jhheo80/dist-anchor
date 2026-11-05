-- 연장·휴일 근무 신청서 + 결과보고서 (한 행 = 신청서 1건, 결과보고서는 같은 행에 나중에 채움)
-- 운영 D1 콘솔에서 한 번 실행. 기존 표는 건드리지 않음 (CREATE ... IF NOT EXISTS 만 있음).
CREATE TABLE IF NOT EXISTS worklogs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kind TEXT NOT NULL,                 -- '연장' | '휴일'
  user_name TEXT NOT NULL,            -- 신청자 = 로그인 계정 이름 (서버가 넣음)
  dept TEXT, position TEXT,           -- 소속 / 직위
  plan_date TEXT NOT NULL, plan_start TEXT NOT NULL, plan_end TEXT NOT NULL, plan_hours REAL NOT NULL,
  plan_text TEXT NOT NULL,            -- 근무계획
  apply_date TEXT NOT NULL,           -- 신청일
  actual_date TEXT, actual_start TEXT, actual_end TEXT, actual_hours REAL,
  report_text TEXT,                   -- 근무내용(결과)
  attach TEXT,                        -- 붙임
  report_date TEXT,                   -- 결과보고서 작성일
  reported_at TEXT,                   -- NULL이면 결과보고서 미제출 → '결과보고서 작성' 목록에 뜸
  approved_hours REAL,                -- 처리내역: 산정 실근무시간 (관리자)
  checker TEXT,                       -- 처리내역: 담당 (관리자 이름)
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS worklogs_user ON worklogs (user_name, plan_date);
CREATE INDEX IF NOT EXISTS worklogs_open ON worklogs (reported_at);
