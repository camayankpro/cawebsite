/* Base path: pages inside articles/ need ../ before shared files */
var TX_BASE = (function () {
  // Count folders below the site root. Pages live in articles/, main/ or services/
  // (and articles/<group>/), so count from the first known folder name.
  var dirs = window.location.pathname.split('/').slice(0, -1);
  var idx = -1;
  for (var i = 0; i < dirs.length; i++) {
    if (['articles', 'main', 'services'].indexOf(dirs[i]) >= 0) { idx = i; break; }
  }
  return idx >= 0 ? new Array(dirs.length - idx + 1).join('../') : '';
})();
/* ── TAXAMC SHARED ICONS: edit icons here; every page updates ── */
(function () {
  var ICONS = {
  "ic-money": "<path d=\"M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1\"/><path d=\"M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4\"/>",
  "ic-clipboard": "<rect width=\"8\" height=\"4\" x=\"8\" y=\"2\" rx=\"1\"/><path d=\"M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2\"/><path d=\"M12 11h4M12 16h4M8 11h.01M8 16h.01\"/>",
  "ic-building": "<path d=\"M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z\"/><path d=\"M6 12H4a2 2 0 0 0-2 2v8h4M18 9h2a2 2 0 0 1 2 2v11h-4\"/><path d=\"M10 6h4M10 10h4M10 14h4M10 18h4\"/>",
  "ic-folder": "<path d=\"M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z\"/>",
  "ic-book": "<path d=\"M12 7v14\"/><path d=\"M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z\"/>",
  "ic-scale": "<path d=\"M12 3v18M7 21h10M3 7h1a17 17 0 0 0 8-2 17 17 0 0 0 8 2h1\"/><path d=\"m5 8 3 8a5 5 0 0 1-6 0zM19 8l3 8a5 5 0 0 1-6 0z\"/>",
  "ic-chart": "<path d=\"M3 3v16a2 2 0 0 0 2 2h16\"/><path d=\"M18 17V9M13 17V5M8 17v-3\"/>",
  "ic-search": "<circle cx=\"11\" cy=\"11\" r=\"8\"/><path d=\"m21 21-4.3-4.3\"/>",
  "ic-card": "<rect width=\"20\" height=\"14\" x=\"2\" y=\"5\" rx=\"2\"/><path d=\"M2 10h20\"/>",
  "ic-package": "<path d=\"m16.5 9.4-9-5.19M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z\"/><path d=\"M3.3 7 12 12l8.7-5M12 22V12\"/>",
  "ic-cart": "<circle cx=\"8\" cy=\"21\" r=\"1\"/><circle cx=\"19\" cy=\"21\" r=\"1\"/><path d=\"M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12\"/>",
  "ic-phone": "<path d=\"M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z\"/>"
  };
  var sprite = '<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">' +
    '<g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">';
  Object.keys(ICONS).forEach(function (k) {
    sprite += '<symbol id="' + k + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' + ICONS[k] + '</symbol>';
  });
  sprite += '</g></svg>';
  function insert() { document.body.insertAdjacentHTML('afterbegin', sprite); }
  if (document.body) insert(); else document.addEventListener('DOMContentLoaded', insert);
})();

/* ── GA4 — Google Analytics 4 ───────────────────────────────
   Measurement ID: G-DNF0748CLY
   Tracks: page views + WhatsApp clicks (as 'whatsapp_click' event)
   ─────────────────────────────────────────────────────────── */
(function () {
  // Skip analytics when this page is shown inside the theme selector preview
  if (window.top !== window.self) return;
  var GA_ID = 'G-DNF0748CLY';

  // Inject gtag.js
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);

  // Init
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', GA_ID);

  // Track every WhatsApp link click as a Lead event
  document.addEventListener('click', function (e) {
    var el = e.target.closest('a[href*="wa.me"]');
    if (!el) return;
    var page = window.location.pathname.split('/').pop() || 'index.html';
    gtag('event', 'whatsapp_click', {
      event_category: 'Lead',
      event_label: page,
      page_location: window.location.href
    });
  });
})();

// Auto-inject missing SEO meta tags
(function() {
  if (!document.querySelector('meta[name="language"]')) {
    var m = document.createElement('meta');
    m.setAttribute('http-equiv', 'content-language');
    m.setAttribute('content', 'en-IN');
    document.head.appendChild(m);
  }
})();

