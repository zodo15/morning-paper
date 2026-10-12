(function () {
  'use strict';
  var D = window.PAPER_DATA;
  var app = document.getElementById('app');
  var SPEEDS = [1, 1.25, 1.5, 0.75];

  /* ---------- plates: section title pictures ---------- */
  var PLATES = {
    '7:Front page': 'photos/lead-cpi.jpg',
    '7:Markets': 'photos/markets-nifty.jpg',
    '7:Sport': 'photos/cricket.jpg',
    '7:What\u2019s new radar': 'photos/ai-radar.jpg',
    '7:Startup case study': 'photos/longread-phonepe.jpg',
    '6:Front page': 'photos/rupee-shield.jpg',
    '5:Front page': 'photos/markets-nifty.jpg',
    '5:Markets': 'photos/markets-nifty.jpg',
    '6:Policy desk': 'photos/rupee-shield.jpg',
    '4:What\u2019s new radar': 'photos/ai-radar.jpg',
    '5:What\u2019s new radar': 'photos/ai-radar.jpg',
    '6:What\u2019s new radar': 'photos/ai-radar.jpg',
    '6:Sport': 'photos/cricket.jpg',
    '3:Front page': 'photos/rupee-shield.jpg'
  };
  function plateFor(day, heading) {
    for (var k in PLATES) {
      var parts = k.split(':');
      if (parseInt(parts[0], 10) === day && heading.indexOf(parts.slice(1).join(':')) === 0) return PLATES[k];
    }
    return null;
  }

  /* ---------- reader (speechSynthesis word highlight) ---------- */
  var R = { blocks: [], bi: 0, utter: null, playing: false, speedIdx: 0, label: '' };
  var rbar = document.getElementById('reader-bar');
  var rbToggle = document.getElementById('rb-toggle');
  var rbStop = document.getElementById('rb-stop');
  var rbSpeed = document.getElementById('rb-speed');
  var rbLabel = document.getElementById('rb-label');

  function clearMarks() {
    var on = document.querySelectorAll('.w.on, .w.done');
    for (var i = 0; i < on.length; i++) on[i].classList.remove('on', 'done');
  }
  function wrapWords(el) {
    if (el.dataset.wrapped) return;
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (node) {
      var frag = document.createDocumentFragment();
      node.nodeValue.split(/(\s+)/).forEach(function (piece) {
        if (!piece) return;
        if (/^\s+$/.test(piece)) { frag.appendChild(document.createTextNode(piece)); return; }
        var s = document.createElement('span');
        s.className = 'w'; s.textContent = piece;
        frag.appendChild(s);
      });
      node.parentNode.replaceChild(frag, node);
    });
    el.dataset.wrapped = '1';
  }
  function collectBlocks(scopeEl) {
    var els = scopeEl.querySelectorAll('.rp');
    var blocks = [];
    els.forEach(function (el) {
      wrapWords(el);
      var spans = el.querySelectorAll('.w');
      if (!spans.length) return;
      var text = el.textContent;
      var offsets = [], pos = 0;
      spans.forEach(function (s) {
        var idx = text.indexOf(s.textContent, pos);
        offsets.push(idx); pos = idx + s.textContent.length;
      });
      blocks.push({ el: el, spans: spans, text: text, offsets: offsets });
    });
    return blocks;
  }
  function speakBlock() {
    if (R.bi >= R.blocks.length) { stopReader(); return; }
    var b = R.blocks[R.bi];
    var u = new SpeechSynthesisUtterance(b.text);
    u.rate = SPEEDS[R.speedIdx];
    u.onboundary = function (e) {
      if (typeof e.charIndex !== 'number') return;
      var wi = 0;
      for (var i = 0; i < b.offsets.length; i++) { if (b.offsets[i] <= e.charIndex) wi = i; else break; }
      b.spans.forEach(function (s, i) {
        s.classList.toggle('on', i === wi);
        s.classList.toggle('done', i < wi);
      });
    };
    u.onend = function () {
      b.spans.forEach(function (s) { s.classList.remove('on'); s.classList.add('done'); });
      R.bi++;
      if (R.playing) speakBlock();
    };
    R.utter = u;
    window.speechSynthesis.speak(u);
  }
  function startReader(scopeEl, label) {
    stopReader();
    R.blocks = collectBlocks(scopeEl);
    if (!R.blocks.length) return;
    R.bi = 0; R.playing = true; R.label = label;
    rbLabel.textContent = label;
    rbToggle.innerHTML = '&#10073;&#10073;';
    rbSpeed.innerHTML = SPEEDS[R.speedIdx] + '&times;';
    rbar.hidden = false;
    speakBlock();
  }
  function stopReader() {
    R.playing = false;
    try { window.speechSynthesis.cancel(); } catch (e) {}
    clearMarks();
    rbar.hidden = true;
  }
  rbToggle.addEventListener('click', function () {
    if (!R.blocks.length) return;
    if (R.playing) {
      window.speechSynthesis.pause(); R.playing = false;
      rbToggle.innerHTML = '&#9654;';
    } else {
      R.playing = true; rbToggle.innerHTML = '&#10073;&#10073;';
      window.speechSynthesis.resume();
    }
  });
  rbStop.addEventListener('click', stopReader);
  rbSpeed.addEventListener('click', function () {
    R.speedIdx = (R.speedIdx + 1) % SPEEDS.length;
    rbSpeed.innerHTML = SPEEDS[R.speedIdx] + '&times;';
    if (R.playing && R.utter) { // restart current block at new rate
      window.speechSynthesis.cancel();
      speakBlock();
    }
  });

  /* ---------- audio players ---------- */
  function playerHTML(day, kind, label, sub, dark) {
    var audio = D.audio[String(day)];
    var src = audio && audio[kind];
    var off = !src;
    return '<div class="player' + (dark ? ' dark' : '') + (off ? ' off' : '') + '" data-src="' + (src || '') + '">' +
      '<button class="play-btn" ' + (off ? 'disabled' : '') + ' aria-label="Play ' + label + '"></button>' +
      '<div class="player-mid"><div class="player-meta"><b>' + label + '</b><span>' + sub + '</span></div>' +
      (off ? '<div class="player-note">Audio lands with edition 8 - the reader below reads this page aloud today.</div>' : '<div class="player-track"><div class="player-fill"></div></div>') +
      '</div>' +
      '<div class="player-right">' +
      '<button class="speed-btn" ' + (off ? 'disabled' : '') + '>1&times;</button>' +
      '<span class="player-dur">' + (off ? '--:--' : '0:00') + '</span></div></div>';
  }
  function wirePlayers(root) {
    root.querySelectorAll('.player:not(.off)').forEach(function (p) {
      var a = new Audio(p.dataset.src);
      var btn = p.querySelector('.play-btn');
      var fill = p.querySelector('.player-fill');
      var dur = p.querySelector('.player-dur');
      var spd = p.querySelector('.speed-btn');
      var si = 0;
      function fmt(t) { if (!isFinite(t)) return '--:--'; var m = Math.floor(t / 60), s = Math.floor(t % 60); return m + ':' + (s < 10 ? '0' : '') + s; }
      a.addEventListener('loadedmetadata', function () { dur.textContent = fmt(a.duration); });
      a.addEventListener('timeupdate', function () {
        if (a.duration) fill.style.width = (a.currentTime / a.duration * 100) + '%';
        dur.textContent = fmt(a.currentTime);
      });
      a.addEventListener('ended', function () { btn.classList.remove('playing'); });
      btn.addEventListener('click', function () {
        root.querySelectorAll('.player:not(.off)').forEach(function (o) { if (o !== p && o._a) { o._a.pause(); o.querySelector('.play-btn').classList.remove('playing'); } });
        if (a.paused) { a.play(); btn.classList.add('playing'); } else { a.pause(); btn.classList.remove('playing'); }
      });
      spd.addEventListener('click', function () {
        si = (si + 1) % SPEEDS.length;
        a.playbackRate = SPEEDS[si];
        spd.innerHTML = SPEEDS[si] + '&times;';
      });
      p._a = a;
    });
  }

  /* ---------- render helpers ---------- */
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function blockHTML(b) {
    switch (b.t) {
      case 'story': return (b.kicker ? '<div class="story-kicker">' + esc(b.kicker) + '</div>' : '') + '<h3 class="story-title">' + esc(b.title) + '</h3>';
      case 'p': return '<p class="body-p rp">' + b.html + '</p>';
      case 'bullets': return '<ul class="bullets">' + b.items.map(function (i) { return '<li class="rp">' + esc(i) + '</li>'; }).join('') + '</ul>';
      case 'rows': return '<div class="rows">' + b.items.map(function (r) {
          return '<div class="row">' + (r.n ? '<span class="row-n">' + esc(r.n) + '</span>' : '') +
            '<div><span class="row-title">' + esc(r.title) + '</span><span class="row-detail rp">' + esc(r.detail) + '</span></div></div>';
        }).join('') + '</div>';
      case 'facts': return '<dl class="facts">' + b.items.map(function (f) { return '<div><dt>' + esc(f.k) + '</dt><dd>' + esc(f.v) + '</dd></div>'; }).join('') + '</dl>';
      case 'callout': return '<aside class="callout rp">' + b.html + '</aside>';
      case 'closing': return '<div class="closing rp">' + b.html + '</div>';
      case 'figure': return b.img ? '<figure class="plate"><img src="' + b.img + '" alt="' + esc(b.alt || '') + '" loading="lazy">' + (b.caption ? '<figcaption>' + esc(b.caption) + '</figcaption>' : '') + '</figure>' : '';
    }
    return '';
  }
  function mast(active) {
    var today = D.meta[D.today];
    return '<div class="mast">' +
      '<div class="mast-top"><span class="live-dot"></span><span>A personal daily &middot; brewed before breakfast</span></div>' +
      '<div class="mast-name"><a href="#/">The Morning Paper</a></div>' +
      '<div class="mast-sub">' + esc(today.date) + ' &middot; Edition ' + D.today + ' of 7 &middot; the trial week</div>' +
      '<div class="mast-rule"></div>' +
      '<div class="tabs"><a class="tab' + (active === 'today' ? ' active' : '') + '" href="#/">Today</a>' +
      '<a class="tab' + (active === 'archive' ? ' active' : '') + '" href="#/archive">Archive</a></div></div>';
  }
  function tickerHTML(day) {
    var ed = D.editions[day];
    var g = ed.groups.filter(function (x) { return x.heading.indexOf('Eight things') === 0; })[0];
    if (!g) return '';
    var items = [];
    g.blocks.forEach(function (b) { if (b.t === 'bullets') items = items.concat(b.items); });
    var txt = items.slice(0, 5).map(function (i) { return esc(i.split('.')[0]); }).join(' &nbsp;&bull;&nbsp; ');
    return '<div class="ticker"><span class="ticker-in">' + txt + ' &nbsp;&bull;&nbsp; ' + txt + '</span></div>';
  }
  function conceptHTML() {
    var c = D.concept;
    return '<div class="concept"><div class="concept-label">' + esc(c.label) + '</div>' +
      '<div class="concept-name">' + esc(c.name) + '</div><div class="concept-line">' + esc(c.line) + '</div></div>';
  }
  function lrTeaser(day) {
    var lrDay = D.meta[day].longread;
    if (!lrDay) return '';
    var lr = D.longreads[lrDay];
    return '<a class="lr-teaser" href="#/longread/' + lrDay + '"><div class="k">The long read</div>' +
      '<div class="t">' + esc(lr.title) + '</div><div class="d">' + esc(lr.fact) + '</div>' +
      '<div class="go">Read it &rarr;</div></a>';
  }

  /* ---------- pages ---------- */
  function editionBody(day, isToday) {
    var ed = D.editions[day];
    var h = '';
    if (isToday) {
      h += playerHTML(day, 'full', 'The full read', 'Every section, read aloud', true);
      h += playerHTML(day, 'quick', 'The quick listen', 'Five minutes, just what matters', false);
      h += conceptHTML();
    }
    if (ed.hero && ed.hero.img) {
      h += '<figure class="plate"><img src="' + ed.hero.img + '" alt="' + esc(ed.hero.alt || '') + '">' +
        (ed.hero.caption ? '<figcaption>' + esc(ed.hero.caption) + '</figcaption>' : '') + '</figure>';
    }
    ed.groups.forEach(function (g, gi) {
      h += '<section class="section" id="g' + gi + '"><div class="section-head">' +
        '<div class="section-title">' + esc(g.heading) + '</div>' +
        '<button class="listen-btn" data-g="' + gi + '">&#9654; Listen</button></div>';
      var plate = plateFor(day, g.heading);
      if (plate) h += '<figure class="plate"><img src="' + plate + '" alt="" loading="lazy"></figure>';
      g.blocks.forEach(function (b) { h += blockHTML(b); });
      if (g.heading.indexOf('Startup case study') === 0) h += lrTeaser(day);
      h += '</section>';
    });
    return h;
  }
  function ednavHTML(day) {
    return '<div class="ednav">' +
      '<a class="ednav-btn' + (day <= 1 ? ' disabled' : '') + '" href="#/edition/' + (day - 1) + '">&larr; ' + (day > 1 ? esc(D.meta[day - 1].short) : '') + '</a>' +
      '<a class="ednav-btn next' + (day >= D.today ? ' disabled' : '') + '" href="#/edition/' + (day + 1) + '">' + (day < D.today ? esc(D.meta[day + 1].short) : '') + ' &rarr;</a></div>';
  }
  function renderToday() {
    var ed = D.editions[D.today];
    var h = '<div class="wrap">' + mast('today') + tickerHTML(D.today) +
      '<div class="kicker">Today &middot; ' + esc(D.meta[D.today].date) + '</div>' +
      '<h1 class="h1">' + esc(ed.fact) + '</h1>' +
      '<p class="intro">' + esc(ed.intro) + '</p>' +
      editionBody(D.today, true) + ednavHTML(D.today) +
      '<div class="footer"><span>The Morning Paper &middot; trial week, Oct 6-12</span><span>Set in Fraunces &amp; Source Serif</span></div></div>';
    app.innerHTML = h;
    wirePlayers(app);
  }
  function renderArchive() {
    var h = '<div class="wrap">' + mast('archive') +
      '<div class="arch-title">The archive</div>' +
      '<div class="arch-sub">Every edition of the trial week, complete. Seven days, Oct 6-12.</div>';
    for (var n = D.today; n >= 1; n--) {
      var ed = D.editions[n];
      var thumb = (ed.hero && ed.hero.img) || plateFor(n, 'Front page') || 'photos/concept-compounding.jpg';
      h += '<a class="arch-card" href="#/edition/' + n + '"><span class="arch-num">' + n + '</span>' +
        '<span class="arch-meta"><b>' + esc(D.meta[n].date) + (n === D.today ? ' &nbsp;<span class="arch-today-tag">Today</span>' : '') + '</b>' +
        '<span>' + esc(ed.fact) + '</span></span>' +
        '<img class="arch-thumb" src="' + thumb + '" alt="" loading="lazy"></a>';
    }
    h += '<div class="footer"><span>The Morning Paper</span><span>7 editions</span></div></div>';
    app.innerHTML = h;
  }
  function renderEdition(n) {
    var ed = D.editions[n];
    if (!ed) { renderArchive(); return; }
    var h = '<div class="wrap">' + mast('') +
      '<div class="kicker">Edition ' + n + ' &middot; ' + esc(D.meta[n].date) + '</div>' +
      '<h1 class="h1">' + esc(ed.fact) + '</h1>' +
      '<p class="intro">' + esc(ed.intro) + '</p>' +
      editionBody(n, n === D.today) + ednavHTML(n) +
      '<div class="footer"><span>The Morning Paper</span><span><a href="#/archive">Full archive</a></span></div></div>';
    app.innerHTML = h;
    wirePlayers(app);
  }
  function renderLongread(n) {
    var lr = D.longreads[n];
    if (!lr) { renderArchive(); return; }
    var h = '<div class="wrap">' + mast('') +
      '<div class="kicker">The long read &middot; ' + esc(D.meta[n].date) + '</div>' +
      '<h1 class="h1">' + esc(lr.title) + '</h1>' +
      '<p class="intro">' + esc(lr.intro || lr.fact) + '</p>';
    if (lr.hero && lr.hero.img) {
      h += '<figure class="plate"><img src="' + lr.hero.img + '" alt="' + esc(lr.hero.alt || '') + '">' +
        (lr.hero.caption ? '<figcaption>' + esc(lr.hero.caption) + '</figcaption>' : '') + '</figure>';
    }
    lr.groups.forEach(function (g, gi) {
      h += '<section class="section"><div class="section-head"><div class="section-title">' + esc(g.heading) + '</div>' +
        '<button class="listen-btn" data-lg="' + gi + '">&#9654; Listen</button></div>';
      g.blocks.forEach(function (b) { h += blockHTML(b); });
      h += '</section>';
    });
    h += '<div class="ednav"><a class="ednav-btn" href="#/edition/' + n + '">&larr; Back to the edition</a></div>' +
      '<div class="footer"><span>The Morning Paper &middot; long reads</span></div></div>';
    app.innerHTML = h;
  }

  /* ---------- router ---------- */
  function route() {
    stopReader();
    var hash = location.hash.replace(/^#\/?/, '');
    var m;
    if (!hash || hash === 'today') renderToday();
    else if (hash === 'archive') renderArchive();
    else if ((m = hash.match(/^edition\/(\d+)$/))) renderEdition(parseInt(m[1], 10));
    else if ((m = hash.match(/^longread\/(\d+)$/))) renderLongread(parseInt(m[1], 10));
    else renderToday();
    window.scrollTo(0, 0);
  }
  window.addEventListener('hashchange', route);
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.listen-btn');
    if (!btn) return;
    var sec = btn.closest('.section');
    var label = sec.querySelector('.section-title').textContent;
    startReader(sec, label);
    sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  route();
})();
