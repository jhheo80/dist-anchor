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

NAV = [
    ("index.html", "홈"),
    ("about.html", "사업소개"),
    ("projects.html", "세부과제"),
    ("departments.html", "참여학과"),
    ("contact.html", "문의·오시는 길"),
]

# ── 아이콘 (Lucide 계열, 24x24 stroke) ─────────────────────────────
IC = {
    "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "sprout": '<path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/><path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/><path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"/>',
    "factory": '<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2z"/><path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "network": '<rect x="9" y="2" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="16" y="16" width="6" height="6" rx="1"/><path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3"/><path d="M12 12V8"/>',
    "graduation": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M15 2v2M9 2v2M15 20v2M9 20v2M2 15h2M2 9h2M20 15h2M20 9h2"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7z"/>',
    "plane": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.4-.2c.4-.2.7-.6.6-1.2z"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "flask": '<path d="M10 2v7.31"/><path d="M14 9.3V1.99"/><path d="M8.5 2h7"/><path d="M14 9.3a6.5 6.5 0 1 1-4 0"/><path d="M5.52 16h12.96"/>',
    "chef": '<path d="M6 13.87A4 4 0 0 1 7.41 6a5.11 5.11 0 0 1 1.05-1.54 5 5 0 0 1 7.08 0A5.11 5.11 0 0 1 16.59 6 4 4 0 0 1 18 13.87V21H6z"/><path d="M6 17h12"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><path d="M20 4 8.12 15.88"/><circle cx="6" cy="18" r="3"/><path d="M14.8 14.8 20 20"/>',
    "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "baby": '<path d="M9 12h.01M15 12h.01"/><path d="M10 16c.5.3 1.2.5 2 .5s1.5-.2 2-.5"/><circle cx="12" cy="12" r="10"/>',
    "ship": '<path d="M2 21c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2s2.5 2 5 2 2.5-2 5-2c1.3 0 1.9.5 2.5 1"/><path d="M19.38 20A11.6 11.6 0 0 0 21 14l-9-4-9 4c0 2.9.94 5.34 2.81 7.76"/><path d="M12 10V2M8 6h8"/>',
    "snow": '<path d="M12 2v20M4.93 4.93l14.14 14.14M19.07 4.93 4.93 19.07M2 12h20"/>',
    "compass": '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "printer": '<polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "layers": '<path d="m12.83 2.18 8.34 4.17a1 1 0 0 1 0 1.79l-8.34 4.17a2 2 0 0 1-1.66 0L2.83 8.14a1 1 0 0 1 0-1.79l8.34-4.17a2 2 0 0 1 1.66 0z"/><path d="m2.83 15.86 8.34 4.17a2 2 0 0 0 1.66 0l8.34-4.17"/><path d="m2.83 11.86 8.34 4.17a2 2 0 0 0 1.66 0l8.34-4.17"/>',
    "spark": '<path d="M12 3v3M12 18v3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M3 12h3M18 12h3M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="3"/>',
    "lightbulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6M10 22h4"/>',
    "handshake": '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.9-3.9a2 2 0 0 1 0-2.8l.4-.4a2.8 2.8 0 0 1 4 0l4 4"/><path d="m21 3 1 1"/><path d="M3 4h4l4 4"/><path d="m2 12 4.6 4.6a1 1 0 1 0 3-3"/>',
}


def icon(name, cls=""):
    p = IC.get(name, IC["target"])
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
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
    ("간호학과", "4년제", "heart"), ("호텔식품제과제빵과", "", "chef"),
    ("AI기계제어과", "", "cpu"), ("헤어디자인과", "", "scissors"),
    ("안경광학과", "3년제", "eye"), ("메카트로닉스과", "", "wrench"),
    ("선박동력기계과", "", "ship"), ("생활문화예술과", "", "spark"),
    ("보건의료행정과", "", "briefcase"), ("산업안전관리과", "", "shield"),
    ("스포츠재활운동과", "", "activity"), ("사회복지과", "주간/야간", "users"),
    ("디저트카페창업과", "", "chef"), ("항공정비과", "3년제", "plane"),
    ("전문스포츠지도과", "", "activity"), ("보건복지과", "", "heart"),
    ("글로벌외식조리과", "", "chef"), ("항공기계과", "", "plane"),
    ("파크골프건강지도과", "신설", "activity"), ("유아교육과", "3년제", "baby"),
    ("AI푸드창업과", "", "cpu"), ("냉동공조설비과", "", "snow"),
    ("자율전공학부", "", "compass"),
]