/* ============================================================
   common.js — Agarwal Mayank & Company
   Place just before </body>. Injects navbar, WA float, footer,
   popup. Exposes initPopup(), cep(), sep().
   ============================================================ */

(function () {

  /* ── NAVBAR ─────────────────────────────────────────────── */
  var NAV_HTML =
    '<nav class="navbar">' +
      '<div class="navbar-content">' +
        '<a href="' + TX_BASE + 'index.html" class="navbar-brand">' +
          '<img src="' + TX_BASE + 'assets/logo.webp" alt="CA India Logo" class="ca-logo">' +
          '<div class="navbar-text">' +
            '<div class="navbar-logo" style="color:var(--primary);">Agarwal Mayank <span style="color:var(--accent);">&amp; Company</span></div>' +
            '<div class="navbar-subtitle">Takes your business as seriously as you do</div>' +
          '</div>' +
        '</a>' +
        '<ul class="nav-links" id="navLinks">' +
          '<li><a href="' + TX_BASE + 'index.html">Home</a></li>' +
          '<li><a href="' + TX_BASE + 'index.html#about">About</a></li>' +
          '<li><a href="' + TX_BASE + 'index.html#services">Services</a></li>' +
          '<li><a href="' + TX_BASE + 'main/articles.html" class="nav-articles-link">Articles</a></li>' +
          '<li><a href="' + TX_BASE + 'index.html#contact">Contact Us</a></li>' +
        '</ul>' +
        '<div class="burger-menu" id="burgerMenu"><span></span><span></span><span></span></div>' +
      '</div>' +
    '</nav>';

  var navEl = document.getElementById('site-nav');
  if (navEl) navEl.outerHTML = NAV_HTML;

  /* ── CONTACT CLUSTER (WhatsApp + Call + Email) ──────────── */
  var CLUSTER_CSS =
    '<style>' +
    '.contact-cluster{position:fixed;bottom:28px;right:28px;display:flex;flex-direction:column;gap:12px;z-index:999}' +
    '.contact-cluster a{width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;text-decoration:none;box-shadow:0 4px 12px rgba(0,0,0,.25);transition:transform .2s,box-shadow .2s}' +
    '.contact-cluster a:hover{transform:scale(1.12);box-shadow:0 6px 20px rgba(0,0,0,.35)}' +
    '.contact-cluster a svg{width:26px;height:26px;fill:#fff}' +
    '.cc-wa{background:#25D366}.cc-call{background:var(--primary)}.cc-mail{background:var(--accent)}' +
    '@media(max-width:600px){.contact-cluster{bottom:16px;right:16px;gap:10px}.contact-cluster a{width:48px;height:48px}.contact-cluster a svg{width:22px;height:22px}}' +
    '</style>';
  document.head.insertAdjacentHTML('beforeend', CLUSTER_CSS);

  var CLUSTER_HTML =
    '<div class="contact-cluster">' +
      '<a href="https://wa.me/919045222870?text=Hello!%20I%20need%20CA%20services" class="cc-wa" target="_blank" title="WhatsApp Us">' +
        '<svg viewBox="0 0 32 32"><path d="M16 0C7.163 0 0 7.163 0 16c0 2.825.737 5.607 2.137 8.048L0 32l7.933-2.127A15.93 15.93 0 0016 32c8.837 0 16-7.163 16-16S24.837 0 16 0zm0 29.467a13.43 13.43 0 01-7.07-1.87l-.507-.292-5.245 1.407 1.417-5.26-.321-.523A13.43 13.43 0 012.5 16C2.5 8.556 8.556 2.5 16 2.5S29.5 8.556 29.5 16 23.444 29.467 16 29.467zm7.803-10.192c-.297-.149-1.757-.867-2.03-.967-.272-.099-.47-.149-.669.148s-.768.967-.941 1.166c-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059s-.018-.458.13-.606c.134-.133.297-.347.446-.521s.198-.297.297-.495c.099-.198.05-.372-.025-.521s-.669-1.611-.916-2.206c-.242-.579-.487-.5-.669-.51-.173-.008-.372-.01-.571-.01s-.52.074-.793.372c-.272.297-1.04 1.016-1.04 2.479s1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.757-.719 2.006-1.413.248-.694.248-1.289.173-1.413s-.272-.198-.571-.347z"/></svg>' +
      '</a>' +
      '<a href="tel:+919045222870" class="cc-call" title="Call Us">' +
        '<svg viewBox="0 0 24 24"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C9.4 21 3 14.6 3 7c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1L6.6 10.8z"/></svg>' +
      '</a>' +
      '<a href="mailto:contact@taxamc.com?subject=CA%20Services%20Enquiry&body=Hello%2C%0A%0AI%20am%20interested%20in%20your%20CA%20services.%0A%0AMy%20contact%20number%20is%20____" class="cc-mail" title="Email Us">' +
        '<svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>' +
      '</a>' +
    '</div>';
  document.body.insertAdjacentHTML('afterbegin', CLUSTER_HTML);

  /* ── FOOTER ─────────────────────────────────────────────── */
  var FOOTER_HTML =
    '<footer class="footer">' +
      '<div class="footer-content">' +
        '<div class="footer-section">' +
          '<h3>Agarwal Mayank &amp; Company</h3>' +
          '<p><strong>Chartered Accountants</strong></p>' +
          '<p style="margin-top:15px;">Providing comprehensive financial services across India digitally with expertise in taxation, audit, and business advisory.</p>' +
        '</div>' +
        '<div class="footer-section">' +
          '<h3>Quick Links</h3>' +
          '<a href="' + TX_BASE + 'index.html">Home</a>' +
          '<a href="' + TX_BASE + 'index.html#about">About Us</a>' +
          '<a href="' + TX_BASE + 'index.html#services">Services</a>' +
          '<a href="' + TX_BASE + 'main/articles.html">Articles</a>' +
          '<a href="' + TX_BASE + 'index.html#contact">Contact Us</a>' +
          '<a href="' + TX_BASE + 'main/disclaimer.html">Disclaimer</a>' +
          '<a href="' + TX_BASE + 'main/sitemap.html">Sitemap</a>' +
        '</div>' +
        '<div class="footer-section">' +
          '<h3>Contact Us</h3>' +
          '<p style="line-height:1.8;"><strong>&#128205; Office Address:</strong><br>1097, Surya Vihar, Delhi Road<br>Hapur - 245101, Uttar Pradesh</p>' +
          '<a href="https://www.google.com/maps?client=opera&oe=UTF-8&um=1&ie=UTF-8&fb=1&gl=in&sa=X&geocode=KdfbVE6lhQw5MaPv3FjSHS9d&daddr=1097,+Surya+Vihar,+Delhi+-+Meerut+Expy,+Hapur,+Uttar+Pradesh+245101" ' +
             'target="_blank" class="map-btn">' +
             '&#128205; View on Google Maps</a>' +
          '<p><strong>&#9990;&#65039; Phone:</strong> <a href="tel:+919045222870" style="color:rgba(255,255,255,0.9);text-decoration:underline;">+91-9045222870</a></p>' +
          '<p><strong>&#9993;&#65039; Email:</strong> <a href="#" id="emailLink" style="color:rgba(255,255,255,0.9);text-decoration:underline;"></a></p>' +
          '<p><strong>&#127757; Service Area:</strong> Serving India digitally</p>' +
        '</div>' +
      '</div>' +
      '<div class="footer-bottom">' +
        '<p>Copyright &copy; 2026 Agarwal Mayank &amp; Company | Chartered Accountants | All Rights Reserved. | <a href="' + TX_BASE + 'main/disclaimer.html" style="color:rgba(255,255,255,0.7);text-decoration:underline;">Disclaimer</a></p>' +
      '</div>' +
    '</footer>';

  var ftEl = document.getElementById('site-footer');
  if (ftEl) ftEl.outerHTML = FOOTER_HTML;

  /* ── POPUP HTML ─────────────────────────────────────────── */
  var POPUP_HTML =
    '<div id="ep" style="display:none;position:fixed;inset:0;background:rgba(var(--primary-rgb),0.88);z-index:9999;align-items:center;justify-content:center;">' +
      '<div style="background:white;border-radius:16px;max-width:360px;width:90%;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.35);position:relative;">' +
        '<button onclick="cep()" style="position:absolute;top:10px;right:14px;background:none;border:none;color:rgba(255,255,255,0.7);font-size:1.4rem;cursor:pointer;z-index:1;">&#x2715;</button>' +
        '<div id="ep-hd" style="background:linear-gradient(135deg,var(--primary),var(--primary-dark));padding:26px 26px 20px;text-align:center;"></div>' +
        '<div style="padding:20px 24px 22px;">' +
          '<input type="text" id="en" placeholder="Your Name" ' +
            'style="width:100%;padding:10px 13px;border:1.5px solid #e0e0e0;border-radius:8px;font-family:\'Poppins\',sans-serif;font-size:0.86rem;margin-bottom:10px;outline:none;display:block;box-sizing:border-box;" ' +
            'onfocus="this.style.borderColor=\'var(--primary)\'" onblur="this.style.borderColor=\'#e0e0e0\'">' +
          '<input type="tel" id="ep2" placeholder="Mobile Number" ' +
            'style="width:100%;padding:10px 13px;border:1.5px solid #e0e0e0;border-radius:8px;font-family:\'Poppins\',sans-serif;font-size:0.86rem;margin-bottom:12px;outline:none;display:block;box-sizing:border-box;" ' +
            'onfocus="this.style.borderColor=\'var(--primary)\'" onblur="this.style.borderColor=\'#e0e0e0\'">' +
          '<button onclick="sep()" style="width:100%;background:var(--accent);color:white;padding:12px;border:none;border-radius:8px;font-size:0.9rem;font-weight:700;cursor:pointer;font-family:\'Poppins\',sans-serif;">&#x1F4E9; Contact Us on WhatsApp</button>' +
          '<p style="text-align:center;margin-top:8px;font-size:0.7rem;color:#aaa;font-family:\'Poppins\',sans-serif;">Our CA team will get back to you shortly.</p>' +
        '</div>' +
      '</div>' +
    '</div>';
  document.body.insertAdjacentHTML('beforeend', POPUP_HTML);

  /* ── BURGER MENU ────────────────────────────────────────── */
  var burger = document.getElementById('burgerMenu');
  if (burger && document.getElementById('site-nav')) {
    burger.addEventListener('click', function () {
      this.classList.toggle('active');
      document.getElementById('navLinks').classList.toggle('active');
    });
  }

  /* ── AUTO-HIGHLIGHT ACTIVE NAV LINK ──────────────────────── */
  var page = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href === page || (page === '' && href === 'index.html')) {
      a.classList.add('nav-active');
    }
  });

  /* ── EMAIL PROTECTION ────────────────────────────────────── */
  var emailEl = document.getElementById('emailLink');
  if (emailEl) {
    var u = 'contact', d = 'taxamc', t = 'com';
    emailEl.href = 'mailto:' + u + '@' + d + '.' + t;
    emailEl.textContent = u + '@' + d + '.' + t;
  }

  /* ── POPUP LOGIC ─────────────────────────────────────────── */
  var _shown = false, _engaged = false, _pmsg = 'I need CA assistance.';

  window.initPopup = function (icon, title, msg) {
    _pmsg = msg;
    document.getElementById('ep-hd').innerHTML =
      '<div style="font-size:2rem;margin-bottom:7px;">' + icon + '</div>' +
      '<h2 style="color:white;font-size:1.1rem;font-weight:700;line-height:1.35;margin:0;font-family:Poppins,sans-serif;">' + title + '</h2>' +
      '<p style="color:rgba(255,255,255,0.72);font-size:0.78rem;margin-top:5px;font-family:Poppins,sans-serif;">Fill in your details and we will get back to you.</p>';

    document.querySelectorAll('a[href^="https://wa.me"]').forEach(function (l) {
      l.addEventListener('click', function () { _engaged = true; });
    });

    function sp() {
      if (_shown || _engaged) return;
      _shown = true;
      document.getElementById('ep').style.display = 'flex';
    }
    document.addEventListener('mouseleave', function (e) { if (e.clientY <= 0) sp(); });
    document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'hidden') sp(); });
    var st = false;
    window.addEventListener('scroll', function () {
      if (!st && (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 120) {
        st = true; setTimeout(sp, 1800);
      }
    });

    document.getElementById('ep').addEventListener('click', function (e) { if (e.target === this) cep(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') cep(); });
  };

  window.cep = function () { document.getElementById('ep').style.display = 'none'; };

  window.sep = function () {
    var n = document.getElementById('en').value.trim();
    var p = document.getElementById('ep2').value.trim();
    if (!n) { alert('Please enter your name.'); return; }
    if (!/^[6-9][0-9]{9}$/.test(p)) { alert('Please enter a valid 10-digit mobile number.'); return; }
    window.open('https://wa.me/919045222870?text=' + encodeURIComponent('Hi, I am ' + n + ' (' + p + '). ' + _pmsg), '_blank');
    cep();
  };

})();

/* ═══ ADD TO END OF common.js ═══ */
(function injectContactUI() {
    var WA = 'https://wa.me/919045222870?text=Hello!%20I%20am%20interested%20in%20your%20CA%20services.%20Please%20contact%20me.';

    function inject() {
        /* Desktop nav button */
        var burger = document.getElementById('burgerMenu');
        if (burger && document.getElementById('site-nav') && !document.querySelector('.navbar-actions')) {
            var actions = document.createElement('div');
            actions.className = 'navbar-actions';
            var navBtn = document.createElement('a');
            navBtn.className = 'nav-cta-btn';
            navBtn.href = WA;
            navBtn.target = '_blank';
            navBtn.rel = 'noopener noreferrer';
            navBtn.innerHTML = '&#128222; Contact Us';
            burger.parentNode.insertBefore(actions, burger);
            actions.appendChild(navBtn);
            actions.appendChild(burger);
        }

        /* Mobile floating pill */
        if (!document.querySelector('.mobile-cta-pill')) {
            var pill = document.createElement('a');
            pill.className = 'mobile-cta-pill';
            pill.href = WA;
            pill.target = '_blank';
            pill.rel = 'noopener noreferrer';
            pill.innerHTML = '&#128222; Contact Us';
            document.body.appendChild(pill);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', inject);
    } else {
        inject();
    }
})();

/* ============================================================
   SHARED SCROLL REVEAL + NAVBAR SCROLL EFFECT
   Runs on every page that loads common.js
   ============================================================ */
(function () {
    function initAnimations() {
        /* ── Scroll reveal ── */
        var els = document.querySelectorAll('.reveal, .reveal-stagger, .stat-item');
  if ('IntersectionObserver' in window) {
            var io = new IntersectionObserver(function (entries) {
                entries.forEach(function (e) {
                    if (e.isIntersecting) {
                        e.target.classList.add('visible');
                        io.unobserve(e.target);
                    }
                });
            }, { threshold: 0, rootMargin: '50px 0px 50px 0px' });
            els.forEach(function (el) { io.observe(el); });
        } else {
            els.forEach(function (el) { el.classList.add('visible'); });
        }

        /* ── Navbar shadow on scroll ── */
        var navbar = document.querySelector('.navbar');
        if (navbar) {
            window.addEventListener('scroll', function () {
                navbar.classList.toggle('scrolled', window.scrollY > 8);
            }, { passive: true });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAnimations);
    } else {
        initAnimations();
    }
})();


/* ── FAQ ACCORDION ───────────────────────────────────────── */
(function(){
  document.querySelectorAll('.faq-item').forEach(function(item){
    var btn = item.querySelector('.faq-question');
    if(!btn) return;
    btn.addEventListener('click', function(){
      var isOpen = item.classList.contains('open');
      // close all in same list
      var list = item.closest('.faq-list');
      if(list) list.querySelectorAll('.faq-item.open').forEach(function(o){ o.classList.remove('open'); });
      if(!isOpen) item.classList.add('open');
    });
  });
})();


/* Theme preview listener: applies themes sent by theme-selector.html.
   Only accepts messages from the parent window; inert on normal visits. */
(function () {
  window.addEventListener('message', function (e) {
    if (!e.data || e.data.type !== 'taxamc-theme' || e.source !== window.parent) return;
    var vars = e.data.vars || {};
    Object.keys(vars).forEach(function (k) {
      document.documentElement.style.setProperty(k, vars[k]);
    });
  });
  // Tell the selector this page is ready to receive themes
  if (window.parent !== window) window.parent.postMessage({ type: 'taxamc-ready' }, '*');
})();



/* ── WHATSAPP: add the page link to the message ── */
(function () {
  function addPageLink(e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href*="wa.me"]') : null;
    if (!a || a.getAttribute('data-page-added') === '1') return;
    var url = new URL(a.href);
    var text = url.searchParams.get('text') || '';
    var pageUrl = window.location.href.split('#')[0];
    url.searchParams.set('text', text + '\n\nPage: ' + pageUrl);
    a.href = url.toString();
    a.setAttribute('data-page-added', '1');
  }
  document.addEventListener('click', addPageLink, true);
  document.addEventListener('auxclick', addPageLink, true);
})();

/* ── CLIENT REVIEWS STRIP (moving, shared on all pages without a testimonials section) ── */
(function () {
  var REVIEWS = [
    { q: '\u201CMr. Agarwal was very knowledgeable and guided me correctly at the right time. He was always available, on text and call, whenever I needed help.\u201D', n: 'Krishnan Pillai', r: 'ITR filing' },
    { q: '\u201CGreat service by CA. Mayank Agarwal. Have been associated with him for long. Thanks for handling my taxes and finances.\u201D', n: 'Prasoon Vashishtha', r: 'Long-term client' },
    { q: '\u201CThe team is knowledgeable, professional, and always ready to assist. Their timely service and clear guidance made the entire process smooth.\u201D', n: 'Aniket Singhal', r: 'GST, accounting, ITR and project report' },
    { q: '\u201CI started my business and got company registration, GST registration and accounting services from them. Fully satisfied.\u201D', n: 'Jasmeet Singh', r: 'Business setup' },
    { q: '\u201CMr. Mayank is a highly knowledgeable, supportive, methodical and painstaking person. My work is always done before time.\u201D', n: 'Maalik', r: 'Accounting and compliance' },
    { q: '\u201CFast working, professional approach. Would definitely recommend.\u201D', n: 'Gaurav Kumar', r: 'Professional services' }
  ];
  var css =
    '.tm-wrap{background:#f8fafc;padding:56px 0;overflow:hidden}' +
    '.tm-head{text-align:center;margin-bottom:28px;font-family:Poppins,sans-serif}' +
    '.tm-head p{color:#FF3333;font-weight:600;font-size:.85rem;letter-spacing:1px;text-transform:uppercase;margin:0 0 6px}' +
    '.tm-head h2{color:#111;font-size:1.6rem;font-weight:700;margin:0}' +
    '.tm-track{display:flex;gap:20px;width:max-content;animation:tm-scroll 45s linear infinite;padding:4px 10px}' +
    '.tm-wrap:hover .tm-track{animation-play-state:paused}' +
    '.tm-card{width:330px;flex-shrink:0;background:#fff;border-radius:12px;padding:22px 24px;box-shadow:0 2px 12px rgba(0,0,0,.07);border-top:3px solid #FF3333;font-family:Poppins,sans-serif;margin:0}' +
    '.tm-stars{color:#FF3333;letter-spacing:2px;margin-bottom:10px}' +
    '.tm-card blockquote{margin:0 0 14px;color:#444;font-size:.92rem;line-height:1.7}' +
    '.tm-card figcaption strong{display:block;color:#111;font-size:.95rem}' +
    '.tm-card figcaption span{color:#777;font-size:.8rem}' +
    '@keyframes tm-scroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}' +
    '@media (max-width:600px){.tm-card{width:280px}}' +
    '@media (prefers-reduced-motion:reduce){.tm-track{animation:none;width:auto;flex-wrap:wrap;justify-content:center}.tm-dup{display:none}}';
  function card(x, dup) {
    return '<figure class="tm-card' + (dup ? ' tm-dup" aria-hidden="true"' : '"') + '>' +
      '<div class="tm-stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</div>' +
      '<blockquote>' + x.q + '</blockquote>' +
      '<figcaption><strong>' + x.n + '</strong><span>' + x.r + '</span></figcaption></figure>';
  }
  var cards = REVIEWS.map(function (x) { return card(x, false); }).join('');
  var dupCards = REVIEWS.map(function (x) { return card(x, true); }).join('');
  var html =
    '<section class="tm-wrap" aria-label="Client reviews">' +
      '<div class="tm-head"><p>Client Reviews</p><h2>What our clients say</h2></div>' +
      '<div class="tm-track">' + cards + dupCards + '</div>' +
    '</section>';
  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);
  if (document.getElementById('testimonials') || document.querySelector('.tm-wrap')) return;
  function mount() {
    var ft = document.getElementById('site-footer');
    if (ft) ft.insertAdjacentHTML('beforebegin', html);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
