// Mockup behaviour for the course design (learn/DESIGN.md).
// Injects the shared chrome (nav, sidebar, Ask Claude) so every mockup page shows
// the same markup, and wires the interactive states. Not production code: the
// port session rebuilds this in Jekyll includes and the real widget scripts.

(function () {
  const site = document.querySelector(".site");
  const page = site.dataset.page;          // home | lesson | reference | plain | components
  const current = site.dataset.current;    // id of the current course item, e.g. "l2"

  // ---------- Icons (Lucide-style strokes, 24px grid) ----------
  const I = {
    menu: '<path d="M4 6h16M4 12h16M4 18h16"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    moon: '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
    chat: '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/><path d="M9 10.5h6M9 13.5h4"/>',
    close: '<path d="M6 6l12 12M18 6L6 18"/>',
    send: '<path d="M12 19V5M6 11l6-6 6 6"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    chev: '<path d="M9 6l6 6-6 6"/>',
    chevDown: '<path d="M6 9l6 6 6-6"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    spark: '<path d="M12 3l1.8 4.6L18.5 9.5l-4.7 1.9L12 16l-1.8-4.6L5.5 9.5l4.7-1.9z"/><path d="M19 15l.7 1.8 1.8.7-1.8.7L19 20l-.7-1.8-1.8-.7 1.8-.7z"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    x: '<path d="M7 7l10 10M17 7L7 17"/>',
    list: '<path d="M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01"/>',
  };
  const icon = (name, cls = "icon") => `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true">${I[name]}</svg>`;
  window.mockIcon = icon;

  // ---------- Course data (from _data/parts.yml + lesson front matter in the real site) ----------
  const parts = [
    { id: "market-data", n: 1, title: "Market data",
      lessons: [
        { id: "l1", n: 1, short: "Bars and adjusted close", href: "#" },
        { id: "l3", n: 3, short: "Adjusted close rewrites the past", href: "#" },
      ] },
    { id: "performance", n: 2, title: "Measuring performance",
      lessons: [{ id: "l2", n: 2, short: "The stats table", href: "lesson.html" }] },
    { id: "backtesting", n: 3, title: "Backtesting without fooling yourself", lessons: [] },
    { id: "first-strategy", n: 4, title: "A first strategy, end to end", lessons: [] },
  ];
  const reference = [{ id: "r1", title: "Bars and stats", href: "reference.html" }];
  const navLinks = [
    { id: "reference", title: "Reference", href: "reference.html" },
    { id: "resources", title: "Resources", href: "resources.html" },
    { id: "mission", title: "Mission", href: "mission.html" },
  ];
  const navCurrent = page === "reference" ? "reference" : site.dataset.nav;

  // ---------- Mockup page switcher (not part of the design) ----------
  const bar = document.querySelector("[data-mock-bar]");
  if (bar) {
    const pages = [["index.html", "Dashboard"], ["lesson.html", "Lesson"], ["lesson.html#ask", "Lesson + Ask Claude"],
      ["reference.html", "Reference"], ["mission.html", "Mission"], ["resources.html", "Resources"], ["components.html", "Components and states"]];
    const here = location.pathname.split("/").pop() || "index.html";
    bar.innerHTML = "<b>Design mockup</b>" + pages.map(([h, t]) =>
      `<a href="${h}"${h === here && !h.includes("#") ? ' aria-current="page"' : ""}>${t}</a>`).join("");
    bar.addEventListener("click", (e) => { const a = e.target.closest('a[href="lesson.html#ask"]'); if (a && here === "lesson.html") { e.preventDefault(); setChat(true); } });
  }

  // ---------- Nav ----------
  const nav = document.querySelector("[data-nav]");
  if (nav) {
    nav.innerHTML = `<div class="inner">
      <button class="icon-btn menu-btn" type="button" aria-label="Open course menu" aria-expanded="false" data-drawer-open>${icon("menu")}</button>
      <a class="brand" href="index.html"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 3v14M6 7h4M10 13h4"/></svg>Algorithmic Trading</a>
      <nav class="nav-links" aria-label="Site">${navLinks.map((l) =>
        `<a href="${l.href}"${l.id === navCurrent ? ' aria-current="page"' : ""}>${l.title}</a>`).join("")}</nav>
      <button class="icon-btn theme-btn" type="button" aria-label="Switch light or dark theme">${icon("sun", "icon sun")}${icon("moon", "icon moon")}</button>
    </div>`;
  }

  // ---------- Sidebar (course tree) ----------
  const sidebar = document.querySelector("[data-sidebar]");
  if (sidebar) {
    sidebar.setAttribute("aria-label", "Course");
    const tree = parts.map((p) => `<li class="part${p.lessons.length ? "" : " planned"}">
      <div class="part-head"><span class="label">Part ${p.n}${p.lessons.length ? "" : ' · <span class="pill">Planned</span>'}</span>
      <span class="part-title">${p.title}</span></div>
      ${p.lessons.length ? `<ol>${p.lessons.map((l) => `<li><a href="${l.href}"${l.id === current ? ' aria-current="page"' : ""}>
        <span class="n">${l.n}</span><span>${l.short}</span></a></li>`).join("")}</ol>` : ""}
    </li>`).join("");
    sidebar.innerHTML = `
      <div class="drawer-links">${[{ title: "Course home", href: "index.html", id: "home" }, ...navLinks].map((l) =>
        `<a href="${l.href}"${l.id === navCurrent || (l.id === "home" && page === "home") ? ' aria-current="page"' : ""}>${l.title}</a>`).join("")}</div>
      <ol class="course-tree">${tree}</ol>
      <div class="sidebar-section"><span class="label">Reference</span>
        ${reference.map((r) => `<a href="${r.href}"${r.id === current ? ' aria-current="page"' : ""}>${r.title}</a>`).join("")}
      </div>`;
  }

  // ---------- Ask Claude chrome ----------
  const askable = site.dataset.ask !== "off";
  if (askable) {
    site.insertAdjacentHTML("beforeend", `
      <button class="ask-fab" type="button" data-chat-open aria-label="Ask Claude">${icon("chat")}<span class="fab-label">Ask Claude</span>${site.dataset.thread ? '<span class="dot" title="This page has a conversation"></span>' : ""}</button>
      <aside class="ask-panel" aria-label="Ask Claude" id="ask-panel">
        <div class="ask-head">
          <div class="title"><b>Ask Claude</b><span>About: ${document.querySelector("h1")?.textContent ?? document.title}</span></div>
          <div class="actions">
            <button class="btn btn-ghost new-topic" type="button" data-new-topic>${icon("plus")}New topic</button>
            <button class="icon-btn" type="button" aria-label="Close" data-chat-close>${icon("close")}</button>
          </div>
        </div>
        <div class="ask-body" data-ask-body></div>
        <div class="ask-foot">
          <form class="composer" data-composer>
            <textarea id="ask-input" rows="1" placeholder="Ask about this page…" aria-label="Message"></textarea>
            <button class="send-btn" type="submit" aria-label="Send" disabled>${icon("send")}</button>
          </form>
          <p class="ask-hint">Claude reads this page and anything you select. Saved with this page.</p>
        </div>
      </aside>`);
  }
  site.insertAdjacentHTML("beforeend", '<div class="scrim" data-scrim></div>');

  // ---------- Theme toggle ----------
  const root = document.documentElement;
  try { const t = localStorage.getItem("course-theme"); if (t) root.dataset.theme = t; } catch (e) {}
  const isDark = () => root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".theme-btn")) return;
    root.dataset.theme = isDark() ? "light" : "dark";
    try { localStorage.setItem("course-theme", root.dataset.theme); } catch (err) {}
  });

  // ---------- Drawer ----------
  const setDrawer = (open) => {
    site.dataset.drawer = open ? "open" : "closed";
    document.querySelectorAll("[data-drawer-open]").forEach((b) => b.setAttribute("aria-expanded", String(open)));
  };
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-drawer-open]")) setDrawer(site.dataset.drawer !== "open");
    if (e.target.closest("[data-scrim]")) { setDrawer(false); setChat(false); }
  });

  // ---------- Chat panel ----------
  const body = document.querySelector("[data-ask-body]");
  function setChat(open) {
    if (!askable) return;
    site.dataset.chat = open ? "open" : "closed";
    if (open) { renderThread(); setTimeout(() => document.getElementById("ask-input")?.focus({ preventScroll: true }), 50); }
  }
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-chat-open]")) setChat(true);
    if (e.target.closest("[data-chat-close]")) setChat(false);
    if (e.target.closest("[data-new-topic]")) { body.insertAdjacentHTML("beforeend", '<div class="divider topic">New topic</div>'); scrollDown(); }
    const sug = e.target.closest(".suggestions button");
    if (sug) send(sug.textContent, null);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { closePop(); setDrawer(false); if (site.dataset.chat === "open") setChat(false); }
  });

  let rendered = false;
  function renderThread() {
    if (rendered || !body) return;
    rendered = true;
    const seed = document.getElementById("thread-seed");
    body.innerHTML = seed ? seed.innerHTML : emptyState();
    typeset(body);
    scrollDown();
  }
  function emptyState() {
    const t = document.querySelector("h1")?.textContent ?? "this page";
    return `<div class="ask-empty" data-empty>
      <h3>Ask about “${t}”</h3>
      <p>Claude reads this page with you. Select a passage in the lesson to ask about it, or start here.</p>
      <div class="suggestions"><button type="button">Quiz me on this lesson</button>
      <button type="button">Explain the √252 rule more simply</button>
      <button type="button">How does this connect to my notebook?</button></div></div>`;
  }
  const scrollDown = () => { if (body) body.scrollTop = body.scrollHeight; };
  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function send(text, quote) {
    body.querySelector("[data-empty]")?.remove();
    const chip = quote ? `<span class="quote-chip"><span class="where">From ${esc(quote.where)}</span><q>${esc(quote.text)}</q></span>` : "";
    body.insertAdjacentHTML("beforeend", `<div class="msg msg-user">${chip}<div>${esc(text)}</div></div>
      <div class="msg msg-claude" data-pending><span class="typing" aria-label="Claude is thinking"><i></i><i></i><i></i></span></div>`);
    scrollDown();
    setTimeout(() => {
      const p = body.querySelector("[data-pending]");
      if (!p) return;
      p.removeAttribute("data-pending");
      p.innerHTML = "<p>This is a mockup, so no real answer comes back. On the published site Claude replies here, with the selected passage, its section and the whole page as context, and the exchange is saved with this page.</p>";
      scrollDown();
    }, 1100);
  }

  const composer = document.querySelector("[data-composer]");
  if (composer) {
    const ta = composer.querySelector("textarea");
    const btn = composer.querySelector("button");
    ta.addEventListener("input", () => {
      btn.disabled = !ta.value.trim();
      ta.style.height = "auto"; ta.style.height = ta.scrollHeight + "px";
    });
    ta.addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); composer.requestSubmit(); } });
    composer.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!ta.value.trim()) return;
      send(ta.value.trim(), null);
      ta.value = ""; ta.style.height = "auto"; btn.disabled = true;
    });
  }

  // ---------- Selection popover (lesson pages only) ----------
  const prose = document.querySelector(".content .prose");
  let pop = null;
  function closePop() { pop?.remove(); pop = null; }
  function sectionOf(node) {
    let el = node.nodeType === 1 ? node : node.parentElement;
    let block = el.closest(".prose > *");
    while (block && block.tagName !== "H2") block = block.previousElementSibling;
    return block ? "§ " + block.textContent : "the introduction";
  }
  if (askable && page === "lesson" && prose) {
    document.addEventListener("mouseup", (e) => {
      if (e.target.closest(".sel-pop")) return;
      setTimeout(() => {
        const sel = getSelection();
        const text = sel.toString().trim();
        if (!text || !sel.rangeCount || !prose.contains(sel.anchorNode) || e.target.closest("button, input, .quiz, .numeric")) { closePop(); return; }
        const rects = sel.getRangeAt(0).getClientRects();
        const r = rects[rects.length - 1];
        closePop();
        pop = document.createElement("div");
        pop.className = "sel-pop";
        pop.style.left = Math.min(r.right + scrollX + 6, document.documentElement.clientWidth - 48) + "px";
        pop.style.top = r.top + scrollY - 6 - 32 + "px";
        pop.dataset.below = r.bottom + scrollY + 8;
        pop.innerHTML = `<button class="sel-btn" type="button" aria-label="Ask Claude about the selection">${icon("spark")}</button>`;
        document.body.appendChild(pop);
        const quote = { text: text.length > 280 ? text.slice(0, 277) + "…" : text, where: sectionOf(sel.anchorNode) };
        pop.querySelector(".sel-btn").addEventListener("click", () => openMenu(quote));
      }, 0);
    });
  }
  function openMenu(quote) {
    const left = Math.min(parseFloat(pop.style.left), document.documentElement.clientWidth - 296 + scrollX);
    pop.style.left = Math.max(8, left) + "px";
    pop.style.top = pop.dataset.below + "px";   // the menu opens below the selection so the text stays readable
    pop.innerHTML = `<div class="sel-menu" role="dialog" aria-label="Ask about the selection">
      <button class="sel-explain" type="button">${icon("spark")}Explain this</button>
      <form><input id="sel-prompt" type="text" placeholder="Ask something else…" aria-label="Your question about the selection">
      <button class="send-btn" type="submit" aria-label="Ask">${icon("send")}</button></form></div>`;
    pop.querySelector(".sel-explain").focus();
    pop.querySelector(".sel-explain").addEventListener("click", () => { closePop(); setChat(true); send("Explain this", quote); });
    pop.querySelector("form").addEventListener("submit", (e) => {
      e.preventDefault();
      const v = pop.querySelector("input").value.trim();
      if (!v) return;
      closePop(); setChat(true); send(v, quote);
    });
  }
  document.addEventListener("mousedown", (e) => { if (pop && !e.target.closest(".sel-pop")) closePop(); });

  // ---------- TOC (from ## headings) ----------
  const h2s = prose ? [...prose.querySelectorAll(":scope > h2, :scope > section > h2")] : [];
  h2s.forEach((h) => { if (!h.id) h.id = h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""); });
  const tocItems = h2s.map((h) => `<li><a href="#${h.id}">${h.textContent}</a></li>`).join("");
  const rail = document.querySelector("[data-toc]");
  if (rail) rail.innerHTML = `<span class="label">On this page</span><ol>${tocItems}</ol>`;
  const inline = document.querySelector("[data-toc-inline]");
  if (inline) inline.innerHTML = `<summary>${icon("list")}On this page${icon("chevDown")}</summary><ol>${tocItems}</ol>`;
  if (rail && h2s.length) {
    const links = [...rail.querySelectorAll("a")];
    const spy = () => {
      let i = 0;
      h2s.forEach((h, k) => { if (h.getBoundingClientRect().top < 140) i = k; });
      links.forEach((a, k) => a.setAttribute("aria-current", String(k === i)));
    };
    addEventListener("scroll", spy, { passive: true }); spy();
  }

  // ---------- Practice widgets (same data attributes as learn/assets/quiz.js) ----------
  document.querySelectorAll(".quiz[data-answer]").forEach((box) => {
    const answer = box.dataset.answer;
    const explain = box.querySelector(".explain");
    const buttons = box.querySelectorAll(".choice");
    buttons.forEach((b) => b.addEventListener("click", () => {
      const mark = b.querySelector(".mark");
      if (b.dataset.choice === answer) {
        b.classList.add("right"); mark.innerHTML = icon("check", "icon");
        buttons.forEach((x) => (x.disabled = true));
        explain?.classList.add("shown");
      } else {
        b.classList.add("wrong"); mark.innerHTML = icon("x", "icon"); b.disabled = true;
      }
    }));
  });
  document.querySelectorAll(".numeric[data-answer]").forEach((box, idx) => {
    const answer = parseFloat(box.dataset.answer), tol = parseFloat(box.dataset.tol || "0");
    const percent = box.hasAttribute("data-percent");
    const explain = box.querySelector(".explain");
    box.insertBefore(Object.assign(document.createElement("div"), { className: "row", innerHTML:
      `<input class="field" id="num-${idx}" type="text" inputmode="decimal" placeholder="${percent ? "e.g. 12.3%" : "your answer"}" aria-label="Your answer">
       <button class="btn btn-primary" type="button" data-check>Check</button>
       <button class="btn btn-ghost" type="button" data-give-up>Show solution</button>` }), explain);
    const fb = Object.assign(document.createElement("p"), { className: "feedback" });
    box.insertBefore(fb, explain);
    const input = box.querySelector("input");
    const say = (cls, ic, text) => { fb.className = "feedback " + cls; fb.innerHTML = icon(ic) + text; };
    const grade = () => {
      const raw = input.value.replace(",", ".").replace("%", "").trim();
      let v = raw === "" ? NaN : parseFloat(raw); if (percent) v /= 100;
      input.classList.remove("is-wrong", "is-right");
      if (Number.isNaN(v)) { input.classList.add("is-wrong"); return say("wrong", "x", "Type a number first."); }
      if (Math.abs(v - answer) <= tol) { input.classList.add("is-right"); input.readOnly = true; say("right", "check", "Correct."); explain?.classList.add("shown"); }
      else { input.classList.add("is-wrong"); say("wrong", "x", `Not quite: ${v > answer ? "too high" : "too low"}. Try again.`); }
    };
    box.querySelector("[data-check]").addEventListener("click", grade);
    input.addEventListener("keydown", (e) => { if (e.key === "Enter") grade(); });
    box.querySelector("[data-give-up]").addEventListener("click", () => explain?.classList.add("shown"));
  });

  // ---------- Math ----------
  function typeset(el) {
    if (window.renderMathInElement) renderMathInElement(el, {
      delimiters: [{ left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }],
      output: "mathml", throwOnError: false });
  }
  typeset(document.querySelector(".content") || document.body);

  if (location.hash === "#ask") setChat(true);
})();