# ── 데이터: 추진 방향 / 인재상 / 로드맵 / 협의체 ───────────────────
DIRECTIONS = [
    ("target", "담대한 대학혁신을 통한 지역 사회 수요 기반의 대학교육 실현"),
    ("network", "대학–지자체–기업 간 연계성 강화를 통한 거버넌스 활동 실천"),
    ("factory", "기업 현장을 이용한 OJT(현장실습, 인턴십 등) 교육운영 강화"),
    ("graduation", "ANCHOR 체계를 통한 생애 주기 맞춤 지역인재 양성 프로세스 운영"),
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
    ("14", "선정 단위·세부과제"), ("4", "대 추진 프로젝트"),
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
<meta name="theme-color" content="#2C5E13">
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
          <rect width="40" height="40" rx="11" fill="#2C5E13"/>
          <path d="M20 9v22M20 31c-4.5 0-8-3.2-8-7M20 31c4.5 0 8-3.2 8-7" stroke="#AEEB5D" stroke-width="2.6" stroke-linecap="round"/>
          <circle cx="20" cy="13" r="3.4" stroke="#AEEB5D" stroke-width="2.6"/>
          <path d="M14 17h12" stroke="#AEEB5D" stroke-width="2.6" stroke-linecap="round"/>
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
    return f'<div class="shead rv"><span class="shead__kicker">{kicker}</span><h2>{title}</h2>{d}</div>'


# ── 페이지: 홈 ────────────────────────────────────────────────────
def page_index():
    stats = "".join('<div class="hero__stat"><b>%s</b><span>%s</span></div>' % s for s in STATS)
    pcards = "".join(f"""
      <a class="card card--hover pcard {p['cls']} rv" href="projects.html#{p['cls']}">
        <span class="icon-badge">{icon(p['icon'])}</span>
        <span class="pcard__no">{p['no']}</span>
        <h3>{p['title']}</h3>
        <p>{p['desc']}</p>
      </a>""" for p in PROJECTS)
    dirs = "".join(f"""
      <div class="card rv">
        <span class="icon-badge">{icon(ic)}</span>
        <p style="color:var(--ink);font-weight:600;font-size:.98rem">{txt}</p>
      </div>""" for ic, txt in DIRECTIONS)
    road = "".join('<li class="tl__item rv"><span class="tl__yr">%s</span><p>%s</p></li>' % r for r in ROADMAP)

    return head("홈", f"{SITE} — {SLOGAN}. 지역맞춤형 혁신과 발전을 선도하는 유니컬라이제이션 인재양성.", "index.html") + f"""
<section class="hero">
  <div class="hero__deco" aria-hidden="true">
    <svg width="100%" height="100%" viewBox="0 0 1200 620" preserveAspectRatio="xMidYMax slice">
      <defs>
        <linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#AEEB5D" stop-opacity=".30"/>
          <stop offset="100%" stop-color="#AEEB5D" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <path d="M0 470c90-16 140 12 210-6s110-52 190-40 130 62 210 46 140-64 220-52 130 58 190 44 180-40 180-40V620H0z" fill="url(#g1)"/>
      <g fill="none" stroke="#AEEB5D" stroke-opacity=".22" stroke-width="1.4">
        <circle cx="1010" cy="150" r="120"/><circle cx="1010" cy="150" r="76"/><circle cx="1010" cy="150" r="34"/>
        <path d="M1010 30v240M890 150h240"/>
      </g>
    </svg>
  </div>
  <div class="wrap hero__in">
    <p class="hero__eyebrow">{icon('spark', 'ic')} 경상남도 지역혁신중심 대학지원체계 · 14개 과제 선정</p>
    <h1>지역과 함께,<br><span class="accent">미래를 혁신하다</span></h1>
    <p class="hero__lead">동원과학기술대학교 경남앵커사업(ANCHOR)은 지역맞춤형 혁신과 발전을 선도하는
      <strong>유니컬라이제이션(Unification&nbsp;+&nbsp;Localization)</strong> 인재를 양성합니다.</p>
    <div class="hero__cta">
      <a class="btn btn--primary" href="projects.html">14개 세부과제 보기</a>
      <a class="btn btn--ghost" href="about.html">사업 소개</a>
    </div>
    <div class="hero__stats">{stats}</div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    {shead("PROMOTION DIRECTION", "네 갈래의 추진 계획", "대학혁신 · 거버넌스 · 현장교육 · 생애주기 인재양성으로 지역과 대학이 함께 성장합니다.")}
    <div class="grid grid--4">{dirs}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {shead("PROJECTS", "4대 프로젝트", "산업 혁신 인재부터 정주·창업 밸류 창출까지, 지역이 필요로 하는 네 가지 축으로 사업을 추진합니다.")}
    <div class="grid grid--2">{pcards}</div>
  </div>
</section>

<section class="section section--deep">
  <div class="wrap">
    {shead("ROADMAP", "ANCHOR 사업 5개년 추진 방향")}
    <ul class="tl">{road}</ul>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="cta rv">
      <h2>함께 만드는 지역의 미래</h2>
      <p>참여 학과, 프로그램 참여, 산학협력 문의를 환영합니다. 동원앵커사업단이 안내해 드립니다.</p>
      <a class="btn btn--solid" href="contact.html">문의하기</a>
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
    road = "".join('<li class="tl__item rv"><span class="tl__yr">%s</span><p>%s</p></li>' % r for r in ROADMAP)
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

<section class="section section--deep">
  <div class="wrap">
    {shead("ROADMAP", "5개년 추진 방향")}
    <ul class="tl">{road}</ul>
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
        <span class="pcard__no">{p['no']}</span>
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
      <li class="dept rv"><span class="dept__ic">{icon(ic)}</span>
        <span><span class="dept__n">{name}</span>{'<span class="dept__m">%s</span>' % meta if meta else ''}</span>
      </li>""" for name, meta, ic in DEPTS)

    return head("참여학과", "2026학년도 경남 ANCHOR 사업에 참여하는 동원과학기술대학교 23개 학과를 소개합니다.", "departments.html") + \
        phead("참여학과", "26 ANCHOR 사업 학과소개",
              "항공·기계·바이오·보건복지·조리·창업까지, 지역 산업 수요에 맞춘 23개 학과가 함께합니다.") + f"""
<section class="section">
  <div class="wrap">
    {shead("DEPARTMENTS", "참여 학과 23개", "학과별 모집 요강과 교육과정은 동원과학기술대학교 홈페이지에서 확인하실 수 있습니다.")}
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


PAGES = {
    "index.html": page_index,
    "about.html": page_about,
    "projects.html": page_projects,
    "departments.html": page_departments,
    "contact.html": page_contact,
}

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(root, "assets", "img"), exist_ok=True)
    fav = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">
<rect width="40" height="40" rx="9" fill="#2C5E13"/>
<path d="M20 9v22M20 31c-4.5 0-8-3.2-8-7M20 31c4.5 0 8-3.2 8-7" stroke="#AEEB5D" stroke-width="2.8" stroke-linecap="round" fill="none"/>
<circle cx="20" cy="13" r="3.4" stroke="#AEEB5D" stroke-width="2.8" fill="none"/>
<path d="M14 17h12" stroke="#AEEB5D" stroke-width="2.8" stroke-linecap="round"/>
</svg>"""
    with open(os.path.join(root, "assets", "img", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(fav)
    for name, fn in PAGES.items():
        with open(os.path.join(root, name), "w", encoding="utf-8") as f:
            f.write(fn())
        print("built", name)
