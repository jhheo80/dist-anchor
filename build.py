# -*- coding: utf-8 -*-
"""
동원과학기술대학교 경남 ANCHOR 사업 홍보 사이트 정적 빌드 스크립트
  실행:  python3 build.py
  결과:  index.html / about.html / projects.html / departments.html / contact.html
콘텐츠 수정은 이 파일의 데이터 영역만 고치고 다시 실행하면 됩니다.
"""
import os
import html as _h

SITE = "동원과학기술대학교 경남 ANCHOR 사업"
SLOGAN = "지역과 함께, 미래를 혁신하다"
ADDR = "50578 경상남도 양산시 명곡로 321(명곡동) 동원과학기술대학교 동원앵커사업단"
TEL = ["055-370-8335", "055-370-8530"]
FAX = "055-370-8347"

# ── 운영 프로그램 게시판이 읽어올 구글 시트 ────────────────────────
#  SHEET_ID  : 시트 주소 .../spreadsheets/d/[여기]/edit 의 가운데 문자열
#  SHEET_TAB : 아래쪽 탭 이름 (기본값 그대로 쓰면 첫 번째 탭)
# 운영 프로그램 게시판을 켜려면 아래를 True 로 바꾸고 python build.py 다시 실행
PROGRAMS_ENABLED = False
SHEET_ID = "1boslZR_F6LBKddTLS2YDQ4RtsSssfWmtWggkAHhSp_Q"
SHEET_TAB = ""

NAV = [
    ("index.html", "홈"),
    ("about.html", "사업소개"),
    ("projects.html", "세부과제"),
    ("departments.html", "참여학과"),
    ("contact.html", "문의·오시는 길"),
]
if PROGRAMS_ENABLED:
    NAV.insert(4, ("programs.html", "운영프로그램"))

