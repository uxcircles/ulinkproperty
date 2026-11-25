/* ULINK concept: menu, fee calculator (price tags), enquiry form (mailto), lazy map. */
(() => {
  const zh = document.documentElement.lang.startsWith('zh');
  const T = zh ? {
    menu: '選單', close: '關閉',
    let: [['搵租客', '一次過'], ['管理費', '每月 12%'], ['第一年你袋', '12 個月租金減收費']],
    bnb: [['每月房租收入', '未計清潔費'], ['管家 15% + VAT', '每月'], ['每月你袋', '未計清潔費及雜費']],
    buy: [['買樓服務 1%', '成交後付'], ['睇樓報告', '每間，睇完先俾'], ['樓價', '港幣約']],
    approx: '約', subject: '查詢', name: '姓名', reach: '聯絡方法', svc: '服務', msg: '訊息',
  } : {
    menu: 'Menu', close: 'Close',
    let: [['Tenant find', 'one-off'], ['Management', '12% a month'], ['You keep, year one', '12 months’ rent less fees']],
    bnb: [['Bookings a month', 'before cleaning'], ['Fee 15% + VAT', 'a month'], ['You keep a month', 'before cleaning and bills']],
    buy: [['Buying fee 1%', 'paid on completion'], ['Viewing report', 'each, after the viewing'], ['Property price', 'in Hong Kong dollars']],
    approx: 'about', subject: 'Enquiry', name: 'Name', reach: 'Reply to', svc: 'Service', msg: 'Message',
  };

  // menu
  const btn = document.querySelector('.menu-btn');
  const menu = document.getElementById('menu');
  if (btn && menu) {
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open);
      menu.hidden = !open;
      btn.textContent = open ? T.close : T.menu;
      document.documentElement.classList.toggle('menu-open', open);
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !menu.hidden) { btn.click(); btn.focus(); } });
    menu.addEventListener('click', (e) => { if (e.target.closest('a')) { btn.click(); } });
  }

  // fee calculator: fees as published on ulinkproperty.co.uk/service and /why-choose-us
  const out = document.getElementById('c-out');
  if (out) {
    const $ = (id) => document.getElementById(id);
    const num = (id) => Math.max(0, parseFloat($(id).value) || 0);
    const gbp = (n) => '£' + Math.round(n).toLocaleString('en-GB');
    const hkd = (n) => 'HK$' + Math.round(n).toLocaleString('en-GB');
    const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const tag = (label, price, note, red) => `<div class="tag${red ? ' tag-red' : ''}"><span class="tag-hole" aria-hidden="true"></span><span class="tag-label">${esc(label)}</span><b class="tag-price">${esc(price)}</b><span class="tag-hk">${esc(note)}</span></div>`;
    const mode = () => document.querySelector('input[name=mode]:checked').value;
    const run = () => {
      const m = mode();
      document.querySelectorAll('.f[data-for]').forEach((f) => { f.hidden = f.dataset.for !== m; });
      const rate = num('c-rate') || 10.4;
      const L = T[m];
      let rows;
      if (m === 'let') {
        const rent = num('c-rent');
        const find = rent, mgmt = rent * 0.12, keep = rent * 12 - find - mgmt * 12;
        rows = [[L[0][0], gbp(find), hkd(find * rate)], [L[1][0], gbp(mgmt), hkd(mgmt * rate)], [L[2][0], gbp(keep), `${T.approx} ${hkd(keep * rate)}`, 1]];
      } else if (m === 'bnb') {
        const gross = num('c-night') * Math.min(31, num('c-nights'));
        const fee = gross * 0.15 * 1.2, keep = gross - fee;
        rows = [[L[0][0], gbp(gross), hkd(gross * rate)], [L[1][0], gbp(fee), hkd(fee * rate)], [L[2][0], gbp(keep), `${T.approx} ${hkd(keep * rate)}`, 1]];
      } else {
        const price = num('c-price');
        rows = [[L[0][0], gbp(price * 0.01), hkd(price * 0.01 * rate), 1], [L[1][0], 'HK$450', L[1][1]], [L[2][0], gbp(price), `${L[2][1]} ${hkd(price * rate)}`]];
      }
      out.innerHTML = rows.map((r) => tag(r[0], r[1], r[2], r[3])).join('');
    };
    document.querySelectorAll('#calc input').forEach((i) => i.addEventListener('input', run));
    run();
  }

  // enquiry form -> mailto (nothing stored)
  const form = document.getElementById('ask');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const err = document.getElementById('f-err');
      let ok = true;
      ['name', 'reach'].forEach((k) => {
        const bad = !form[k].value.trim();
        form[k].setAttribute('aria-invalid', bad);
        if (bad && ok) { form[k].focus(); ok = false; }
      });
      err.hidden = ok;
      if (!ok) return;
      const body = [`${T.name}: ${form.name.value.trim()}`, `${T.reach}: ${form.reach.value.trim()}`, `${T.svc}: ${form.svc.value}`, form.msg.value.trim() ? `\n${T.msg}:\n${form.msg.value.trim()}` : ''].filter(Boolean).join('\n');
      location.href = `mailto:info@ulinkproperty.co.uk?subject=${encodeURIComponent(`${T.subject}: ${form.svc.value}`)}&body=${encodeURIComponent(body)}`;
    });
  }

  // map: load MapLibre only when it scrolls near
  const box = document.querySelector('[data-map]');
  if (box && 'IntersectionObserver' in window) {
    const root = document.querySelector('link[rel=stylesheet][href*="assets/site.css"]').getAttribute('href').split('assets/')[0];
    const load = () => {
      const css = document.createElement('link'); css.rel = 'stylesheet'; css.href = root + 'assets/vendor/maplibre/maplibre-gl.css'; document.head.appendChild(css);
      const s1 = document.createElement('script'); s1.src = root + 'assets/vendor/maplibre/maplibre-gl.js';
      s1.onload = () => {
        const s2 = document.createElement('script'); s2.src = root + 'assets/map.js?v=1';
        s2.onload = () => { try { const map = window.ulMap(box, root); map.on('load', () => { box.querySelector('.map-fallback').style.visibility = 'hidden'; }); } catch (e) { /* keep the sketch */ } };
        document.head.appendChild(s2);
      };
      document.head.appendChild(s1);
    };
    const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { io.disconnect(); load(); } }, { rootMargin: '400px' });
    io.observe(box);
  }
})();
