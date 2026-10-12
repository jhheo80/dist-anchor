/* 운영 프로그램 게시판 — 구글 시트에서 목록을 읽어 화면에 그립니다.
   시트 주소는 programs.html 안의 PROGRAM_SHEET 설정에서 바꿉니다. */
(function () {
  'use strict';

  var CFG = window.PROGRAM_SHEET || {};
  var grid = document.getElementById('gal');
  var chipbox = document.getElementById('gal-chips');
  var live = document.getElementById('gal-live');
  if (!grid) return;

  /* ---------- CSV 파서 (따옴표·줄바꿈 포함 처리) ---------- */
  function parseCSV(text) {
    var rows = [], row = [], val = '', q = false, i = 0, c;
    text = text.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    for (; i < text.length; i++) {
      c = text[i];
      if (q) {
        if (c === '"') { if (text[i + 1] === '"') { val += '"'; i++; } else q = false; }
        else val += c;
      } else if (c === '"') q = true;
      else if (c === ',') { row.push(val); val = ''; }
      else if (c === '\n') { row.push(val); rows.push(row); row = []; val = ''; }
      else val += c;
    }
    if (val !== '' || row.length) { row.push(val); rows.push(row); }
    return rows;
  }

  /* ---------- 구글 드라이브 링크를 이미지 주소로 변환 ---------- */
  function imageUrl(raw) {
    var u = (raw || '').trim();
    if (!u) return '';
    var m = u.match(/drive\.google\.com\/(?:file\/d\/|open\?id=|uc\?id=|thumbnail\?id=)([\w-]{20,})/);
    if (m) return 'https://drive.google.com/thumbnail?id=' + m[1] + '&sz=w1000';
    m = u.match(/[?&]id=([\w-]{20,})/);
    if (m && u.indexOf('google.com') > -1) return 'https://drive.google.com/thumbnail?id=' + m[1] + '&sz=w1000';
    return u;
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (ch) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch];
    });
  }

  var PH = '<div class="pg__ph"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/></svg></div>';

  function state(kind, title, msg) {
    var ic = kind === 'error'
      ? '<path d="M12 9v4M12 17h.01"/><circle cx="12" cy="12" r="10"/>'
      : '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/>';
    grid.className = '';
    grid.innerHTML = '<div class="gal-state"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
      + 'stroke-width="1.6" stroke-linecap="round" aria-hidden="true">' + ic + '</svg>'
      + '<b>' + esc(title) + '</b><span>' + esc(msg) + '</span></div>';
  }

  function skeleton() {
    var h = '';
    for (var i = 0; i < 6; i++) h += '<div class="gal-skel"><div class="s1"></div><div class="s2"></div><div class="s3"></div></div>';
    grid.innerHTML = h;
  }

  /* ---------- 상세 보기 ---------- */
  var modal = document.getElementById('pgm'), lastFocus = null;
  function openModal(it) {
    document.getElementById('pgm-img').src = it.img || '';
    document.getElementById('pgm-img').style.display = it.img ? '' : 'none';
    document.getElementById('pgm-img').alt = it.title;
    document.getElementById('pgm-img').onerror = function () { this.style.display = 'none'; };
    document.getElementById('pgm-t').textContent = it.title;
    var meta = document.getElementById('pgm-meta'); meta.innerHTML = '';
    if (it.cat) meta.innerHTML += '<span class="tag">' + esc(it.cat) + '</span>';
    if (it.date) meta.innerHTML += '<span class="pg__d">' + esc(it.date) + '</span>';
    document.getElementById('pgm-s').textContent = it.body || it.summary || '';
    var link = document.getElementById('pgm-link');
    if (it.link) { link.href = it.link; link.hidden = false; } else { link.hidden = true; }
    lastFocus = document.activeElement;
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    document.getElementById('pgm-x').focus();
  }
  function closeModal() {
    modal.hidden = true;
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }
  if (modal) {
    document.getElementById('pgm-x').addEventListener('click', closeModal);
    modal.querySelector('.pgm__bd').addEventListener('click', closeModal);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !modal.hidden) closeModal(); });
  }

  /* ---------- 렌더링 ---------- */
  var ALL = [], filter = '전체';

  function render() {
    var list = filter === '전체' ? ALL : ALL.filter(function (x) { return x.cat === filter; });
    if (!list.length) { state('empty', '해당 분류의 프로그램이 없습니다', '다른 분류를 선택해 보세요.'); return; }
    grid.className = 'gal';
    grid.innerHTML = list.map(function (it, i) {
      return '<button class="pg" type="button" data-i="' + ALL.indexOf(it) + '">'
        + '<span class="pg__thumb">'
        + (it.cat ? '<span class="pg__tag">' + esc(it.cat) + '</span>' : '')
        + PH
        + (it.img ? '<img src="' + esc(it.img) + '" alt="" loading="lazy" data-fallback="1">' : '')
        + '</span>'
        + '<span class="pg__body">'
        + '<span class="pg__t">' + esc(it.title) + '</span>'
        + (it.date ? '<span class="pg__d">' + esc(it.date) + '</span>' : '')
        + (it.summary ? '<p class="pg__s">' + esc(it.summary) + '</p>' : '')
        + '</span></button>';
    }).join('');
    grid.querySelectorAll('.pg').forEach(function (b) {
      b.addEventListener('click', function () { openModal(ALL[+b.dataset.i]); });
    });
    // 사진 주소가 잘못됐거나 공개 설정이 안 된 경우 기본 그림으로 교체
    grid.querySelectorAll('img[data-fallback]').forEach(function (im) {
      im.addEventListener('error', function () { im.remove(); });
    });
    if (live) live.textContent = filter + ' — ' + list.length + '건';
  }

  function buildChips() {
    if (!chipbox) return;
    var cats = ['전체'];
    ALL.forEach(function (x) { if (x.cat && cats.indexOf(x.cat) < 0) cats.push(x.cat); });
    if (cats.length < 3) { chipbox.hidden = true; return; }
    chipbox.innerHTML = cats.map(function (c) {
      return '<button class="chip" type="button" aria-pressed="' + (c === '전체') + '">' + esc(c) + '</button>';
    }).join('');
    chipbox.querySelectorAll('.chip').forEach(function (b) {
      b.addEventListener('click', function () {
        filter = b.textContent.trim();
        chipbox.querySelectorAll('.chip').forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        render();
      });
    });
  }

  /* ---------- 시트 읽기 ---------- */
  function col(head, names) {
    for (var i = 0; i < head.length; i++) {
      var h = head[i].replace(/\s/g, '');
      for (var j = 0; j < names.length; j++) if (h === names[j]) return i;
    }
    return -1;
  }

  if (!CFG.id) { state('empty', '시트가 아직 연결되지 않았습니다', 'programs.html 안의 PROGRAM_SHEET 설정에 구글 시트 ID를 넣어 주세요.'); return; }

  skeleton();
  var url = 'https://docs.google.com/spreadsheets/d/' + CFG.id + '/gviz/tq?tqx=out:csv'
          + (CFG.sheet ? '&sheet=' + encodeURIComponent(CFG.sheet) : '');

  fetch(url, { cache: 'no-store' })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
    .then(function (txt) {
      var rows = parseCSV(txt).filter(function (r) { return r.join('').trim() !== ''; });
      if (rows.length < 2) { state('empty', '아직 등록된 프로그램이 없습니다', '구글 시트에 첫 번째 프로그램을 추가해 보세요.'); return; }
      var head = rows[0];
      var iOn = col(head, ['게시', '공개', '표시']),
          iT  = col(head, ['제목', '프로그램명']),
          iC  = col(head, ['분류', '구분', '카테고리']),
          iD  = col(head, ['날짜', '일자', '기간']),
          iS  = col(head, ['요약', '한줄소개']),
          iB  = col(head, ['내용', '본문', '설명']),
          iI  = col(head, ['사진', '사진링크', '이미지', '이미지링크']),
          iL  = col(head, ['링크', '자세히보기', '신청링크']);
      if (iT < 0) { state('error', '시트 형식을 확인해 주세요', '첫 줄에 "제목" 열이 있어야 합니다.'); return; }

      ALL = rows.slice(1).map(function (r) {
        return {
          on: iOn < 0 ? true : /^(y|yes|o|true|공개|게시|1)$/i.test((r[iOn] || '').trim()),
          title: (r[iT] || '').trim(),
          cat: iC < 0 ? '' : (r[iC] || '').trim(),
          date: iD < 0 ? '' : (r[iD] || '').trim(),
          summary: iS < 0 ? '' : (r[iS] || '').trim(),
          body: iB < 0 ? '' : (r[iB] || '').trim(),
          img: iI < 0 ? '' : imageUrl(r[iI]),
          link: iL < 0 ? '' : (r[iL] || '').trim()
        };
      }).filter(function (x) { return x.title && x.on; });

      if (!ALL.length) { state('empty', '표시할 프로그램이 없습니다', '시트의 "게시" 열이 Y로 되어 있는지 확인해 주세요.'); return; }
      buildChips();
      render();
    })
    .catch(function () {
      state('error', '목록을 불러오지 못했습니다',
        '구글 시트가 "링크가 있는 모든 사용자에게 공개"로 설정되어 있는지 확인해 주세요.');
    });
})();