# ── 아이콘 (Material Design Icons 채움형, 24x24, Apache 2.0) ─────────────────────────────
IC = {
    "rocket": '<path fill="currentColor" d="m13.16 22.19l-1.66-3.84c1.6-.58 3.07-1.35 4.43-2.27l-2.78 6.11m-7.5-9.69l-3.84-1.65l6.11-2.78a20 20 0 0 0-2.27 4.43M21.66 2.35S23.78 7.31 18.11 13c-2.2 2.17-4.58 3.5-6.73 4.34c-.74.28-1.57.1-2.12-.46l-2.13-2.13c-.56-.56-.74-1.38-.47-2.13C7.5 10.5 8.83 8.09 11 5.89C16.69.216 21.66 2.35 21.66 2.35M6.25 22H4.84l4.09-4.1c.3.21.63.36.97.45zM2 22v-1.41l4.77-4.78l1.43 1.42L3.41 22zm0-2.84v-1.41l3.65-3.65c.09.35.24.68.45.97zM16 6a2 2 0 1 0 0 4c1.11 0 2-.89 2-2a2 2 0 0 0-2-2"/>',  # mdi:rocket-launch
    "globe": '<path fill="currentColor" d="M17.9 17.39c-.26-.8-1.01-1.39-1.9-1.39h-1v-3a1 1 0 0 0-1-1H8v-2h2a1 1 0 0 0 1-1V7h2a2 2 0 0 0 2-2v-.41a7.984 7.984 0 0 1 2.9 12.8M11 19.93c-3.95-.49-7-3.85-7-7.93c0-.62.08-1.22.21-1.79L9 15v1a2 2 0 0 0 2 2m1-16A10 10 0 0 0 2 12a10 10 0 0 0 10 10a10 10 0 0 0 10-10A10 10 0 0 0 12 2"/>',  # mdi:earth
    "book": '<path fill="currentColor" d="M12 21.5c-1.35-.85-3.8-1.5-5.5-1.5c-1.65 0-3.35.3-4.75 1.05c-.1.05-.15.05-.25.05c-.25 0-.5-.25-.5-.5V6c.6-.45 1.25-.75 2-1c1.11-.35 2.33-.5 3.5-.5c1.95 0 4.05.4 5.5 1.5c1.45-1.1 3.55-1.5 5.5-1.5c1.17 0 2.39.15 3.5.5c.75.25 1.4.55 2 1v14.6c0 .25-.25.5-.5.5c-.1 0-.15 0-.25-.05c-1.4-.75-3.1-1.05-4.75-1.05c-1.7 0-4.15.65-5.5 1.5M12 8v11.5c1.35-.85 3.8-1.5 5.5-1.5c1.2 0 2.4.15 3.5.5V7c-1.1-.35-2.3-.5-3.5-.5c-1.7 0-4.15.65-5.5 1.5m1 3.5c1.11-.68 2.6-1 4.5-1c.91 0 1.76.09 2.5.28V9.23c-.87-.15-1.71-.23-2.5-.23q-2.655 0-4.5.84zm4.5.17c-1.71 0-3.21.26-4.5.79v1.69c1.11-.65 2.6-.99 4.5-.99c1.04 0 1.88.08 2.5.24v-1.5c-.87-.16-1.71-.23-2.5-.23m2.5 2.9c-.87-.16-1.71-.24-2.5-.24c-1.83 0-3.33.27-4.5.8v1.69c1.11-.66 2.6-.99 4.5-.99c1.04 0 1.88.08 2.5.24z"/>',  # mdi:book-open-variant
    "sprout": '<path fill="currentColor" d="M2 22v-2s5-2 10-2s10 2 10 2v2zm9.3-12.9c-1.2-3.9-7.3-3-7.3-3s.2 7.8 5.9 6.6C9.5 9.8 8 9 8 9c2.8 0 3 3.4 3 3.4V17h2v-4.2s0-3.9 3-4.9c0 0-2 3-2 5c7 .7 7-8.9 7-8.9s-8.9-1-9.7 5.1"/>',  # mdi:sprout
    "factory": '<path fill="currentColor" d="M4 18v2h4v-2zm0-4v2h10v-2zm6 4v2h4v-2zm6-4v2h4v-2zm0 4v2h4v-2zM2 22V8l5 4V8l5 4V8l5 4l1-10h3l1 10v10z"/>',  # mdi:factory
    "users": '<path fill="currentColor" d="M12 5.5A3.5 3.5 0 0 1 15.5 9a3.5 3.5 0 0 1-3.5 3.5A3.5 3.5 0 0 1 8.5 9A3.5 3.5 0 0 1 12 5.5M5 8c.56 0 1.08.15 1.53.42c-.15 1.43.27 2.85 1.13 3.96C7.16 13.34 6.16 14 5 14a3 3 0 0 1-3-3a3 3 0 0 1 3-3m14 0a3 3 0 0 1 3 3a3 3 0 0 1-3 3c-1.16 0-2.16-.66-2.66-1.62a5.54 5.54 0 0 0 1.13-3.96c.45-.27.97-.42 1.53-.42M5.5 18.25c0-2.07 2.91-3.75 6.5-3.75s6.5 1.68 6.5 3.75V20h-13zM0 20v-1.5c0-1.39 1.89-2.56 4.45-2.9c-.59.68-.95 1.62-.95 2.65V20zm24 0h-3.5v-1.75c0-1.03-.36-1.97-.95-2.65c2.56.34 4.45 1.51 4.45 2.9z"/>',  # mdi:account-group
    "target": '<path fill="currentColor" d="M12 2A10 10 0 0 0 2 12a10 10 0 0 0 10 10a10 10 0 0 0 10-10c0-1.16-.21-2.31-.61-3.39l-1.6 1.6c.14.59.21 1.19.21 1.79a8 8 0 0 1-8 8a8 8 0 0 1-8-8a8 8 0 0 1 8-8c.6 0 1.2.07 1.79.21L15.4 2.6C14.31 2.21 13.16 2 12 2m7 0l-4 4v1.5l-2.55 2.55C12.3 10 12.15 10 12 10a2 2 0 0 0-2 2a2 2 0 0 0 2 2a2 2 0 0 0 2-2c0-.15 0-.3-.05-.45L16.5 9H18l4-4h-3zm-7 4a6 6 0 0 0-6 6a6 6 0 0 0 6 6a6 6 0 0 0 6-6h-2a4 4 0 0 1-4 4a4 4 0 0 1-4-4a4 4 0 0 1 4-4z"/>',  # mdi:bullseye-arrow
    "network": '<path fill="currentColor" d="M9 2v6h2v3H5c-1.11 0-2 .89-2 2v3H1v6h6v-6H5v-3h6v3H9v6h6v-6h-2v-3h6v3h-2v6h6v-6h-2v-3c0-1.11-.89-2-2-2h-6V8h2V2z"/>',  # mdi:sitemap
    "graduation": '<path fill="currentColor" d="M12 3L1 9l11 6l9-4.91V17h2V9M5 13.18v4L12 21l7-3.82v-4L12 17z"/>',  # mdi:school
    "briefcase": '<path fill="currentColor" d="M10 2h4a2 2 0 0 1 2 2v2h4a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8c0-1.11.89-2 2-2h4V4c0-1.11.89-2 2-2m4 4V4h-4v2z"/>',  # mdi:briefcase
    "cpu": '<path fill="currentColor" d="M18.41 4L16 6.41v.18L18.41 9H22v2h-4.41L16 9.41V12h-1a2 2 0 0 1-2-2V7.5H9.86c-.09.37-.24.72-.44 1.05L15.18 19H20a2 2 0 0 1 2 2v1H2v-1a2 2 0 0 1 2-2h6.61l-4.69-8.5a4.006 4.006 0 0 1-3.81-3A4 4 0 0 1 5 2.63c2.13-.55 4.31.73 4.86 2.87H13V3a2 2 0 0 1 2-2h1v2.59L17.59 2H22v2zM6 4.5a2 2 0 0 0-2 2a2 2 0 0 0 2 2a2 2 0 0 0 2-2a2 2 0 0 0-2-2"/>',  # mdi:robot-industrial
    "heart": '<path fill="currentColor" d="M7.5 4A5.5 5.5 0 0 0 2 9.5c0 .5.09 1 .22 1.5H6.3l1.27-3.37c.3-.8 1.48-.88 1.86 0L11.5 13l.59-1.42c.13-.33.48-.58.91-.58h8.78c.13-.5.22-1 .22-1.5A5.5 5.5 0 0 0 16.5 4c-1.86 0-3.5.93-4.5 2.34C11 4.93 9.36 4 7.5 4M3 12.5a1 1 0 0 0-1 1a1 1 0 0 0 1 1h2.44L11 20c1 .9 1 .9 2 0l5.56-5.5H21a1 1 0 0 0 1-1a1 1 0 0 0-1-1h-7.6l-.93 2.3c-.4 1.01-1.55.87-1.92.03L8.5 9.5l-.96 2.33c-.15.38-.49.67-.94.67z"/>',  # mdi:heart-pulse
    "plane": '<path fill="currentColor" d="M20.56 3.91c.59.59.59 1.54 0 2.12l-3.89 3.89l2.12 9.19l-1.41 1.42l-3.88-7.43L9.6 17l.36 2.47l-1.07 1.06l-1.76-3.18l-3.19-1.77L5 14.5l2.5.37L11.37 11L3.94 7.09l1.42-1.41l9.19 2.12l3.89-3.89c.56-.58 1.56-.58 2.12 0"/>',  # mdi:airplane
    "wrench": '<path fill="currentColor" d="m22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9c-2-2-5-2.4-7.4-1.3L9 6L6 9L1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4"/>',  # mdi:wrench
    "flask": '<path fill="currentColor" d="M6 22a3 3 0 0 1-3-3c0-.6.18-1.16.5-1.63L9 7.81V6a1 1 0 0 1-1-1V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v1a1 1 0 0 1-1 1v1.81l5.5 9.56c.32.47.5 1.03.5 1.63a3 3 0 0 1-3 3zm-1-3a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1c0-.21-.07-.41-.18-.57l-2.29-3.96L14 17l-5.07-5.07l-3.75 6.5c-.11.16-.18.36-.18.57m8-9a1 1 0 0 0-1 1a1 1 0 0 0 1 1a1 1 0 0 0 1-1a1 1 0 0 0-1-1"/>',  # mdi:flask
    "chef": '<path fill="currentColor" d="M12.5 1.5c-1.77 0-3.33 1.17-3.83 2.87C8.14 4.13 7.58 4 7 4a4 4 0 0 0-4 4a4.01 4.01 0 0 0 3 3.87V19h13v-7.13c1.76-.46 3-2.05 3-3.87a4 4 0 0 0-4-4c-.58 0-1.14.13-1.67.37c-.5-1.7-2.06-2.87-3.83-2.87m-.5 9h1v7h-1zm-3 2h1v5H9zm6 0h1v5h-1zM6 20v1a1 1 0 0 0 1 1h11a1 1 0 0 0 1-1v-1z"/>',  # mdi:chef-hat
    "shield": '<path fill="currentColor" d="m10 17l-4-4l1.41-1.41L10 14.17l6.59-6.59L18 9m-6-8L3 5v6c0 5.55 3.84 10.74 9 12c5.16-1.26 9-6.45 9-12V5z"/>',  # mdi:shield-check
    "eye": '<path fill="currentColor" d="M3 10c-.24 0-.45.09-.59.25c-.14.15-.2.37-.17.61l.5 2.99C2.82 14.5 3.4 15 4 15h3c.64 0 1.36-.56 1.5-1.18l1.06-3.19c.04-.13.01-.32-.06-.44c-.11-.12-.28-.19-.5-.19zm4 7H4C2.38 17 .96 15.74.76 14.14l-.5-2.99C.15 10.3.39 9.5.91 8.92S2.19 8 3 8h6c.83 0 1.58.35 2.06.96c.11.15.21.31.29.49c.43-.09.87-.09 1.29 0c.08-.18.18-.34.3-.49C13.41 8.35 14.16 8 15 8h6c.81 0 1.57.34 2.09.92c.51.58.75 1.38.65 2.19l-.51 3.07C23.04 15.74 21.61 17 20 17h-3c-1.56 0-3.08-1.19-3.46-2.7l-.9-2.71c-.38-.28-.91-.28-1.29 0l-.92 2.78C10.07 15.82 8.56 17 7 17m8-7c-.22 0-.39.07-.5.19c-.08.12-.1.31-.05.51l1.01 3.05c.18.69.9 1.25 1.54 1.25h3c.59 0 1.18-.5 1.25-1.11l.51-3.07c.03-.2-.03-.42-.17-.57A.77.77 0 0 0 21 10z"/>',  # mdi:glasses
    "scissors": '<path fill="currentColor" d="m19 3l-6 6l2 2l7-7V3m-10 9.5a.5.5 0 0 1-.5-.5a.5.5 0 0 1 .5-.5a.5.5 0 0 1 .5.5a.5.5 0 0 1-.5.5M6 20a2 2 0 0 1-2-2a2 2 0 0 1 2-2a2 2 0 0 1 2 2a2 2 0 0 1-2 2M6 8a2 2 0 0 1-2-2a2 2 0 0 1 2-2a2 2 0 0 1 2 2a2 2 0 0 1-2 2m3.64-.36c.23-.5.36-1.05.36-1.64a4 4 0 0 0-4-4a4 4 0 0 0-4 4a4 4 0 0 0 4 4c.59 0 1.14-.13 1.64-.36L10 12l-2.36 2.36C7.14 14.13 6.59 14 6 14a4 4 0 0 0-4 4a4 4 0 0 0 4 4a4 4 0 0 0 4-4c0-.59-.13-1.14-.36-1.64L12 14l7 7h3v-1z"/>',  # mdi:content-cut
    "activity": '<path fill="currentColor" d="M16.5 5.5a2 2 0 0 0 2-2a2 2 0 0 0-2-2a2 2 0 0 0-2 2a2 2 0 0 0 2 2m-3.6 13.9l1-4.4l2.1 2v6h2v-7.5l-2.1-2l.6-3A7.3 7.3 0 0 0 22 13v-2c-1.76.03-3.4-.89-4.3-2.4l-1-1.6c-.36-.6-1-1-1.7-1c-.3 0-.5.1-.8.1L9 8.3V13h2V9.6l1.8-.7l-1.6 8.1l-4.9-1l-.4 2zM4 9a1 1 0 0 1-1-1a1 1 0 0 1 1-1h3v2zm1-4a1 1 0 0 1-1-1a1 1 0 0 1 1-1h5v2zm-2 8a1 1 0 0 1-1-1a1 1 0 0 1 1-1h4v2z"/>',  # mdi:run-fast
    "baby": '<path fill="currentColor" d="M1 12c0-1.81 1.2-3.34 2.86-3.83A8.97 8.97 0 0 1 12 3a9 9 0 0 1 8.15 5.17C21.8 8.66 23 10.19 23 12s-1.2 3.34-2.85 3.83A9 9 0 0 1 12 21c-3.6 0-6.71-2.11-8.14-5.17A3.99 3.99 0 0 1 1 12m13.5-2.75a1.25 1.25 0 0 0-1.25 1.25a1.25 1.25 0 0 0 1.25 1.25a1.25 1.25 0 0 0 1.25-1.25a1.25 1.25 0 0 0-1.25-1.25m-5 0a1.25 1.25 0 0 0-1.25 1.25a1.25 1.25 0 0 0 1.25 1.25a1.25 1.25 0 0 0 1.25-1.25A1.25 1.25 0 0 0 9.5 9.25M7.5 14c.76 1.77 2.5 3 4.5 3s3.74-1.23 4.5-3zM3 12c0 .82.5 1.53 1.21 1.84C4.07 13.25 4 12.63 4 12s.07-1.25.21-1.84C3.5 10.47 3 11.18 3 12m18 0c0-.82-.5-1.53-1.21-1.84c.14.59.21 1.21.21 1.84s-.07 1.25-.21 1.84C20.5 13.53 21 12.82 21 12"/>',  # mdi:baby-face
    "ship": '<path fill="currentColor" d="M6 6h12v3.96L12 8L6 9.96M3.94 19H4c1.6 0 3-.88 4-2c1 1.12 2.4 2 4 2s3-.88 4-2c1 1.12 2.4 2 4 2h.05l1.9-6.69c.08-.25.05-.53-.06-.77c-.13-.24-.34-.42-.6-.5L20 10.62V6a2 2 0 0 0-2-2h-3V1H9v3H6a2 2 0 0 0-2 2v4.62l-1.29.42c-.26.08-.47.26-.6.5c-.11.24-.14.52-.06.77M20 21c-1.39 0-2.78-.47-4-1.33c-2.44 1.71-5.56 1.71-8 0C6.78 20.53 5.39 21 4 21H2v2h2c1.37 0 2.74-.35 4-1c2.5 1.3 5.5 1.3 8 0c1.26.65 2.62 1 4 1h2v-2z"/>',  # mdi:ferry
    "snow": '<path fill="currentColor" d="m20.79 13.95l-2.33.62l-2-1.13v-2.88l2-1.13l2.33.62l.52-1.93l-1.77-.47l.46-1.77l-1.93-.52l-.62 2.33l-2 1.13L13 7.38V5.12l1.71-1.71L13.29 2L12 3.29L10.71 2L9.29 3.41L11 5.12v2.26L8.5 8.82l-2-1.13l-.58-2.33L4 5.88l.47 1.77l-1.77.47l.52 1.93l2.33-.62l2 1.13v2.89l-2 1.13l-2.33-.62l-.52 1.93l1.77.47L4 18.12l1.93.52l.62-2.33l2-1.13L11 16.62v2.26l-1.71 1.71L10.71 22L12 20.71L13.29 22l1.41-1.41l-1.7-1.71v-2.26l2.5-1.45l2 1.13l.62 2.33l1.88-.51l-.47-1.77l1.77-.47zM9.5 10.56L12 9.11l2.5 1.45v2.88L12 14.89l-2.5-1.45z"/>',  # mdi:snowflake
    "compass": '<path fill="currentColor" d="M14.19 14.19L6 18l3.81-8.19L18 6m-6-4A10 10 0 0 0 2 12a10 10 0 0 0 10 10a10 10 0 0 0 10-10A10 10 0 0 0 12 2m0 8.9a1.1 1.1 0 0 0-1.1 1.1a1.1 1.1 0 0 0 1.1 1.1a1.1 1.1 0 0 0 1.1-1.1a1.1 1.1 0 0 0-1.1-1.1"/>',  # mdi:compass
    "pin": '<path fill="currentColor" d="M12 11.5A2.5 2.5 0 0 1 9.5 9A2.5 2.5 0 0 1 12 6.5A2.5 2.5 0 0 1 14.5 9a2.5 2.5 0 0 1-2.5 2.5M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7"/>',  # mdi:map-marker
    "phone": '<path fill="currentColor" d="M6.62 10.79c1.44 2.83 3.76 5.15 6.59 6.59l2.2-2.2c.28-.28.67-.36 1.02-.25c1.12.37 2.32.57 3.57.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57c.11.35.03.74-.25 1.02z"/>',  # mdi:phone
    "printer": '<path fill="currentColor" d="M18 3H6v4h12m1 5a1 1 0 0 1-1-1a1 1 0 0 1 1-1a1 1 0 0 1 1 1a1 1 0 0 1-1 1m-3 7H8v-5h8m3-6H5a3 3 0 0 0-3 3v6h4v4h12v-4h4v-6a3 3 0 0 0-3-3"/>',  # mdi:printer
    "clock": '<path fill="currentColor" d="M12 2A10 10 0 0 0 2 12a10 10 0 0 0 10 10a10 10 0 0 0 10-10A10 10 0 0 0 12 2m4.2 14.2L11 13V7h1.5v5.2l4.5 2.7z"/>',  # mdi:clock
    "layers": '<path fill="currentColor" d="m12 16l7.36-5.73L21 9l-9-7l-9 7l1.63 1.27M12 18.54l-7.38-5.73L3 14.07l9 7l9-7l-1.63-1.27z"/>',  # mdi:layers
    "spark": '<path fill="currentColor" d="M17.5 12a1.5 1.5 0 0 1-1.5-1.5A1.5 1.5 0 0 1 17.5 9a1.5 1.5 0 0 1 1.5 1.5a1.5 1.5 0 0 1-1.5 1.5m-3-4A1.5 1.5 0 0 1 13 6.5A1.5 1.5 0 0 1 14.5 5A1.5 1.5 0 0 1 16 6.5A1.5 1.5 0 0 1 14.5 8m-5 0A1.5 1.5 0 0 1 8 6.5A1.5 1.5 0 0 1 9.5 5A1.5 1.5 0 0 1 11 6.5A1.5 1.5 0 0 1 9.5 8m-3 4A1.5 1.5 0 0 1 5 10.5A1.5 1.5 0 0 1 6.5 9A1.5 1.5 0 0 1 8 10.5A1.5 1.5 0 0 1 6.5 12M12 3a9 9 0 0 0-9 9a9 9 0 0 0 9 9a1.5 1.5 0 0 0 1.5-1.5c0-.39-.15-.74-.39-1c-.23-.27-.38-.62-.38-1a1.5 1.5 0 0 1 1.5-1.5H16a5 5 0 0 0 5-5c0-4.42-4.03-8-9-8"/>',  # mdi:palette
    "lightbulb": '<path fill="currentColor" d="M12 6a6 6 0 0 1 6 6c0 2.22-1.21 4.16-3 5.2V19a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1v-1.8c-1.79-1.04-3-2.98-3-5.2a6 6 0 0 1 6-6m2 15v1a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-1zm6-10h3v2h-3zM1 11h3v2H1zM13 1v3h-2V1zM4.92 3.5l2.13 2.14l-1.42 1.41L3.5 4.93zm12.03 2.13l2.12-2.13l1.43 1.43l-2.13 2.12z"/>',  # mdi:lightbulb-on
    "external": '<path fill="currentColor" d="M14 3v2h3.59l-9.83 9.83l1.41 1.41L19 6.41V10h2V3m-2 16H5V5h7V3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7h-2z"/>',  # mdi:open-in-new
    "handshake": '<path fill="currentColor" d="M11 6h3l3.29-3.3a1 1 0 0 1 1.42 0l2.58 2.59a1 1 0 0 1 0 1.41L19 9h-8v2a1 1 0 0 1-1 1a1 1 0 0 1-1-1V8a2 2 0 0 1 2-2m-6 5v4l-2.29 2.29a1 1 0 0 0 0 1.41l2.58 2.59a1 1 0 0 0 1.42 0L11 17h4a1 1 0 0 0 1-1v-1h1a1 1 0 0 0 1-1v-1h1a1 1 0 0 0 1-1v-1h-7v1a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2V9Z"/>',  # mdi:handshake
    "anchor": '<path fill="currentColor" d="M12 2a3 3 0 0 0-3 3a3 3 0 0 0 2 2.83V9H8v2h3v8.92c-.74-.13-1.5-.34-2.21-.65c-.74-.32-1.39-.71-1.97-1.18s-1.04-.98-1.38-1.54L7 15l-4-3v3c0 .97.27 1.88.82 2.72A8.2 8.2 0 0 0 6 19.95c.87.64 1.84 1.14 2.88 1.5c1.05.36 2.09.55 3.12.55s2.07-.2 3.12-.56c1.04-.36 2.01-.86 2.88-1.49c.92-.64 1.63-1.38 2.18-2.23c.55-.84.82-1.75.82-2.72v-3l-4 3l1.56 1.55c-.34.56-.8 1.07-1.38 1.54s-1.23.86-1.97 1.18c-.71.31-1.47.52-2.21.65V11h3V9h-3V7.82A3 3 0 0 0 15 5a3 3 0 0 0-3-3m0 2a1 1 0 0 1 1 1a1 1 0 0 1-1 1a1 1 0 0 1-1-1a1 1 0 0 1 1-1"/>',  # mdi:anchor
}


