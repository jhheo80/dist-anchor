/* 동원과학기술대학교 경남 ANCHOR 사업 — 공통 스크립트 */
(function () {
  'use strict';

  /* ---- 모바일 내비게이션 ---- */
  var toggle = document.querySelector('.navtoggle');
  var nav = document.getElementById('gnb');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /* ---- 아코디언(세부과제) ---- */
  document.querySelectorAll('.task__btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var panel = document.getElementById(btn.getAttribute('aria-controls'));
      if (!panel) return;
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      panel.hidden = open;
    });
  });

  /* ---- 필터 칩 ---- */
  var chips = document.querySelectorAll('.chip[data-filter]');
  if (chips.length) {
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        var key = chip.dataset.filter;
        chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
        document.querySelectorAll('[data-group]').forEach(function (item) {
          var show = key === 'all' || item.dataset.group === key;
          item.hidden = !show;
        });
        var live = document.getElementById('filter-status');
        if (live) {
          var n = document.querySelectorAll('[data-group]:not([hidden])').length;
          live.textContent = chip.textContent.trim() + ' — ' + n + '개 항목 표시';
        }
      });
    });
  }

  /* ---- 스크롤 등장 효과 ---- */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var targets = document.querySelectorAll('.rv');
  if (reduce || !('IntersectionObserver' in window)) {
    targets.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    targets.forEach(function (el, i) {
      el.style.transitionDelay = Math.min(i % 6, 5) * 55 + 'ms';
      io.observe(el);
    });
  }

  /* ---- 현재 연도 ---- */
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
