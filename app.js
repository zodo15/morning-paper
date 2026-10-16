(function () {
  'use strict';
  var D = window.PAPER_DATA;
  var app = document.getElementById('app');
  var SPEEDS = [1, 1.25, 1.5, 2, 0.75];

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
    clearHL();
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
    var times = audio && audio.times && audio.times[kind];
    return '<div class="player' + (dark ? ' dark' : '') + (off ? ' off' : '') + '" data-src="' + (src || '') + '"' +
      (times ? ' data-times="' + times + '"' : '') + ' data-kind="' + kind + '">' +
      '<button class="play-btn" ' + (off ? 'disabled' : '') + ' aria-label="Play ' + label + '"></button>' +
      '<div class="player-mid"><div class="player-meta"><b>' + label + '</b><span>' + sub + '</span></div>' +
      (off ? '<div class="player-note">No recording for this edition - print only.</div>' : '<div class="player-track"><div class="player-fill"></div></div>') +
      '</div>' +
      '<div class="player-right">' +
      (off ? '<span class="player-soon">Soon</span>' : '<button class="speed-btn">1&times;</button>') +
      '<span class="player-dur">' + (off ? '--:--' : '0:00') + '</span></div></div>';
  }
  function fmt(t) { if (!isFinite(t)) return '--:--'; var m = Math.floor(t / 60), s = Math.floor(t % 60); return m + ':' + (s < 10 ? '0' : '') + s; }

  /* sentence highlight synced to the recorded full read */
  var HL = { items: [], ready: false, pending: false, failed: false };
  function clearHL() {
    var on = document.querySelectorAll('.w2.on, .w2.done, .rp.reading-on, .rp.reading-done');
    for (var i = 0; i < on.length; i++) on[i].classList.remove('on', 'done', 'reading-on', 'reading-done');
    HL.items = []; HL.ready = false; HL.pending = false; HL.failed = false;
  }
  function wrapBlockSentences(el, sentences) {
    var text = el.textContent, pos = 0, ranges = [];
    for (var i = 0; i < sentences.length; i++) {
      var t = sentences[i].t;
      var idx = text.indexOf(t, pos);
      if (idx < 0) return null; // text drifted from the script: caller falls back to block-level
      ranges.push({ a: idx, b: idx + t.length, s: sentences[i].s, e: sentences[i].e });
      pos = idx + t.length;
    }
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    var nodes = [], n;
    while ((n = walker.nextNode())) nodes.push(n);
    var items = ranges.map(function (r) { return { s: r.s, e: r.e, spans: [], block: el }; });
    var off = 0;
    nodes.forEach(function (node) {
      var start = off, end = off + node.nodeValue.length;
      var segs = [], cur = start;
      ranges.forEach(function (r, ri) {
        if (r.b <= start || r.a >= end) return;
        var a = Math.max(r.a, start), b = Math.min(r.b, end);
        if (a > cur) segs.push({ a: cur, b: a });
        segs.push({ a: a, b: b, ri: ri });
        cur = Math.max(cur, b);
      });
      if (cur < end) segs.push({ a: cur, b: end });
      if (!segs.length) { off = end; return; }
      var frag = document.createDocumentFragment();
      segs.forEach(function (g) {
        var piece = node.nodeValue.slice(g.a - start, g.b - start);
        if (g.ri == null) { frag.appendChild(document.createTextNode(piece)); return; }
        var sp = document.createElement('span');
        sp.className = 'w2'; sp.textContent = piece;
        frag.appendChild(sp);
        items[g.ri].spans.push(sp);
      });
      node.parentNode.replaceChild(frag, node);
      off = end;
    });
    return items;
  }
  function wrapWholeBlock(el) {
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    var nodes = [], n;
    while ((n = walker.nextNode())) nodes.push(n);
    var spans = [];
    nodes.forEach(function (node) {
      var sp = document.createElement('span');
      sp.className = 'w2'; sp.textContent = node.nodeValue;
      node.parentNode.replaceChild(sp, node);
      spans.push(sp);
    });
    return spans;
  }
  function loadHighlight(timesUrl, scopeEl) {
    if (HL.ready || HL.pending || HL.failed) return;
    HL.pending = true;
    fetch(timesUrl).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (data) {
      var els = scopeEl.querySelectorAll('.rp');
      var items = [];
      for (var i = 0; i < data.blocks.length && i < els.length; i++) {
        var bm = data.blocks[i];
        if (!bm) continue;
        var got = wrapBlockSentences(els[i], bm.sentences || []);
        if (got) items = items.concat(got);
        else if (bm.s != null) items.push({ s: bm.s, e: bm.e, spans: [], block: els[i] });
      }
      items.sort(function (x, y) { return x.s - y.s; });
      if (items.length && items[0].s > 2) {  // spoken opening (greeting, nameplate, fact, intro) has no sentence map: light the title + intro as one honest block, no faked timings
        var leadSpans = [];
        var h1el = scopeEl.querySelector('.h1');
        var introEl = scopeEl.querySelector('.intro');
        var deckEl = scopeEl.querySelector('.deck');
        if (h1el) leadSpans = leadSpans.concat(wrapWholeBlock(h1el));
        if (deckEl) leadSpans = leadSpans.concat(wrapWholeBlock(deckEl));
        if (introEl) leadSpans = leadSpans.concat(wrapWholeBlock(introEl));
        if (leadSpans.length) items.unshift({ s: 0, e: items[0].s, spans: leadSpans, block: introEl || h1el });
      }
      HL.items = items; HL.ready = true; HL.pending = false;
    }).catch(function () { HL.pending = false; HL.failed = true; });
  }
  function setSpans(it, cls, on) {
    it.spans.forEach(function (sp) {
      if (on) sp.classList.add(cls); else sp.classList.remove(cls);
    });
  }
  function updateHL(t) {
    if (!HL.ready) return;
    var cur = null;
    for (var i = 0; i < HL.items.length; i++) {
      var it = HL.items[i];
      if (t >= it.e) {
        setSpans(it, 'on', false); setSpans(it, 'done', true);
        it.block.classList.remove('reading-on'); it.block.classList.add('reading-done');
      } else if (t >= it.s) {
        cur = it;
      } else {
        setSpans(it, 'on', false); setSpans(it, 'done', false);
        it.block.classList.remove('reading-on', 'reading-done');
      }
    }
    if (cur) {
      setSpans(cur, 'on', true);
      cur.block.classList.add('reading-on');
    }
  }

  function wirePlayers(root) {
    root.querySelectorAll('.player:not(.off)').forEach(function (p) {
      var a = new Audio(p.dataset.src);
      var btn = p.querySelector('.play-btn');
      var fill = p.querySelector('.player-fill');
      var track = p.querySelector('.player-track');
      var dur = p.querySelector('.player-dur');
      var spd = p.querySelector('.speed-btn');
      var si = 0;
      a.addEventListener('loadedmetadata', function () { dur.textContent = '0:00 / ' + fmt(a.duration); });
      a.addEventListener('timeupdate', function () {
        if (a.duration) fill.style.width = (a.currentTime / a.duration * 100) + '%';
        dur.textContent = fmt(a.currentTime) + ' / ' + fmt(a.duration);
        if (p.dataset.times) updateHL(a.currentTime);
        if (A.on && A.a === a) audioProgress();
      });
      a.addEventListener('seeked', function () { if (A.a === a) A.last = a.currentTime; });
      a.addEventListener('play', function () { btn.classList.add('playing'); if (A.on && A.a === a) pcToggle.innerHTML = '&#10073;&#10073;'; });
      a.addEventListener('pause', function () { btn.classList.remove('playing'); if (A.on && A.a === a) pcToggle.innerHTML = '&#9654;'; });
      a.addEventListener('ended', function () { btn.classList.remove('playing'); });
      if (track) track.addEventListener('click', function (e) {
        if (!a.duration) return;
        var r = track.getBoundingClientRect();
        a.currentTime = Math.min(Math.max((e.clientX - r.left) / r.width, 0), 1) * a.duration;
      });
      btn.addEventListener('click', function () {
        root.querySelectorAll('.player:not(.off)').forEach(function (o) { if (o !== p && o._a) { o._a.pause(); o.querySelector('.play-btn').classList.remove('playing'); } });
        if (a.paused) {
          stopPacer(true);
          if (p.dataset.times) loadHighlight(p.dataset.times, root);
          a.play(); btn.classList.add('playing');
          enterAudio(a, p, spd);
        } else { a.pause(); btn.classList.remove('playing'); }
      });
      spd.addEventListener('click', function () {
        si = (si + 1) % SPEEDS.length;
        a.playbackRate = SPEEDS[si];
        spd.innerHTML = SPEEDS[si] + '&times;';
      });
      p._a = a;
    });
  }


  /* ---------- silent reading pacer (no audio; WPM-paced sentence highlight) ---------- */
  var splitSents;
  try {
    splitSents = new Function('t', 'return t.split(/(?<=[.!?])\\s+/)');
    splitSents('a. b');
    splitSents = function (t) { return t.split(/(?<=[.!?])\s+/); };
  } catch (e) {
    splitSents = function (t) {
      var parts = t.split(/([.!?])\s+/), out = [];
      for (var i = 0; i < parts.length; i += 2) out.push(parts[i] + (parts[i + 1] || ''));
      return out;
    };
  }
  var P = { items: [], i: 0, running: false, timer: null, tick: null, wpm: 200,
            acc: 0, resumedAt: 0, segStart: 0, segLeft: 0, label: '', base: 0 };
  var pbar = document.getElementById('pacer-bar');
  window.__P = P;
  var pcToggle = document.getElementById('pc-toggle');
  var pcMinus = document.getElementById('pc-minus');
  var pcPlus = document.getElementById('pc-plus');
  var pcWpm = document.getElementById('pc-wpm');
  var pcLabel = document.getElementById('pc-label');
  var pcStats = document.getElementById('pc-stats');
  var pcStop = document.getElementById('pc-stop');
  try { P.wpm = Math.min(600, Math.max(80, parseInt(localStorage.getItem('pacerWpm'), 10) || 200)); } catch (e) {}

  function wordCount(t) { var m = t.trim().split(/\s+/); return m[0] ? m.length : 0; }
  function wrapPacerSentences(el) {
    var text = el.textContent;
    var sents = splitSents(text).filter(function (x) { return x.trim(); });
    if (!sents.length) return [];
    var pos = 0, ranges = [];
    for (var i = 0; i < sents.length; i++) {
      var idx = text.indexOf(sents[i], pos);
      if (idx < 0) return [];
      ranges.push({ a: idx, b: idx + sents[i].length });
      pos = idx + sents[i].length;
    }
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    var nodes = [], n;
    while ((n = walker.nextNode())) nodes.push(n);
    var items = ranges.map(function (r, ri) {
      return { spans: [], block: el, words: wordCount(sents[ri]), text: sents[ri] };
    });
    var off = 0;
    nodes.forEach(function (node) {
      var start = off, end = off + node.nodeValue.length;
      var segs = [], cur = start;
      ranges.forEach(function (r, ri) {
        if (r.b <= start || r.a >= end) return;
        var a = Math.max(r.a, start), b = Math.min(r.b, end);
        if (a > cur) segs.push({ a: cur, b: a });
        segs.push({ a: a, b: b, ri: ri });
        cur = Math.max(cur, b);
      });
      if (cur < end) segs.push({ a: cur, b: end });
      var frag = document.createDocumentFragment();
      segs.forEach(function (g) {
        var piece = node.nodeValue.slice(g.a - start, g.b - start);
        if (g.ri == null) { frag.appendChild(document.createTextNode(piece)); return; }
        var sp = document.createElement('span');
        sp.className = 'pc'; sp.textContent = piece;
        frag.appendChild(sp);
        items[g.ri].spans.push(sp);
      });
      node.parentNode.replaceChild(frag, node);
      off = end;
    });
    return items;
  }
  function pcSet(it, cls, on) {
    it.spans.forEach(function (sp) { if (on) sp.classList.add(cls); else sp.classList.remove(cls); });
  }
  function pcClearMarks() {
    var on = document.querySelectorAll('.pc.pc-on, .pc.pc-done');
    for (var i = 0; i < on.length; i++) on[i].classList.remove('pc-on', 'pc-done');
  }
  function pcElapsed() { return P.acc + (P.running ? Date.now() - P.resumedAt : 0); }
  function pcWordsRead() {
    var w = 0;
    for (var i = P.base; i < P.i && i < P.items.length; i++) w += P.items[i].words;
    return w;
  }
  function pcStatsTick() {
    var s = Math.round(pcElapsed() / 1000);
    pcStats.textContent = Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2) + ' \u00b7 ' + pcWordsRead() + ' words';
  }
  function pcSchedule() {
    clearTimeout(P.timer);
    var it = P.items[P.i];
    if (!it) return;
    var dur = Math.max(250, it.words / P.wpm * 60000);
    P.segStart = Date.now(); P.segLeft = dur;
    P.timer = setTimeout(pcAdvance, dur);
  }
  function pcAdvance() {
    var it = P.items[P.i];
    if (it) { pcSet(it, 'pc-on', false); pcSet(it, 'pc-done', true); }
    P.i++;
    if (P.i >= P.items.length) { pcFinish(); return; }
    var nx = P.items[P.i];
    pcSet(nx, 'pc-on', true);
    var r = nx.block.getBoundingClientRect();
    if (r.top < 90 || r.bottom > window.innerHeight - 90) {
      nx.block.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    pcSchedule();
  }
  function pcPause() {
    if (!P.running) return;
    P.running = false;
    clearTimeout(P.timer); clearInterval(P.tick);
    var now = Date.now();
    P.segLeft = Math.max(0, P.segLeft - (now - P.segStart));
    P.acc += now - P.resumedAt;
    pcToggle.innerHTML = '&#9654;';
  }
  function pcResume() {
    if (P.running || !P.items.length || P.i >= P.items.length) return;
    P.running = true;
    P.resumedAt = Date.now(); P.segStart = Date.now();
    clearTimeout(P.timer);
    P.timer = setTimeout(pcAdvance, P.segLeft);
    P.tick = setInterval(pcStatsTick, 1000);
    pcToggle.innerHTML = '&#10073;&#10073;';
  }
  function pcLogResult() {
    var words = pcWordsRead(), secs = pcElapsed() / 1000;
    if (words < 10 || secs < 5) { pcStats.textContent = ''; return; }
    var eff = Math.round(words / (secs / 60));
    pcStats.textContent = 'done \u00b7 ' + words + ' words in ' + Math.floor(secs / 60) + ':' + ('0' + Math.round(secs % 60)).slice(-2) + ' \u00b7 ' + eff + ' wpm effective';
    try {
      var log = JSON.parse(localStorage.getItem('pacerLog') || '[]');
      log.push({ d: new Date().toISOString().slice(0, 10), page: P.label, wpm: eff, words: words, secs: Math.round(secs) });
      localStorage.setItem('pacerLog', JSON.stringify(log.slice(-100)));
    } catch (e) {}
  }
  function pcFinish() {
    if (P.running) { P.acc += Date.now() - P.resumedAt; P.running = false; }
    clearTimeout(P.timer); clearInterval(P.tick);
    pcLogResult();
    pcToggle.innerHTML = '&#9654;';
  }
  function stopPacer(silent) {
    if (pbar.hidden) return;
    if (P.running) { P.acc += Date.now() - P.resumedAt; P.running = false; }
    clearTimeout(P.timer); clearInterval(P.tick);
    if (!silent) pcLogResult();
    pcClearMarks();
    P.items = []; P.i = 0;
    pbar.hidden = true;
    var act = document.querySelector('.pace-btn.active');
    if (act) act.classList.remove('active');
  }
  function startPacer(scopeEls, label, fromIdx) {
    stopPacer(true); stopReader();
    root_pausePlayers();
    P.items = [];
    scopeEls.forEach(function (scopeEl) {
      scopeEl.querySelectorAll('.rp').forEach(function (el) {
        P.items = P.items.concat(wrapPacerSentences(el));
      });
    });
    if (!P.items.length) return;
    P.i = fromIdx || 0; P.base = P.i; P.acc = 0; P.label = label;
    pcLabel.textContent = label;
    pcWpm.textContent = P.wpm + ' wpm';
    pcStats.textContent = '';
    pbar.hidden = false;
    var cur = P.items[P.i];
    pcSet(cur, 'pc-on', true);
    cur.block.scrollIntoView({ behavior: 'smooth', block: 'center' });
    P.segLeft = Math.max(250, cur.words / P.wpm * 60000);
    P.running = true; P.resumedAt = Date.now(); P.segStart = Date.now();
    P.timer = setTimeout(pcAdvance, P.segLeft);
    P.tick = setInterval(pcStatsTick, 1000);
    pcToggle.innerHTML = '&#10073;&#10073;';
  }

  /* ---------- pacer + voice together: the bar follows the recorded read ---------- */
  var A = { on: false, a: null, last: 0, accWords: 0, accWall: 0, spd: null, hasWords: false };
  function itemWords(it) {
    if (it.words == null) {
      var t = it.spans.length ? it.spans.map(function (sp) { return sp.textContent; }).join('') : it.block.textContent;
      it.words = wordCount(t);
    }
    return it.words;
  }
  function wordsAt(t) {
    if (!HL.ready) return 0;
    var w = 0;
    for (var i = 0; i < HL.items.length; i++) {
      var it = HL.items[i];
      if (t >= it.e) w += itemWords(it);
      else if (t > it.s) w += itemWords(it) * (t - it.s) / Math.max(0.01, it.e - it.s);
    }
    return w;
  }
  function audioStats() {
    var s = Math.round(A.accWall), words = Math.round(A.accWords);
    var useW = A.hasWords && HL.ready;
    pcStats.textContent = Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2) + (useW ? ' \u00b7 ' + words + ' words' : '');
    var wpm = (useW && A.accWall > 8) ? Math.round(A.accWords / (A.accWall / 60)) : null;
    pcWpm.textContent = (wpm ? wpm : '--') + ' wpm \u00b7 ' + A.a.playbackRate + '\u00d7';
  }
  function audioProgress() {
    var t = A.a.currentTime, dt = t - A.last;
    if (!A.a.paused && dt > 0 && dt < 2) {
      A.accWall += dt / A.a.playbackRate;
      if (A.hasWords) A.accWords += wordsAt(t) - wordsAt(A.last);
    }
    A.last = t;
    audioStats();
  }
  function enterAudio(a, p, spd) {
    stopPacer(true); stopReader();
    if (A.a !== a) { A.accWords = 0; A.accWall = 0; }
    A.on = true; A.a = a; A.spd = spd; A.last = a.currentTime; A.hasWords = !!p.dataset.times;
    var nm = p.querySelector('.player-meta b');
    pcLabel.textContent = 'Listening' + (nm ? ' \u00b7 ' + nm.textContent : '');
    pcToggle.innerHTML = '&#10073;&#10073;';
    pbar.hidden = false;
    audioStats();
  }
  function exitAudio() {
    if (!A.on) return;
    A.on = false;
    pbar.hidden = true;
  }
  function root_pausePlayers() {
    exitAudio();
    document.querySelectorAll('.player').forEach(function (o) {
      if (o._a) { o._a.pause(); var b = o.querySelector('.play-btn'); if (b) b.classList.remove('playing'); }
    });
    clearHL();
  }
  pcToggle.addEventListener('click', function () {
    if (A.on) { if (A.a.paused) A.a.play(); else A.a.pause(); return; }
    if (P.running) pcPause(); else pcResume();
  });
  pcStop.addEventListener('click', function () {
    if (A.on) { A.a.pause(); A.on = false; pbar.hidden = true; return; }
    stopPacer(false);
  });
  function pcStep(d) {
    if (A.on) {
      var r = Math.min(3, Math.max(0.5, Math.round((A.a.playbackRate + d / 100) * 100) / 100));
      A.a.playbackRate = r;
      if (A.spd) A.spd.innerHTML = r + '&times;';
      audioStats();
      return;
    }
    var old = P.wpm;
    P.wpm = Math.min(600, Math.max(80, P.wpm + d));
    if (P.wpm === old) return;
    try { localStorage.setItem('pacerWpm', String(P.wpm)); } catch (e) {}
    pcWpm.textContent = P.wpm + ' wpm';
    if (P.running && P.items[P.i]) {  // live-adjust the current sentence's remaining time
      var now = Date.now();
      var left = Math.max(0, P.segLeft - (now - P.segStart));
      P.segLeft = Math.max(120, left * old / P.wpm);
      P.segStart = now;
      clearTimeout(P.timer);
      P.timer = setTimeout(pcAdvance, P.segLeft);
    }
  }
  pcMinus.addEventListener('click', function () { pcStep(-10); });
  pcPlus.addEventListener('click', function () { pcStep(10); });
  document.addEventListener('click', function (e) {  // tap any line to jump the pacer there
    if (pbar.hidden) return;
    var sp = e.target.closest('.pc');
    if (!sp) return;
    for (var i = 0; i < P.items.length; i++) {
      if (P.items[i].spans.indexOf(sp) < 0) continue;
      clearTimeout(P.timer);
      for (var j = 0; j < P.items.length; j++) {
        pcSet(P.items[j], 'pc-on', j === i);
        pcSet(P.items[j], 'pc-done', j < i);
      }
      P.i = i;
      if (P.running) { P.segLeft = Math.max(250, P.items[i].words / P.wpm * 60000); P.segStart = Date.now(); P.timer = setTimeout(pcAdvance, P.segLeft); }
      else { P.segLeft = Math.max(250, P.items[i].words / P.wpm * 60000); }
      return;
    }
  });

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
      case 'chart': return '<figure class="plate chart-fig">' + b.svg + (b.label ? '<figcaption>' + esc(b.label) + '</figcaption>' : '') + '</figure>';
    }
    return '';
  }
  function mast(active) {
    var today = D.meta[D.today];
    return '<div class="mast">' +
      '<div class="mast-top"><span class="live-dot"></span><span>A personal daily &middot; brewed before breakfast</span></div>' +
      '<div class="mast-name"><a href="#/">The Morning Paper</a></div>' +
      '<div class="mast-sub">' + esc(today.date) + ' &middot; Edition ' + D.today + ' &middot; daily</div>' +
      '<div class="mast-rule"></div>' +
      '<div class="tabs"><a class="tab' + (active === 'today' ? ' active' : '') + '" href="#/">Today</a>' +
      '<a class="tab' + (active === 'cards' ? ' active' : '') + '" href="#/cards">Cards<span class="tab-dot" id="cards-dot" hidden></span></a>' +
      '<a class="tab' + (active === 'archive' ? ' active' : '') + '" href="#/archive">Archive</a>' +
      '<a class="tab' + (active === 'longreads' ? ' active' : '') + '" href="#/longreads">Long reads</a></div></div>';
  }
  function tickerHTML(day) {
    var ed = D.editions[day];
    var g = ed.groups.filter(function (x) { return x.heading.indexOf('Eight things') === 0 || /lead route/i.test(x.heading); })[0] ||
            ed.groups.filter(function (x) { return x.blocks.some(function (b) { return b.t === 'bullets'; }); })[0];
    if (!g) return '';
    var items = [];
    g.blocks.forEach(function (b) { if (b.t === 'bullets') items = items.concat(b.items); });
    var txt = items.slice(0, 5).map(function (i) { return esc(i.split(/\.(?=\s|$)/)[0]); }).join(' &nbsp;&bull;&nbsp; ');
    return '<div class="ticker"><span class="ticker-in">' + txt + ' &nbsp;&bull;&nbsp; ' + txt + '</span></div>';
  }
  function conceptHTML(day) {
    var c = (D.editions[day] && D.editions[day].concept) || D.concept;
    if (!c) return '';
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
      h += conceptHTML(day);
    }
    if (ed.hero && ed.hero.img) {
      h += '<figure class="plate"><img src="' + ed.hero.img + '" alt="' + esc(ed.hero.alt || '') + '">' +
        (ed.hero.caption ? '<figcaption>' + esc(ed.hero.caption) + '</figcaption>' : '') + '</figure>';
    }
    var hasFull = D.audio[String(day)] && D.audio[String(day)].full;
    ed.groups.forEach(function (g, gi) {
      h += '<section class="section" id="g' + gi + '"><div class="section-head">' +
        '<div class="section-title">' + esc(g.heading) + '</div>' +
        (hasFull ? '' : '<button class="listen-btn" data-g="' + gi + '">&#9654; Listen</button>') + '<button class="pace-btn" data-g="' + gi + '">&#9201; Pace</button></div>';
      var plate = plateFor(day, g.heading);
      if (plate) h += '<figure class="plate"><img src="' + plate + '" alt="" loading="lazy"></figure>';
      g.blocks.forEach(function (b) { h += blockHTML(b); });
      if (g.heading.indexOf('Startup case study') === 0 || g.heading.indexOf('Business teardown') === 0) h += lrTeaser(day);
      h += '</section>';
    });
    return h;
  }
  function ednavHTML(day) {
    return '<div class="ednav">' +
      '<a class="ednav-btn' + (day <= 1 ? ' disabled' : '') + '" href="#/edition/' + (day - 1) + '">&larr; ' + (day > 1 ? esc(D.meta[day - 1].short) : '') + '</a>' +
      '<a class="ednav-btn next' + (day >= D.today ? ' disabled' : '') + '" href="#/edition/' + (day + 1) + '">' + (day < D.today ? esc(D.meta[day + 1].short) : '') + ' &rarr;</a></div>';
  }
  function leadSplit(fact) {
    var t = String(fact || '').replace(/^Edition \d+\.\s*/, '');
    var m = t.match(/^(.+?[.!?])\s+(?=[A-Z])/);
    return m ? { head: m[1], deck: t.slice(m[0].length) } : { head: t, deck: '' };
  }
  function renderToday() {
    var ed = D.editions[D.today];
    var h = '<div class="wrap">' + mast('today') + tickerHTML(D.today) +
      '<div class="kicker">Today &middot; ' + esc(D.meta[D.today].date) + '</div>' +
      '<h1 class="h1">' + esc(leadSplit(ed.fact).head) + '</h1>' + (leadSplit(ed.fact).deck ? '<p class="deck">' + esc(leadSplit(ed.fact).deck) + '</p>' : '') +
      '<p class="intro">' + esc(ed.intro) + '</p>' +
      editionBody(D.today, true) + ednavHTML(D.today) +
      '<div class="footer"><span>The Morning Paper &middot; daily since 6 Oct 2026</span><span>Set in Fraunces &amp; Source Serif</span><a href="#" class="push-link" data-push="1" hidden></a></div></div>';
    app.innerHTML = h;
    pushRefresh();
    wirePlayers(app);
  }
  function renderArchive() {
    var h = '<div class="wrap">' + mast('archive') +
      '<div class="arch-title">The archive</div>' +
      '<div class="arch-sub">Every edition, complete. ' + D.today + ' days and counting.</div>';
    h += '<div class="arch-grid">';
    for (var n = D.today; n >= 1; n--) {
      var ed = D.editions[n];
      var thumb = ed.thumb || (ed.hero && ed.hero.img) || plateFor(n, 'Front page') || 'photos/concept-compounding.jpg';
      h += '<a class="arch-card" href="#/edition/' + n + '"><span class="arch-num">' + n + '</span>' +
        '<span class="arch-meta"><b>' + esc(D.meta[n].date) + (n === D.today ? ' &nbsp;<span class="arch-today-tag">Today</span>' : '') + '</b>' +
        '<span>' + esc(leadSplit(ed.fact).head) + '</span></span>' +
        '<img class="arch-thumb" src="' + thumb + '" alt="" loading="lazy"></a>';
    }
    h += '</div><div class="footer"><span>The Morning Paper</span><span>' + D.today + ' editions</span></div></div>';
    app.innerHTML = h;
  }
  function renderEdition(n) {
    var ed = D.editions[n];
    if (!ed) { renderArchive(); return; }
    var h = '<div class="wrap">' + mast('') +
      '<div class="kicker">Edition ' + n + ' &middot; ' + esc(D.meta[n].date) + '</div>' +
      '<h1 class="h1">' + esc(leadSplit(ed.fact).head) + '</h1>' + (leadSplit(ed.fact).deck ? '<p class="deck">' + esc(leadSplit(ed.fact).deck) + '</p>' : '') +
      '<p class="intro">' + esc(ed.intro) + '</p>' +
      editionBody(n, n === D.today) + ednavHTML(n) +
      '<div class="footer"><span>The Morning Paper</span><span><a href="#/archive">Full archive</a></span></div></div>';
    app.innerHTML = h;
    wirePlayers(app);
  }
  function renderLongreads() {
    var h = '<div class="wrap">' + mast('longreads') +
      '<div class="arch-title">The long reads</div>' +
      '<div class="arch-sub">One company, taken apart properly, every day.</div><div class="arch-grid">';
    for (var n = D.today; n >= 1; n--) {
      var lr = D.longreads[n];
      if (!lr) continue;
      var thumb = (lr.hero && lr.hero.img) || 'photos/concept-compounding.jpg';
      h += '<a class="lr-card" href="#/longread/' + n + '">' +
        '<img src="' + thumb + '" alt="" loading="lazy">' +
        '<span class="lr-card-meta"><span class="m">' + esc(D.meta[n].date) + (n === D.today ? ' &middot; Today' : '') + '</span>' +
        '<span class="t">' + esc(lr.title) + '</span>' +
        '<span class="d">' + esc(lr.fact) + '</span></span></a>';
    }
    h += '</div><div class="footer"><span>The Morning Paper &middot; long reads</span><span><a href="#/archive">Full archive</a></span></div></div>';
    app.innerHTML = h;
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
    if (D.audio && D.audio['lr' + n] && D.audio['lr' + n].full) {  // recorded read of the whole long read (no on-device voice)
      h += playerHTML('lr' + n, 'full', 'Listen to this long read', 'Recorded read, highlighted line by line', true);
    }
    lr.groups.forEach(function (g, gi) {
      h += '<section class="section"><div class="section-head"><div class="section-title">' + esc(g.heading) + '</div>' +
        '<button class="pace-btn" data-lg="' + gi + '">&#9201; Pace</button></div>';
      g.blocks.forEach(function (b) { h += blockHTML(b); });
      h += '</section>';
    });
    h += '<div class="ednav"><a class="ednav-btn" href="#/edition/' + n + '">&larr; Back to the edition</a></div>' +
      '<div class="footer"><span>The Morning Paper &middot; long reads</span></div></div>';
    app.innerHTML = h;
    wirePlayers(app);
  }


  /* ---------- cards: short news cards, newest first ---------- */
  var LANE_NAMES = { all: 'All', markets: 'Markets', insurance: 'Insurance', fintech: 'Fintech', ai: 'AI', startups: 'Startups' };
  var CARDS = { list: null, lane: 'all', i: 0, loading: false };
  function cardsCache() { try { return JSON.parse(localStorage.getItem('mp-cards') || 'null'); } catch (e) { return null; } }
  function seenSet() { try { return JSON.parse(localStorage.getItem('mp-seen') || '[]'); } catch (e) { return []; } }
  function markSeen(id) { var s = seenSet(); if (s.indexOf(id) < 0) { s.push(id); try { localStorage.setItem('mp-seen', JSON.stringify(s.slice(-300))); } catch (e) {} } }
  function cardTime(c) {
    var d = new Date(c.at || c.publishedAt); if (isNaN(d)) return '';
    var t = d.toLocaleTimeString('en-IN', { hour: 'numeric', minute: '2-digit', hour12: true, timeZone: 'Asia/Kolkata' });
    var day = d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'Asia/Kolkata' });
    var today = new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', timeZone: 'Asia/Kolkata' });
    return (day === today ? 'Today' : day) + ' &middot; ' + t.toUpperCase().replace(' ', '&nbsp;') + ' IST';
  }
  function filteredCards() {
    return (CARDS.list || []).filter(function (c) { return CARDS.lane === 'all' || c.lane === CARDS.lane; });
  }
  function sane(t) {
    t = String(t || '').trim(); if (!t || /[.!?)"'\u201D\u2019]$/.test(t)) return t;
    var m = t.match(/^[\s\S]*[.!?](?=\s|$)/); return m ? m[0] : '';
  }
  function cardHTML(c) {
    var tags = (c.tags || []).slice(0, 4).map(function (t) { return '<span class="ctag">' + esc(t) + '</span>'; }).join('');
    var src = (c.sources || []).map(function (x) { return '<a href="' + esc(x.url) + '" target="_blank" rel="noopener">' + esc(x.name) + '</a>'; }).join(' &middot; ');
    return '<section class="pg" data-id="' + esc(c.id) + '"><article class="pg-in">' +
      '<div class="ncard-k"><span>' + esc(c.kind || LANE_NAMES[c.lane] || 'Markets') + '</span><span class="ncard-t">' + (c.timeLabel ? esc(c.timeLabel) : cardTime(c)) + '</span></div>' +
      (c.image && c.image.src ? '<figure class="ncard-img"><img src="' + esc(c.image.src) + '" alt="" onerror="this.parentNode.classList.add(\'bad\')">' + (c.image.credit ? '<figcaption>' + esc(c.image.credit) + '</figcaption>' : '') + '</figure>' : '<figure class="ncard-img plate-ph lane-' + esc(c.lane || 'markets') + '"><div class="ph-t">' + esc((c.tags && c.tags[0]) || LANE_NAMES[c.lane] || '') + '</div><div class="ph-s">' + esc((c.tags || []).slice(1, 3).join(' · ')) + '</div></figure>') +
      '<h2 class="ncard-h">' + esc(c.headline) + '</h2>' +
      '<p class="ncard-b">' + esc(sane(c.body)) + '</p>' +
      (sane(c.why) ? '<div class="ncard-why"><b>Why it matters</b><span>' + esc(sane(c.why)) + '</span></div>' : '') +
      '<div class="ncard-foot">' + (tags ? '<div class="ncard-tags">' + tags + '</div>' : '') +
      '<div class="ncard-src">Source: ' + src + (sane(c.watch) ? ' &middot; <button class="more-btn" data-act="more">What could change this</button>' : '') + '</div></div>' +
      '</article></section>';
  }
  function endHTML() {
    return '<section class="pg"><div class="pg-in cards-end"><div class="cards-end-k">Caught up</div><div class="cards-end-h">You\'re caught up.</div><p id="end-note">Nothing newer is waiting.</p><button class="cbtn" data-act="first">Back to the newest</button></div></section>';
  }
  function fitPanels() {
    var ins = document.querySelectorAll('.pg-in');
    for (var k = 0; k < ins.length; k++) {
      var el = ins[k]; el.classList.remove('noimg');
      var hasImg = !!el.querySelector('.ncard-img');
      var st = { bs: 17, hs: 28, ih: 0 };
      function ap() { el.style.setProperty('--bs', st.bs + 'px'); el.style.setProperty('--hs', st.hs + 'px'); if (st.ih) el.style.setProperty('--ih', st.ih + 'px'); else el.style.removeProperty('--ih'); }
      ap();
      var guard = 0;
      while (el.scrollHeight > el.clientHeight + 1 && guard++ < 80) {
        if (st.bs > 15.5) st.bs -= 0.5;
        else if (hasImg && (st.ih || 150) > 100) st.ih = (st.ih || 150) - 10;
        else if (st.bs > 14) st.bs -= 0.5;
        else if (st.hs > 22) st.hs -= 1;
        else if (hasImg && !el.classList.contains('noimg')) el.classList.add('noimg');
        else break;
        ap();
      }
    }
  }
  function renderCardsView() {
    var list = filteredCards(), n = list.length;
    document.documentElement.classList.add('cards-fs');
    var lanes = ['all', 'markets', 'insurance', 'fintech', 'ai', 'startups'].map(function (l) {
      return '<button class="lane' + (CARDS.lane === l ? ' on' : '') + '" data-lane="' + l + '">' + LANE_NAMES[l] + '</button>';
    }).join('');
    var panels;
    if (CARDS.list === null) panels = '<section class="pg"><div class="pg-in cards-empty">Loading cards...</div></section>';
    else if (!n) panels = '<section class="pg"><div class="pg-in cards-empty">' + (CARDS.list.length ? 'No cards in this lane yet.' : 'No cards yet. They appear here as the day\'s news lands.') + '</div></section>';
    else panels = list.map(cardHTML).join('') + endHTML();
    app.innerHTML = '<div class="cfs">' +
      '<div class="cfs-top"><a class="cfs-home" href="#/" aria-label="Back to the paper">&larr; Paper</a><div class="lanes">' + lanes + '</div><button class="cfs-gear" data-act="gear" aria-label="Card settings">&#9881;</button></div>' +
      '<div class="cfs-set" id="cfs-set" hidden><label><input type="checkbox" id="quiet-toggle"' + (quietPref() ? ' checked' : '') + '> Quiet hours <span>11 PM to 7 AM IST, no pushes</span></label><a href="#" class="push-link" data-push="1" hidden></a></div>' +
      '<div class="pager" id="pager"><div class="track" id="track">' + panels + '</div></div>' +
      '<div class="cfs-arrows"><span class="cards-pos" id="cpos"></span><button class="arw" data-act="prev" aria-label="Previous card"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M5 15l7-7 7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button><button class="arw" data-act="next" aria-label="Next card"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M5 9l7 7 7-7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button></div>' +
      '<div class="cfs-sheet" id="cfs-sheet" hidden><div class="cfs-sheet-in"><b>What could change this</b><p id="cfs-sheet-p"></p><button class="cbtn" data-act="closemore">Close</button></div></div></div>';
    pushRefresh();
    updateCardsDot();
    CARDS.i = Math.max(0, Math.min(n ? n : 0, CARDS.i));
    alertsNote();
    fitPanels();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitPanels);
    applyTrack(false);
    var c = list[CARDS.i]; if (c) markSeen(c.id);
  }
  function alertsNote() {
    var el = document.getElementById('end-note'); if (!el) return;
    function set(on) { el.textContent = on ? 'Nothing newer is waiting. A push will tell you when the next card lands.' : 'Nothing newer is waiting. Alerts are off. Tap the gear to turn them on and get a push for new cards.'; }
    set(false);
    if (!pushSupported() || (window.Notification && Notification.permission !== 'granted')) return;
    navigator.serviceWorker.ready.then(function (reg) { return reg.pushManager.getSubscription(); }).then(function (s) { set(!!s); }).catch(function () {});
  }
  function pagerH() { var p = document.getElementById('pager'); return p ? p.clientHeight : 0; }
  function lastIdx() { var n = filteredCards().length; return n ? n : 0; }
  function applyTrack(anim, extra) {
    var tr = document.getElementById('track'); if (!tr) return;
    tr.style.transition = anim ? 'transform .34s cubic-bezier(.22,.8,.24,1)' : 'none';
    tr.style.transform = 'translate3d(0,' + (-CARDS.i * pagerH() + (extra || 0)) + 'px,0)';
    var n = filteredCards().length, pos = document.getElementById('cpos');
    if (pos) pos.textContent = n ? (CARDS.i >= n ? 'end' : (CARDS.i + 1) + ' / ' + n) : '';
    var arr = document.querySelectorAll('.arw');
    if (arr.length) { arr[0].disabled = CARDS.i <= 0; arr[1].disabled = CARDS.i >= lastIdx(); }
  }
  function goTo(i) {
    var n = filteredCards().length; CARDS.i = Math.max(0, Math.min(lastIdx(), i)); applyTrack(true);
    var c = filteredCards()[CARDS.i]; if (c) { markSeen(c.id); updateCardsDot(); if (history.replaceState) history.replaceState(null, '', '#/cards/' + c.id); }
    else if (n && history.replaceState) history.replaceState(null, '', '#/cards');
  }
  function cardStep(d) { goTo(CARDS.i + d); }
  function updateCardsDot() {
    var d = document.getElementById('cards-dot'); if (!d || !CARDS.list) return;
    var seen = seenSet(); d.hidden = !CARDS.list.some(function (c) { return seen.indexOf(c.id) < 0; });
  }
  function loadCards(cb) {
    var cached = cardsCache(); if (cached && CARDS.list === null) CARDS.list = cached;
    fetch('api/cards', { cache: 'no-store' }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (j) {
      CARDS.list = j.cards || []; try { localStorage.setItem('mp-cards', JSON.stringify(CARDS.list)); } catch (e) {}
      cb(true);
    }).catch(function () { if (CARDS.list === null) CARDS.list = []; cb(false); });
  }
  function renderCards(id) {
    var first = CARDS.list === null;
    if (first) { var cc = cardsCache(); if (cc) { CARDS.list = cc; first = false; } }
    function place() {
      if (id) { var l = (CARDS.list || []); var ix = l.findIndex(function (c) { return c.id === id; }); CARDS.lane = 'all'; CARDS.i = ix >= 0 ? ix : 0; }
    }
    place(); renderCardsView();
    var sig0 = JSON.stringify((CARDS.list || []).map(function (c) { return c.id; }));
    loadCards(function () {
      if (location.hash.indexOf('#/cards') !== 0) return;
      var sig1 = JSON.stringify((CARDS.list || []).map(function (c) { return c.id; }));
      if (sig1 === sig0) return;
      var cur = filteredCards()[CARDS.i]; if (id) place(); else if (cur) { var ix2 = filteredCards().findIndex(function (c) { return c.id === cur.id; }); if (ix2 >= 0) CARDS.i = ix2; }
      renderCardsView();
    });
  }
  function closeSheet() { var s = document.getElementById('cfs-sheet'); if (s) s.hidden = true; }
  document.addEventListener('click', function (e) {
    var l = e.target.closest && e.target.closest('.lane');
    if (l) { CARDS.lane = l.getAttribute('data-lane'); CARDS.i = 0; renderCardsView(); return; }
    var b = e.target.closest && e.target.closest('[data-act]');
    if (!b || b.disabled) return;
    var a = b.getAttribute('data-act');
    if (a === 'next') cardStep(1); else if (a === 'prev') cardStep(-1); else if (a === 'first') goTo(0);
    else if (a === 'gear') { var g = document.getElementById('cfs-set'); if (g) g.hidden = !g.hidden; }
    else if (a === 'more') { var c = filteredCards()[CARDS.i]; var s = document.getElementById('cfs-sheet'); if (c && s) { document.getElementById('cfs-sheet-p').textContent = sane(c.watch); s.hidden = false; } }
    else if (a === 'closemore') closeSheet();
  });
  document.addEventListener('click', function (e) { if (e.target && e.target.id === 'cfs-sheet') closeSheet(); });
  document.addEventListener('change', function (e) {
    if (e.target && e.target.id === 'quiet-toggle') {
      try { localStorage.setItem('mp-quiet', e.target.checked ? '1' : '0'); } catch (x) {}
      if (pushSupported()) navigator.serviceWorker.ready.then(function (reg) { return reg.pushManager.getSubscription(); }).then(function (sub) {
        if (sub) fetch('api/subscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: pushBody(sub) });
      }).catch(function () {});
    }
  });
  (function () {
    var st = null;
    function inPager(t) { var p = document.getElementById('pager'); return p && p.contains(t); }
    document.addEventListener('touchstart', function (e) {
      if (!inPager(e.target) || e.touches.length !== 1) { st = null; return; }
      var t = e.touches[0]; st = { y: t.clientY, x: t.clientX, t: Date.now(), dy: 0, mode: null };
      var tr = document.getElementById('track'); if (tr) tr.style.transition = 'none';
    }, { passive: true });
    document.addEventListener('touchmove', function (e) {
      if (!st) return;
      var t = e.touches[0], dy = t.clientY - st.y, dx = t.clientX - st.x;
      if (!st.mode) { if (Math.abs(dy) < 6 && Math.abs(dx) < 6) return; st.mode = Math.abs(dy) >= Math.abs(dx) ? 'v' : 'h'; }
      if (st.mode !== 'v') return;
      if (e.cancelable) e.preventDefault();
      var off = dy; if ((CARDS.i <= 0 && dy > 0) || (CARDS.i >= lastIdx() && dy < 0)) off = dy * 0.28;
      st.dy = dy; applyTrack(false, off);
    }, { passive: false });
    function end() {
      if (!st) return; var s = st; st = null;
      if (s.mode !== 'v') return;
      var H = pagerH() || 700, v = s.dy / Math.max(1, Date.now() - s.t), d = 0;
      if (s.dy < -H * 0.14 || v < -0.4) d = 1; else if (s.dy > H * 0.14 || v > 0.4) d = -1;
      goTo(CARDS.i + d);
    }
    document.addEventListener('touchend', end, { passive: true });
    document.addEventListener('touchcancel', end, { passive: true });
    var wl = 0;
    document.addEventListener('wheel', function (e) {
      if (!inPager(e.target) || Math.abs(e.deltaY) < 12 || Date.now() - wl < 520) return;
      wl = Date.now(); e.preventDefault(); cardStep(e.deltaY > 0 ? 1 : -1);
    }, { passive: false });
    document.addEventListener('keydown', function (e) {
      if (!document.getElementById('pager')) return;
      if (e.key === 'ArrowDown' || e.key === 'PageDown') { e.preventDefault(); cardStep(1); } else if (e.key === 'ArrowUp' || e.key === 'PageUp') { e.preventDefault(); cardStep(-1); }
    });
    window.addEventListener('resize', function () { if (document.getElementById('pager')) { fitPanels(); applyTrack(false); } });
  })();
  function cardsDotBoot() { loadCards(function () { updateCardsDot(); }); }
  cardsDotBoot();

  /* ---------- router ---------- */
  function route() {
    document.documentElement.classList.remove('cards-fs');
    stopReader();
    root_pausePlayers();  // also leaves audio mode and clears the old page's highlight
    HL.items = []; HL.ready = false; HL.pending = false; HL.failed = false;
    stopPacer(true);
    var hash = location.hash.replace(/^#\/?/, '');
    var m;
    if (!hash || hash === 'today') renderToday();
    else if (hash === 'archive') renderArchive();
    else if (hash === 'longreads') renderLongreads();
    else if ((m = hash.match(/^cards(?:\/(c[a-z0-9]+))?$/))) renderCards(m[1] || null);
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
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.pace-btn');
    if (!btn) return;
    var sec = btn.closest('.section');
    var label = sec.querySelector('.section-title').textContent;
    var secs = Array.prototype.slice.call(document.querySelectorAll('.section'));
    secs = secs.slice(secs.indexOf(sec));
    btn.classList.add('active');
    startPacer(secs, label, 0);
  });
  (function () {
    try {
      var q = new URLSearchParams(location.search).get('c');
      if (q && /^c[a-z0-9]+$/.test(q)) { history.replaceState(null, '', location.pathname + '#/cards/' + q); }
    } catch (x) {}
  })();
  route();

  /* Web Push: one tap to turn alerts on (iOS needs the Home Screen app and a tap). */
  function pushSupported() { return 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window; }
  function pushLinks() { return document.querySelectorAll('[data-push]'); }
  function pushSet(txt, off) { pushLinks().forEach(function (a) { a.hidden = false; a.textContent = txt; a.style.opacity = off ? '.6' : ''; }); }
  function pushRefresh() {
    if (!pushSupported()) { var standalone = window.navigator.standalone === false && /iPhone|iPad/.test(navigator.userAgent); if (standalone) pushSet('Add to Home Screen for alerts', true); return; }
    if (Notification.permission === 'denied') { pushSet('Alerts blocked in settings', true); return; }
    navigator.serviceWorker.ready.then(function (reg) { return reg.pushManager.getSubscription(); }).then(function (sub) {
      pushSet(sub && Notification.permission === 'granted' ? 'Alerts on' : 'Turn on alerts', !!sub);
    }).catch(function () {});
  }
  function quietPref() { try { return localStorage.getItem('mp-quiet') === '1'; } catch (e) { return false; } }
  function pushBody(sub) { return JSON.stringify({ subscription: sub.toJSON(), quiet: quietPref() }); }
  function b64u(s) { var p = '='.repeat((4 - s.length % 4) % 4), b = (s + p).replace(/-/g, '+').replace(/_/g, '/'), r = atob(b), o = new Uint8Array(r.length); for (var i = 0; i < r.length; i++) o[i] = r.charCodeAt(i); return o; }
  function pushToggle() {
    pushSet('Working...', true);
    navigator.serviceWorker.ready.then(function (reg) {
      return reg.pushManager.getSubscription().then(function (sub) {
        if (sub) { return fetch('api/subscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: pushBody(sub) }).then(function () { pushSet('Alerts on', true); }); }
        return Notification.requestPermission().then(function (perm) {
          if (perm !== 'granted') { pushRefresh(); return; }
          return fetch('api/vapid').then(function (r) { return r.json(); }).then(function (k) {
            return reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64u(k.publicKey) });
          }).then(function (sub2) {
            return fetch('api/subscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: pushBody(sub2) });
          }).then(function (r) { if (!r.ok) throw new Error('save'); pushSet('Alerts on', true); });
        });
      });
    }).catch(function () { pushSet('Could not turn on alerts, tap to retry', false); });
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-push]');
    if (!a) return; e.preventDefault(); if (pushSupported()) pushToggle();
  });
  if ('serviceWorker' in navigator) navigator.serviceWorker.addEventListener('message', function (e) { if (e.data && e.data.type === 'nav' && e.data.url) { try { var u = new URL(e.data.url); if (u.origin === location.origin) { var cq = u.searchParams.get('c'); location.hash = cq ? '#/cards/' + cq : (u.hash || '#/'); } } catch (x) {} } });
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () { navigator.serviceWorker.register('sw.js').catch(function () {}); });
  }
})();