def icon(name, cls=""):
    p = IC.get(name, IC["target"])
    return ('<svg class="%s" viewBox="0 0 24 24" fill="currentColor" '
            'aria-hidden="true" focusable="false">%s</svg>') % (cls, p)


# ── 데이터: 4대 프로젝트 ────────────────────────────────────────────
PROJECTS = [
    {"no": "PROJECT 1", "cls": "p1", "icon": "factory",
     "title": "미래 제조 DNA를 심는<br>‘산업 혁신 인재’ 양성",
     "plain": "미래 제조 DNA를 심는 ‘산업 혁신 인재’ 양성",
     "desc": "G-10 지역전략산업 특성화와 산학연계 중점 대학 육성을 통해 경남 주력·신산업 현장에 바로 투입되는 기술인재를 길러냅니다.",
     "units": ["G-10 지역전략산업 특성화 대학 육성", "산학연계 중점 대학 육성"]},
    {"no": "PROJECT 2", "cls": "p2", "icon": "flask",
     "title": "세계와 지역을 잇는<br>‘글로벌 연구·정주’ 거점 구축",
     "plain": "세계와 지역을 잇는 ‘글로벌 연구·정주’ 거점 구축",
     "desc": "대학–산업체 공동 연구개발로 지역 중소기업의 산학협력 역량을 높이고 지속 성장 기반을 마련합니다.",
     "units": ["지역 연구 중심대학 육성"]},
    {"no": "PROJECT 3", "cls": "p3", "icon": "book",
     "title": "경계없는 배움터<br>‘글로벌 평생·직업’ 체계 완성",
     "plain": "경계없는 배움터 ‘글로벌 평생·직업’ 체계 완성",
     "desc": "평생교육 거점대학, 고등직업 거점대학, 외국인 유학생 지원을 통해 나이와 국경을 넘는 배움의 길을 엽니다.",
     "units": ["평생교육 거점대학 육성", "고등직업 거점 대학육성(전문대형)", "외국인 유학생 유치지원"]},
    {"no": "PROJECT 4", "cls": "p4", "icon": "sprout",
     "title": "지역 활력을 높이는<br>‘정주·창업 밸류’ 창출",
     "plain": "지역 활력을 높이는 ‘정주·창업 밸류’ 창출",
     "desc": "창업교육 거점대학과 리빙랩 선도대학 육성으로 지역 문제를 함께 풀고 정주형 창업 생태계를 만듭니다.",
     "units": ["창업교육 거점 대학육성", "지역문제 해결 리빙랩 선도대학 육성"]},
]

# ── 데이터: 14개 세부과제 ───────────────────────────────────────────
TASKS = [
    ("1-➊-③", "p1", "우주항공산업 육성", "항공기 부품제작·정비 융합 산업기능인력양성(MRO)",
     ["항공기 부품제작·정비 전문인력 양성을 통한 지역 인재 정주로 경남 항공산업 경쟁력 강화",
      "항공기 MRO 고급인력, 항공기 부품 제작인력, 품질생산 관리인력 양성"],
     ["항공기 부품제작 분야: 제조 ICT 기반 스마트 전문 기술자 양성",
      "항공기 시스템 정비 분야: 고부가가치 융합기술자 양성"]),
    ("1-➊-④", "p1", "소재·부품산업 육성", "기계부품 설계 및 생산기능인력 양성",
     ["기계부품분야 설계 및 생산기능인력양성 거점 대학으로 성장"],
     ["기계부품분야 전문설계인력 양성", "소재부품분야 용접 전문 생산기능인력 양성"]),
    ("1-➊-⑤", "p1", "바이오 산업 육성", "AI기반 바이오 헬스케어 서비스 인력양성 NAVI Project",
     ["AI기반 지산학 협력을 통한 바이오 헬스케어 서비스 인력 양성"],
     ["디지털 항공 응급의료 전문 인력 양성", "AI 기반 휴먼 케어 인력 양성"]),
    ("1-➊-⑨", "p1", "미래차·로봇 산업기술 육성", "로봇SI 분야 고숙련 전문기술인력 양성",
     ["첨단 신산업 집중육성을 위한 경남 맞춤형 로봇SI 분야 특화 및 경쟁력 강화",
      "지역산업체 수요반영 및 기업연계형 첨단 로봇 전문기술인력 양성"],
     ["로봇 설계/제조, 로봇 제어/운용, 로봇시스템 유지보수 인력 양성",
      "로봇SI 분야 핵심기술을 가진 고숙련 전문기술인력 양성"]),
    ("1-➊-⑩", "p1", "지역산업(농수산·관광문화·물류 등) 육성", "저온물류 시스템 운영 및 유지관리 산업기능인력 양성",
     ["현장실무 능력을 겸비한 저온물류 전문인력을 양성하여 지역 정주로 경남 저온 물류산업 경쟁력 강화",
      "저온물류 시스템 관리자, 저온물류 유지관리 관리자 및 저온 물류 산업기능인력 양성"],
     ["냉동특화분야: 콜드체인 관리자, 저온물류 시스템 운영 관리자, 냉동기 설치·유지보수 산업기능인력 양성",
      "공조특화분야: 공조냉동 기계 관리자 및 공조·저온물류 시스템 운영관리 산업기능 인력 양성"]),
    ("1-➊-⑩-1", "p1", "신산업 특화(스마트팜) 사업", "신산업분야 특화선도전문대학 지원사업 2.0 환경분야(스마트팜)",
     ["국가주도 신산업 분야인 환경분야에서 스마트팜의 시설 및 기계분야 전문기술인력 양성",
      "전문대학–폴리텍 간 연계·협력 및 산학연 협업 기반 스마트팜 융합전공 공동 운영체계 구축"],
     ["스마트팜 냉동공조·시설 유지관리 분야", "스마트팜 시설제조 전문인력 및 제어분야 전문인력 양성"]),
    ("1-➋-①", "p1", "대학의 산학친화적 프로그램 운영", "산업체 트윈 타워대학",
     ["지역 중소기업 성장을 지원할 수 있는 친화적 협력체계 구축",
      "지역 중소기업 성장지원을 위한 프로그램 운영",
      "지역 산업체 성장지원을 위한 필드 서비스 인재 양성",
      "지역 산업체 DX 전환 필수 인재 양성"],
     ["이공계 분야: 산업체 요구 수요 반영 현장 친화형 인력",
      "비이공계 분야: AI·DX 융합 디지털 인재 양성"]),
    ("1-➋-②", "p1", "취업역량 강화 프로그램", "현장형 실무인재 지역정주 취업프로그램",
     ["인성·성실성·의사소통능력 및 실무형 현장기술을 갖춘 경남형 우수인재 육성",
      "맞춤형 인재양성에 의한 경남지역 산업체 인력 부족 해소 기여"],
     ["지역산업 맞춤형 취업교육 프로그램", "경남 지역정주취업 지원프로그램"]),
    ("2-①", "p2", "지역 연구 중심대학 육성", "지역 중소기업 산학협력 역량 강화",
     ["대학–산업체 공동 연구개발을 통한 중소기업 산학협력 역량 강화와 지속 성장 가능성 확보",
      "신산업분야 필수 인력 양성과 우수 연구지원 체계 마련"],
     ["경남 주력 산업 분야: 항공우주, 기계, 자동차, 조선, 물류 등",
      "미래 신산업 분야: AI, DX, ICT, 바이오 등"]),
    ("3-①", "p3", "경남형 평생교육 공동교육과정 체계 운영", "경남 라이프 공유대학 평생교육 공동교육과정 운영",
     ["지역 사회와 평생교육 네트워크 구축 및 교육 자원 공유·협력 체계 강화",
      "고용 유지 및 전환 지원을 위해 새로운 직무 또는 산업에 적응할 수 있는 재교육 지원"],
     ["성인학습자 창업 희망 분야: 외식 조리, 디저트 카페 분야",
      "재직자 직무 향상 교육 희망 분야: 조리직, 디지털 융합 교육"]),
    ("3-②", "p3", "산업기능인력양성(전문대–시군)", "성인 친화적 산업기능 인력양성 체계 고도화",
     ["지역의 성인 재취업 및 창업 활동 등의 상시 관리지원을 바탕으로, 교육과정 수혜를 통해 양성된 지역 맞춤 성인 학습 인재의 재취업과 창업 활동을 통한 지역사회 정주 여건 향상 도모",
      "동원과학기술대학교–양산시 상생협력 기반 고등직업교육 거점화를 위한 지역의 성인친화적 산업기능 인력양성 및 지역발전 생태계 조성"],
     ["융합안전 특화: 다양한 산업현장의 안전 지킴이 인재 양성",
      "보건·복지 특화: 지역사회 노인/장애인 케어 및 상담 전문인재 양성"]),
    ("3-③", "p3", "외국인 유학생 유치·지역정주 원스톱 지원", "외국인 유학생 유치–교육–취업–정주 프로그램 GREES",
     ["경남지역 외국인 유학생 유치 확대와 지역 정주 및 산업인력 선순환 체계 구축을 위한 교육",
      "언어소통 문제, 문화적 차이 등을 고려한 유학생 정주 여건 향상 원스톱 시스템 구축"],
     ["돌봄(요양)서비스, 뿌리산업(용접) 전문 인력 양성",
      "지역수요 맞춤형 인재양성 체계 구축 및 지원",
      "지역 정주 유학생 유치 해외기반 구축 및 확대"]),
    ("4-①", "p4", "창업교육 거점 대학 육성", "G-East 창업교육 거점 대학 육성",
     ["맞춤형 창업교육 및 실용창업 지원에 의한 창업지원체계 고도화",
      "지역산업 기반의 혁신 창업 모델 발굴 및 지역 창업허브 구축"],
     ["실용창업을 위한 맞춤형 창업교육 프로그램", "경남 지역정주창업 지원프로그램"]),
    ("4-②", "p4", "시군 연계형 지역문제 해결사업", "50만 미래 양산을 위한 YS-Live 프로젝트",
     ["지역 산업체 재직 청년, 외국인 및 지역민의 지속적인 정주 여건 개선을 통한 미래 도시 양산 지역정주 인구 50만 달성"],
     ["지역산업체 재직 청년, 외국인 지역민의 지속적인 정주 여건 개선 및 활동 지원"]),
]

# ── 데이터: 참여 학과 ───────────────────────────────────────────────
DEPTS = [
    ("간호학과", "4년제", "heart", "https://nurse.dist.ac.kr/"),
    ("호텔식품제과제빵과", "", "chef", "https://baker.dist.ac.kr/"),
    ("AI기계제어과", "", "cpu", "https://aim.dist.ac.kr/aim/Main.do"),
    ("헤어디자인과", "", "scissors", "https://hair.dist.ac.kr/"),
    ("안경광학과", "3년제", "eye", "https://glass.dist.ac.kr/glass/Main.do"),
    ("메카트로닉스과", "", "wrench", "https://mct.dist.ac.kr/mct/Main.do"),
    ("선박동력기계과", "", "ship", "https://sm.dist.ac.kr/sm/Main.do"),
    ("생활문화예술과", "", "spark", "https://lca.dist.ac.kr/"),
    ("보건의료행정과", "", "briefcase", "https://sh.dist.ac.kr/"),
    ("산업안전관리과", "", "shield", "https://insafety.dist.ac.kr/"),
    ("스포츠재활운동과", "", "activity", "https://rp.dist.ac.kr/rp/CMS/Contents/Contents.do?mCode=MN053"),
    ("사회복지과", "주간/야간", "users", "https://sc.dist.ac.kr/"),
    ("디저트카페창업과", "", "chef", "https://dcf.dist.ac.kr/"),
    ("항공정비과", "3년제", "plane", "https://sky.dist.ac.kr/"),
    ("전문스포츠지도과", "", "activity", "https://rp.dist.ac.kr/rp/CMS/Contents/Contents.do?mCode=MN065"),
    ("보건복지과", "", "heart", "https://sc.dist.ac.kr/"),
    ("글로벌외식조리과", "", "chef", "https://hf.dist.ac.kr/"),
    ("항공기계과", "", "plane", "https://sky.dist.ac.kr/sky/CMS/Contents/Contents.do?mCode=MN064"),
    ("파크골프건강지도과", "신설", "activity", "https://pgh.dist.ac.kr/pgh/Main.do"),
    ("유아교육과", "3년제", "baby", "https://kids.dist.ac.kr/"),
    ("AI푸드창업과", "", "cpu", "https://wca.dist.ac.kr/wca/Main.do"),
    ("냉동공조설비과", "", "snow", "https://refrig.dist.ac.kr/"),
    ("자율전공학부", "", "compass", "https://dis.dist.ac.kr/dis/Main.do"),
]

# ── 데이터: 추진 방향 / 인재상 / 로드맵 / 협의체 ───────────────────
DIRECTIONS = [
    ("target", "담대한 대학혁신을 통한 지역 사회 수요 기반의 대학교육 실현"),
    ("network", "대학–지자체–기업 간 연계성 강화를 통한 거버넌스 활동 실천"),
    ("factory", "기업 현장을 이용한 OJT(현장실습, 인턴십 등) 교육운영 강화"),
    ("graduation", "ANCHOR 체계를 통한 생애 주기 맞춤 지역인재 양성 프로세스 운영"),
]

DIRECTION_TITLES = ["지역 수요 기반 대학교육", "대학·지자체·기업 거버넌스", "기업 현장 OJT 교육", "생애주기 맞춤 인재양성"]

# 홈 히어로의 해도(海圖) 등심선 — 안쪽부터 바깥쪽 순서
CHART_RINGS = [
    "M400 330c38 0 70 26 70 68s-30 74-72 74-68-30-68-70 32-72 70-72z",
    "M402 270c76 0 128 50 130 124 2 80-56 138-132 138-74 0-130-54-130-132 0-76 56-130 132-130z",
    "M396 208c112 2 196 76 196 190 0 116-84 196-196 196-110 0-192-82-192-194 0-112 84-194 192-192z",
    "M404 146c150 0 254 104 252 250-2 152-110 260-256 258-146-2-252-110-250-256 2-148 106-252 254-252z",
    "M398 84c186 2 318 132 316 314-2 186-134 318-318 316-182-2-312-134-310-318 2-180 132-314 312-312z",
    "M402 24c222 0 380 160 376 376-4 220-160 378-380 376-216-2-374-160-372-378 2-214 160-374 376-374z",
    "M400-36c258 0 440 186 436 436-4 254-186 440-440 436-250-4-436-188-432-440 4-248 188-432 436-432z",
    "M396-96c294 2 500 214 496 496-4 290-212 498-500 496-284-2-494-214-490-500 4-284 212-494 494-492z",
]

TALENTS = [
    "현장실무 전문성과 창의적 사고를 갖추고 지역 혁신을 창출하는 인재",
    "DX 리터러시와 ICT 활용 능력을 갖춘 인재",
    "글로컬한 시야와 발상으로 지역 지속가능발전에 기여하며, 다양한 전문 분야에서 지역과제에 도전하는 인재",
]

ROADMAP = [
    ("1차년", "역량 결집을 위한 동원 ANCHOR 체계 구축"),
    ("2차년", "지역연계 주문식 인력 양성 융합과정 운영"),
    ("3차년", "기업연계 산학교육 실용화 및 취업 극대화"),
    ("4차년", "지역대학 연계 공유협업 체계 구축"),
    ("5차년", "대학혁신을 통한 지역사회 발전 선도"),
]

COUNCIL = [
    ("지역 혁신기관 R&BD 협의회",
     ["지진방재 연구센터", "KITECH 생산기술센터", "KTC 경남사업센터", "KOMERI 양산본부",
      "KTR 양산지원", "경남TP 자동차로봇센터", "양산시 상공회의소", "양산시 산업혁신과"]),
    ("지역산업협의회",
     ["양산어곡단지 협의회", "(사)웅상경제인 연합회", "양산 일반 산업단지협의회", "양산유산공단 산업단지협의회",
      "양산 석계일반 산업단지협의회", "동부권 산업발전협의회", "양산가산 일반산업단지", "산막일반 산업단지"]),
    ("지역 사회·복지 협의체",
     ["양산 여성새일센터", "양산 노인 일자리 창출지원센터", "양산시 가족센터", "양산시 청년센터",
      "양산시 장애인복지관", "양산시 외국인 노동자의집", "양산 장애인 복지관", "양산직업전문학교"]),
]

STATS = [
    ("14", "세부과제"), ("4", "대 추진 프로젝트"),
    ("23", "개 참여 학과"), ("5", "개년 추진 로드맵"),
]


# ── 템플릿 ────────────────────────────────────────────────────────
def head(title, desc, page):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{_h.escape(title)} | {SITE}</title>
<meta name="description" content="{_h.escape(desc)}">
<meta name="author" content="동원과학기술대학교 동원앵커사업단">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{_h.escape(title)} | {SITE}">
<meta property="og:description" content="{_h.escape(desc)}">
<meta property="og:locale" content="ko_KR">
<meta name="theme-color" content="#0A2A66">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip" href="#main">본문 바로가기</a>
{header(page)}
<main id="main">
"""


def header(page):
    links = "".join(
        '<li><a class="nav__link" href="%s"%s>%s</a></li>'
        % (href, ' aria-current="page"' if href == page else "", label)
        for href, label in NAV
    )
    return f"""<header class="hd">
  <div class="wrap hd__in">
    <a class="brand" href="index.html">
      <span class="brand__mark" aria-hidden="true">
        <svg width="34" height="34" viewBox="0 0 40 40" fill="none">
          <rect width="40" height="40" rx="11" fill="#1D5BD8"/>
          <path d="M20 9v22M20 31c-4.5 0-8-3.2-8-7M20 31c4.5 0 8-3.2 8-7" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>
          <circle cx="20" cy="13" r="3.4" stroke="#fff" stroke-width="2.6"/>
          <path d="M14 17h12" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>
        </svg>
      </span>
      <span class="brand__txt">
        <span class="brand__uni">동원과학기술대학교</span>
        <span class="brand__name">경남 ANCHOR 사업</span>
      </span>
    </a>
    <button class="navtoggle" type="button" aria-expanded="false" aria-controls="gnb" aria-label="메뉴 열기">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
    <nav class="nav" id="gnb" aria-label="주요 메뉴">
      <ul class="nav__list">{links}</ul>
    </nav>
  </div>
</header>"""


def footer():
    links = "".join('<a href="%s">%s</a>' % (h_, l) for h_, l in NAV)
    tel = " / ".join('<a href="tel:%s">%s</a>' % (t.replace("-", ""), t) for t in TEL)
    return f"""</main>
<footer class="ft">
  <div class="wrap">
    <div class="ft__top">
      <div>
        <p class="ft__name">동원과학기술대학교 동원앵커사업단</p>
        <p>{ADDR}</p>
        <p>Tel. {tel} &nbsp;|&nbsp; Fax. {FAX}</p>
      </div>
      <nav class="ft__links" aria-label="푸터 메뉴">{links}</nav>
    </div>
    <p class="ft__bot">&copy; <span id="year">2026</span> Dongwon Institute of Science and Technology. 경상남도 ANCHOR 사업 &mdash; ‘{SLOGAN}’</p>
    <p class="ft__bot">Icons: <a href="https://pictogrammers.com/library/mdi/">Material Design Icons</a> (Apache License 2.0)</p>
  </div>
</footer>
<script src="assets/js/main.js"></script>
</body>
</html>
"""


def phead(crumb, title, desc):
    return f"""<section class="phead">
  <div class="wrap">
    <p class="crumb">{crumb}</p>
    <h1>{title}</h1>
    <p>{desc}</p>
  </div>
</section>"""


def shead(kicker, title, desc=""):
    d = "<p>%s</p>" % desc if desc else ""
    return f'<div class="shead rv"><h2>{title}</h2>{d}</div>'


# ── 페이지: 홈 ────────────────────────────────────────────────────
def page_index():
    facts = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % s_ for s_ in STATS)
    dirs = "".join(f"""
      <li class="rv"><span class="dir__ic">{icon(ic)}</span>
        <div><h3>{t}</h3><p>{txt}</p></div></li>""" for ic, t, txt in
        [(ic, h_, txt) for (ic, txt), h_ in zip(DIRECTIONS, DIRECTION_TITLES)])
    tiles = "".join(f"""
      <a class="tile rv {p['cls']}" href="projects.html#{p['cls']}">
        <span class="tile__name">{p['no'].replace('PROJECT ', '프로젝트 ')}</span>
        <h3>{p['title']}</h3>
        <p>{p['desc']}</p>
        <span class="tile__more">세부과제 보기</span>
        {icon(p['icon'], 'tile__glyph')}
      </a>""" for p in PROJECTS)
    road = "".join('<li class="rv"><b>%s</b><p>%s</p></li>' % r for r in ROADMAP)
    rings = "".join('<path d="%s"/>' % d for d in CHART_RINGS)

    return head("홈", f"{SITE} — {SLOGAN}. 지역맞춤형 혁신과 발전을 선도하는 유니컬라이제이션 인재양성.", "index.html") + f"""
<section class="hero">
  <svg class="hero__chart" viewBox="0 0 800 800" aria-hidden="true">{rings}<circle class="hero__pin" cx="400" cy="400" r="9"/></svg>
  <div class="wrap hero__in">
    <p class="hero__where">경상남도 지역혁신중심 대학지원체계, 14개 과제 선정</p>
    <h1>지역과 함께,<br>미래를 혁신하다</h1>
    <p class="hero__lead">동원과학기술대학교 경남앵커사업(ANCHOR)은 지역맞춤형 혁신과 발전을 선도하는
      <b>유니컬라이제이션(Unification&nbsp;+&nbsp;Localization)</b> 인재를 양성합니다.</p>
    <div class="hero__cta">
      <a class="btn btn--light" href="projects.html">14개 세부과제 보기</a>
      <a class="btn btn--ghost" href="about.html">사업 소개</a>
    </div>
    <dl class="facts">{facts}</dl>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("", "네 갈래의 추진 계획", "대학혁신, 거버넌스, 현장교육, 생애주기 인재양성으로 지역과 대학이 함께 성장합니다.")}
    <ul class="dir">{dirs}</ul>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {shead("", "4대 프로젝트", "산업 혁신 인재부터 정주·창업 밸류 창출까지, 지역이 필요로 하는 네 가지 축으로 사업을 추진합니다.")}
    <div class="tiles">{tiles}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("", "5개년 추진 방향", "체계를 세우는 1차년부터 지역사회 발전을 이끄는 5차년까지 단계적으로 나아갑니다.")}
    <ol class="road">{road}</ol>
  </div>
</section>

<section class="section section--flush">
  <div class="wrap">
    <div class="cta rv">
      <div>
        <h2>함께 만드는 지역의 미래</h2>
        <p>참여 학과, 프로그램 참여, 산학협력 문의를 환영합니다. 동원앵커사업단이 안내해 드립니다.</p>
      </div>
      <a class="btn btn--light" href="contact.html">문의하기</a>
    </div>
  </div>
</section>
""" + footer()


# ── 페이지: 사업소개 ───────────────────────────────────────────────
def page_about():
    dirs = "".join(f"""
      <div class="card rv"><span class="icon-badge">{icon(ic)}</span>
      <p style="color:var(--ink);font-weight:600;font-size:.98rem">{txt}</p></div>""" for ic, txt in DIRECTIONS)
    talents = "".join("<li>%s</li>" % t for t in TALENTS)
    road = "".join('<li class="rv"><b>%s</b><p>%s</p></li>' % r for r in ROADMAP)
    council = "".join(f"""
      <div class="taggroup rv"><h3>{name}</h3>
        <ul class="tags">{''.join('<li class="tag">%s</li>' % o for o in orgs)}</ul>
      </div>""" for name, orgs in COUNCIL)

    return head("사업소개", "경남 ANCHOR 사업의 비전, 추진계획, 인재상, 5개년 로드맵과 지역협의체를 소개합니다.", "about.html") + \
        phead("사업소개", "지역맞춤형 혁신과 발전을 선도하는<br>유니컬라이제이션 인재양성",
              "Unification + Localization — 대학·지자체·기업이 하나의 체계로 움직여 지역에 뿌리내리는 인재를 길러냅니다.") + f"""
<section class="section">
  <div class="wrap">
    {shead("VISION", "왜 ANCHOR 인가")}
    <div class="grid grid--3">
      <div class="card rv"><span class="icon-badge">{icon('network')}</span><h3>지역 정착의 닻</h3>
        <p>배움과 일자리, 정주가 한 지역 안에서 이어지도록 대학이 중심 고리 역할을 합니다.</p></div>
      <div class="card rv"><span class="icon-badge">{icon('handshake')}</span><h3>대학–지자체–기업</h3>
        <p>경상남도, 양산시, 지역 산업체와 협약 기반 거버넌스를 구성해 함께 설계하고 함께 실행합니다.</p></div>
      <div class="card rv"><span class="icon-badge">{icon('graduation')}</span><h3>생애주기 교육</h3>
        <p>초·중교부터 고등학교, 성인 학습자와 외국인 유학생까지 전 생애 맞춤 교육 프로세스를 운영합니다.</p></div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {shead("PROMOTION DIRECTION", "추진계획")}
    <div class="grid grid--4">{dirs}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("TALENT", "동원 ANCHOR사업 육성 인재상")}
    <ol class="nlist rv" style="max-width:78ch">{talents}</ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("ROADMAP", "5개년 추진 방향", "체계를 세우는 1차년부터 지역사회 발전을 이끄는 5차년까지 단계적으로 나아갑니다.")}
    <ol class="road">{road}</ol>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {shead("GOVERNANCE", "앵커(ANCHOR)사업협력 지역협의체", "지역 혁신기관, 산업단지, 사회·복지 기관이 참여하는 협력 네트워크를 운영합니다.")}
    <div class="grid grid--3">{council}</div>
  </div>
</section>
""" + footer()


# ── 페이지: 세부과제 ───────────────────────────────────────────────
def page_projects():
    chips = ['<button class="chip" type="button" data-filter="all" aria-pressed="true">전체 14개</button>']
    for p in PROJECTS:
        chips.append('<button class="chip" type="button" data-filter="%s" aria-pressed="false">%s</button>'
                     % (p["cls"], p["no"].replace("PROJECT ", "프로젝트 ")))
    chips = "".join(chips)

    overview = "".join(f"""
      <div class="card pcard {p['cls']} rv" id="{p['cls']}">
        <span class="icon-badge">{icon(p['icon'])}</span>
        <span class="pcard__no">{p['no'].replace('PROJECT ', '프로젝트 ')}</span>
        <h3>{p['title']}</h3>
        <p>{p['desc']}</p>
        <ul class="tags" style="margin-top:14px">{''.join('<li class="tag">%s</li>' % u for u in p['units'])}</ul>
      </div>""" for p in PROJECTS)

    items = []
    for i, (code, cls, unit, title, purpose, focus) in enumerate(TASKS):
        pid = "task-%d" % i
        items.append(f"""
      <li class="task {cls}" data-group="{cls}">
        <h3 style="margin:0">
          <button class="task__btn" type="button" aria-expanded="false" aria-controls="{pid}">
            <span class="task__code">{code}</span>
            <span class="task__ttl"><b>{title}</b><span>{unit}</span></span>
            <svg class="task__chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>
          </button>
        </h3>
        <div class="task__panel" id="{pid}" hidden>
          <div class="task__block"><span class="task__label">운영목적</span>
            <ul>{''.join('<li>%s</li>' % x for x in purpose)}</ul></div>
          <div class="task__block"><span class="task__label">특화분야</span>
            <ul>{''.join('<li>%s</li>' % x for x in focus)}</ul></div>
        </div>
      </li>""")
    items = "".join(items)

    return head("세부과제", "경남 ANCHOR 사업 4대 프로젝트와 14개 세부과제의 운영목적·특화분야를 안내합니다.", "projects.html") + \
        phead("세부과제", "4대 프로젝트 · 14개 세부과제",
              "각 과제를 눌러 운영목적과 특화분야를 확인하세요.") + f"""
<section class="section">
  <div class="wrap">
    {shead("OVERVIEW", "프로젝트별 사업현황")}
    <div class="grid grid--2">{overview}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {shead("DETAIL", "단위·세부과제 상세")}
    <div class="chips" role="group" aria-label="프로젝트별 보기">{chips}</div>
    <p id="filter-status" class="sr" role="status" aria-live="polite" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap"></p>
    <ul>{items}</ul>
  </div>
</section>
""" + footer()


# ── 페이지: 참여학과 ───────────────────────────────────────────────
def page_departments():
    cards = "".join(f"""
      <li class="rv"><a class="dept" href="{url}" target="_blank" rel="noopener noreferrer">
        <span class="dept__ic">{icon(ic)}</span>
        <span class="dept__body"><span class="dept__n">{name}</span>{'<span class="dept__m">%s</span>' % meta if meta else ''}</span>
        <span class="dept__go" aria-hidden="true">{icon('external')}</span>
        <span class="sr-only">학과 홈페이지 (새 창에서 열림)</span>
      </a></li>""" for name, meta, ic, url in DEPTS)

    return head("참여학과", "2026학년도 경남 ANCHOR 사업에 참여하는 동원과학기술대학교 23개 학과를 소개합니다.", "departments.html") + \
        phead("참여학과", "ANCHOR 사업 참여 학과 소개",
              "항공·기계·바이오·보건복지·조리·창업까지, 지역 산업 수요에 맞춘 23개 학과가 함께합니다.") + f"""
<section class="section">
  <div class="wrap">
    {shead("DEPARTMENTS", "참여 학과 23개", "학과 이름을 누르면 해당 학과 홈페이지가 새 창으로 열립니다. 모집 요강과 교육과정을 바로 확인하실 수 있습니다.")}
    <ul class="grid grid--4">{cards}</ul>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {shead("PATHWAY", "산업기술인력 양성 경로", "생애주기에 맞춰 초·중교부터 고등학교, 성인 학습자까지 이어지는 분야별 인력양성 체계를 운영합니다.")}
    <div class="grid grid--4">
      <div class="card rv"><span class="icon-badge">{icon('plane')}</span><h3>항공 분야</h3><p>제조 인력 · 정비 융합 기술인재</p></div>
      <div class="card rv"><span class="icon-badge">{icon('cpu')}</span><h3>로봇SI 분야</h3><p>설계·제어·유지보수 고숙련 기술인력</p></div>
      <div class="card rv"><span class="icon-badge">{icon('snow')}</span><h3>저온물류 분야</h3><p>콜드체인 운영·유지관리 기술인력</p></div>
      <div class="card rv"><span class="icon-badge">{icon('wrench')}</span><h3>부품설계·생산</h3><p>기계부품 설계 및 용접 생산기능인력</p></div>
      <div class="card rv"><span class="icon-badge">{icon('heart')}</span><h3>바이오헬스케어</h3><p>AI 기반 휴먼케어·응급의료 서비스인력</p></div>
      <div class="card rv"><span class="icon-badge">{icon('sprout')}</span><h3>스마트팜</h3><p>시설제조·제어분야 전문 기술인력</p></div>
      <div class="card rv"><span class="icon-badge">{icon('layers')}</span><h3>디지털 융합</h3><p>DX 리터러시 기반 융합인력 양성</p></div>
      <div class="card rv"><span class="icon-badge">{icon('lightbulb')}</span><h3>창업</h3><p>실용창업·지역정주창업 지원 프로그램</p></div>
    </div>
  </div>
</section>
""" + footer()


# ── 페이지: 문의 ──────────────────────────────────────────────────
def page_contact():
    tel = " / ".join('<a href="tel:%s">%s</a>' % (t.replace("-", ""), t) for t in TEL)
    return head("문의·오시는 길", "동원과학기술대학교 동원앵커사업단 연락처와 찾아오시는 길을 안내합니다.", "contact.html") + \
        phead("문의", "동원앵커사업단에 문의하세요",
              "사업 참여, 프로그램 신청, 산학협력 제안 등 무엇이든 편하게 연락 주세요.") + f"""
<section class="section">
  <div class="wrap">
    <div class="grid grid--2">
      <div class="card rv">
        <span class="icon-badge">{icon('phone')}</span>
        <h3>연락처</h3>
        <div class="info">
          <div class="info__row"><span class="info__k">전화</span><span class="info__v">{tel}</span></div>
          <div class="info__row"><span class="info__k">팩스</span><span class="info__v">{FAX}</span></div>
          <div class="info__row"><span class="info__k">운영시간</span><span class="info__v">평일 09:00 – 18:00<br><span style="color:var(--ink-3);font-size:.9rem">점심시간 12:00 – 13:00 / 주말·공휴일 휴무</span></span></div>
        </div>
      </div>
      <div class="card rv">
        <span class="icon-badge">{icon('pin')}</span>
        <h3>오시는 길</h3>
        <div class="info">
          <div class="info__row"><span class="info__k">주소</span><span class="info__v">{ADDR}</span></div>
          <div class="info__row"><span class="info__k">지도</span><span class="info__v"><a href="https://map.naver.com/p/search/동원과학기술대학교" target="_blank" rel="noopener">네이버 지도에서 보기</a></span></div>
          <div class="info__row"><span class="info__k">대학</span><span class="info__v"><a href="https://www.dist.ac.kr" target="_blank" rel="noopener">동원과학기술대학교 홈페이지</a></span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {shead("GUIDE", "이런 문의를 도와드립니다")}
    <div class="grid grid--3">
      <div class="card rv"><span class="icon-badge">{icon('graduation')}</span><h3>교육과정 참여</h3><p>재학생·성인학습자·재직자 대상 교육 프로그램 참여 방법을 안내합니다.</p></div>
      <div class="card rv"><span class="icon-badge">{icon('handshake')}</span><h3>산학협력·기업</h3><p>공동 연구개발, 현장실습·인턴십, 채용 연계 협력을 논의합니다.</p></div>
      <div class="card rv"><span class="icon-badge">{icon('globe')}</span><h3>유학생·지역정주</h3><p>외국인 유학생 유치와 지역 정주 원스톱 지원(GREES)을 안내합니다.</p></div>
    </div>
  </div>
</section>
""" + footer()


# ── 페이지: 운영 프로그램 ──────────────────────────────────────────
def page_programs():
    return head("운영 프로그램",
                "경남 ANCHOR 사업이 운영하는 교육·창업·산학협력 프로그램 소식을 사진과 함께 전합니다.",
                "programs.html") + \
        phead("운영 프로그램", "프로그램 소식",
              "사업단이 운영 중인 교육과 행사, 현장 이야기를 사진과 함께 전해 드립니다.") + f"""
<section class="section">
  <div class="wrap">
    {shead("PROGRAMS", "프로그램 갤러리", "카드를 누르면 자세한 내용을 볼 수 있습니다.")}
    <div class="chips" id="gal-chips" role="group" aria-label="분류별 보기"></div>
    <p id="gal-live" role="status" aria-live="polite" class="sr-only"></p>
    <div id="gal" class="gal"></div>
  </div>
</section>

<div class="pgm" id="pgm" role="dialog" aria-modal="true" aria-labelledby="pgm-t" hidden>
  <div class="pgm__bd"></div>
  <div class="pgm__box">
    <button class="pgm__x" id="pgm-x" type="button" aria-label="닫기">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>
    </button>
    <img class="pgm__img" id="pgm-img" src="" alt="">
    <div class="pgm__in">
      <div class="pgm__meta" id="pgm-meta"></div>
      <h2 id="pgm-t"></h2>
      <p id="pgm-s"></p>
      <a class="btn btn--solid" id="pgm-link" href="#" target="_blank" rel="noopener noreferrer" hidden>자세히 보기</a>
    </div>
  </div>
</div>

<script>window.PROGRAM_SHEET = {{ id: "{SHEET_ID}", sheet: "{SHEET_TAB}" }};</script>
<script src="assets/js/programs.js"></script>
""" + footer()


PAGES = {
    "index.html": page_index,
    "about.html": page_about,
    "projects.html": page_projects,
    "departments.html": page_departments,
    "contact.html": page_contact,
}

if PROGRAMS_ENABLED:
    PAGES["programs.html"] = page_programs


if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(root, "assets", "img"), exist_ok=True)
    fav = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">
<rect width="40" height="40" rx="9" fill="#0A2A66"/>
<g transform="translate(7 7) scale(1.0833)"><path fill="#FFFFFF" d="M12 2a3 3 0 0 0-3 3a3 3 0 0 0 2 2.83V9H8v2h3v8.92c-.74-.13-1.5-.34-2.21-.65c-.74-.32-1.39-.71-1.97-1.18s-1.04-.98-1.38-1.54L7 15l-4-3v3c0 .97.27 1.88.82 2.72A8.2 8.2 0 0 0 6 19.95c.87.64 1.84 1.14 2.88 1.5c1.05.36 2.09.55 3.12.55s2.07-.2 3.12-.56c1.04-.36 2.01-.86 2.88-1.49c.92-.64 1.63-1.38 2.18-2.23c.55-.84.82-1.75.82-2.72v-3l-4 3l1.56 1.55c-.34.56-.8 1.07-1.38 1.54s-1.23.86-1.97 1.18c-.71.31-1.47.52-2.21.65V11h3V9h-3V7.82A3 3 0 0 0 15 5a3 3 0 0 0-3-3m0 2a1 1 0 0 1 1 1a1 1 0 0 1-1 1a1 1 0 0 1-1-1a1 1 0 0 1 1-1"/></g>
</svg>"""
    with open(os.path.join(root, "assets", "img", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(fav)
    for name, fn in PAGES.items():
        with open(os.path.join(root, name), "w", encoding="utf-8") as f:
            f.write(fn())
        print("built", name)
