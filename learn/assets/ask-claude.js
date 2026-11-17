// Ask Claude (learn/DESIGN.md section 6): a floating button and side chat on every page, plus a
// selection popover on lessons. It runs only where the artifact runtime grants `sample`
// (the published artifact); under jekyll serve or as plain files nothing of it appears.
//
// Every request sends: standing instructions with the course brief (mission and glossary, from
// #course-brief) and the full text of this page, then the thread since the last "New topic".
// A message sent from a selection carries the selected text and its section heading.
//
// Threads are saved in the artifact's db, one document per page in the `chats` collection
// (id "<page key>.<volume>", a new volume once a document nears the size limit). The publish step
// declares rules that make the whole db readable and writable by the owner only, so a teaching
// session reads the chats with ArtifactData acting as the owner. Other viewers chat unsaved.

(function () {
  const site = document.querySelector(".site");
  const claude = window.claude;
  if (!site || !claude || typeof claude.use !== "function") return;

  const KEY = site.dataset.key || "page";
  const KIND = site.dataset.kind || "page";
  const TITLE = site.dataset.title || document.title;
  const SHORT = site.dataset.short || TITLE;
  const PAGE_PATH = KEY === "index" ? "index.html" : KEY.replace("-", "/") + ".html";
  const MAX_DOC_CHARS = 200000;   // db documents are capped at 256 KiB
  const MAX_TURNS = 24;           // conversation turns sent with a request
  const MAX_PAGE_CHARS = 60000;

  const ICON = {
    chat: '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/><path d="M9 10.5h6M9 13.5h4"/>',
    close: '<path d="M6 6l12 12M18 6L6 18"/>',
    send: '<path d="M12 19V5M6 11l6-6 6 6"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    spark: '<path d="M12 3l1.8 4.6L18.5 9.5l-4.7 1.9L12 16l-1.8-4.6L5.5 9.5l4.7-1.9z"/><path d="M19 15l.7 1.8 1.8.7-1.8.7L19 20l-.7-1.8-1.8-.7 1.8-.7z"/>',
  };
  const icon = (name) => `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">${ICON[name]}</svg>`;
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  start();

  async function start() {
    const sample = await claude.use("sample").catch(() => null);
    if (!sample) return;                                  // not an artifact view: the feature stays absent
    const [db, user] = await Promise.all([
      claude.use("db").catch(() => null),
      claude.use("user").catch(() => null),
    ]);
    const isOwner = user ? await user.isOwner().catch(() => false) : false;
    const store = db && isOwner ? threadStore(db) : null;
    build(sample, store);
  }

  // ---------- Storage ----------

  function threadStore(db) {
    const col = db.collection("chats");
    let docs = [];        // [{vol, items}], oldest volume first
    let queue = Promise.resolve();
    return {
      async load() {
        const snap = await withTimeout(col.where("page", "==", KEY).get(), 10000);
        docs = snap.docs.map((d) => d.data()).filter(Boolean)
          .map((d) => ({ vol: Number(d.vol) || 1, items: Array.isArray(d.items) ? d.items.slice() : [] }))
          .sort((a, b) => a.vol - b.vol);
        return docs.flatMap((d) => d.items);
      },
      // Save the whole thread: earlier volumes are frozen, the last one takes the rest.
      save(items) {
        queue = queue.catch(() => {}).then(async () => {
          const frozen = docs.slice(0, -1).reduce((n, d) => n + d.items.length, 0);
          let current = docs[docs.length - 1] || { vol: 1, items: [] };
          if (!docs.length) docs.push(current);
          current.items = items.slice(frozen);
          if (JSON.stringify(current.items).length > MAX_DOC_CHARS && current.items.length > 1) {
            // Freeze all but the newest item in this volume and continue in a fresh one.
            const carry = current.items.pop();
            await col.doc(`${KEY}.${current.vol}`).set(body(current));
            current = { vol: current.vol + 1, items: [carry] };
            docs.push(current);
          }
          await col.doc(`${KEY}.${current.vol}`).set(body(current));
        });
        return queue;
      },
    };
    function body(d) {
      return { page: KEY, vol: d.vol, url: PAGE_PATH, title: TITLE, kind: KIND, updated: new Date().toISOString(), items: d.items };
    }
  }

  function withTimeout(promise, ms) {
    return Promise.race([promise, new Promise((_, reject) => setTimeout(() => reject({ code: "timeout" }), ms))]);
  }

  // ---------- UI ----------

  function build(sample, store) {
    site.insertAdjacentHTML("beforeend", `
      <button class="ask-fab" type="button" data-chat-open aria-label="Ask Claude">${icon("chat")}<span class="fab-label">Ask Claude</span></button>
      <aside class="ask-panel" aria-label="Ask Claude" id="ask-panel">
        <div class="ask-head">
          <div class="title"><b>Ask Claude</b><span>About: ${esc(TITLE)}</span></div>
          <div class="actions">
            <button class="btn btn-ghost new-topic" type="button" data-new-topic>${icon("plus")}New topic</button>
            <button class="icon-btn" type="button" aria-label="Close" data-chat-close>${icon("close")}</button>
          </div>
        </div>
        <div class="ask-body" data-ask-body aria-live="polite"></div>
        <div class="ask-foot">
          <form class="composer" data-composer>
            <textarea id="ask-input" rows="1" placeholder="Ask about this page…" aria-label="Message"></textarea>
            <button class="send-btn" type="submit" aria-label="Send" disabled>${icon("send")}</button>
          </form>
          <p class="ask-hint">${store ? "Claude reads this page and anything you select. Saved with this page."
            : "Claude reads this page and anything you select. Not saved: only the course owner's chats are kept."}</p>
        </div>
      </aside>`);
    document.querySelectorAll("[data-ask-cta]").forEach((el) => (el.hidden = false));

    const fab = site.querySelector(".ask-fab");
    const body = site.querySelector("[data-ask-body]");
    const form = site.querySelector("[data-composer]");
    const input = form.querySelector("textarea");
    const sendBtn = form.querySelector("button");
    const hint = site.querySelector(".ask-hint");
    let items = [];              // the thread: {t: "user"|"claude"|"topic", text?, quote?, at}
    let loaded = !store;
    let busy = false;
    let loadNote = "";

    loadLibs().then(() => { if (isOpen() && !busy) render(); });

    if (store) {
      store.load().then((saved) => { items = saved; loaded = true; markFab(); if (isOpen()) render(); })
        .catch(() => { loaded = true; loadNote = "The saved conversation can't be reached right now. New messages may not be saved."; if (isOpen()) render(); });
    }

    // Open and close
    const isOpen = () => site.dataset.chat === "open";
    function setOpen(open) {
      site.dataset.chat = open ? "open" : "closed";
      if (open) {
        render();
        setTimeout(() => input.focus({ preventScroll: true }), 50);
      } else fab.focus({ preventScroll: true });
    }
    document.addEventListener("click", (e) => {
      if (e.target.closest("[data-chat-open]")) setOpen(true);
      else if (e.target.closest("[data-chat-close]")) setOpen(false);
      else if (e.target.closest("[data-scrim]") && isOpen()) setOpen(false);
      else if (e.target.closest("[data-new-topic]")) newTopic();
      else if (e.target.closest("[data-retry]")) retry();
      else {
        const s = e.target.closest("[data-suggest]");
        if (s) ask(s.textContent, null);
      }
    });
    document.addEventListener("keydown", (e) => {
      if (e.key !== "Escape") return;
      if (pop) closePop();
      else if (isOpen()) setOpen(false);
    });

    // Composer: Enter sends, Shift+Enter adds a line, grows up to 9rem.
    const grow = () => { input.style.height = "auto"; input.style.height = input.scrollHeight + "px"; };
    input.addEventListener("input", () => { sendBtn.disabled = busy || !input.value.trim(); grow(); });
    input.addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.shiftKey && !e.isComposing) { e.preventDefault(); form.requestSubmit(); } });
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const text = input.value.trim();
      if (!text || busy) return;
      input.value = ""; grow(); sendBtn.disabled = true;
      ask(text, null);
    });

    function markFab() {
      const has = items.some((i) => i.t === "user");
      let dot = fab.querySelector(".dot");
      if (has && !dot) fab.insertAdjacentHTML("beforeend", '<span class="dot" title="This page has a conversation"></span>');
      if (!has && dot) dot.remove();
    }

    // ---------- Thread rendering ----------

    function dayLabel(iso) {
      const d = new Date(iso);
      if (d.toDateString() === new Date().toDateString()) return "Today";
      return d.toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" }).replace(",", "");
    }

    function render() {
      if (!loaded) { body.innerHTML = '<p class="msg-note">Loading the saved conversation…</p>'; return; }
      if (!items.length) { body.innerHTML = emptyState() + (loadNote ? `<p class="msg-note">${esc(loadNote)}</p>` : ""); return; }
      let html = loadNote ? `<p class="msg-note">${esc(loadNote)}</p>` : "";
      let day = "";
      for (const item of items) {
        const label = dayLabel(item.at);
        if (label !== day) { day = label; html += `<div class="divider">${label}</div>`; }
        if (item.t === "topic") html += '<div class="divider topic">New topic</div>';
        else if (item.t === "user") html += userHtml(item);
        else html += `<div class="msg msg-claude">${markdown(item.text)}</div>`;
      }
      body.innerHTML = html;
      body.querySelectorAll(".msg-claude").forEach(typeset);
      scrollDown();
    }

    function userHtml(item) {
      const q = item.quote;
      const chip = q ? `<span class="quote-chip"><span class="where">From ${esc(q.where)}</span><q>${esc(q.text)}</q></span>` : "";
      return `<div class="msg msg-user">${chip}<div>${esc(item.text)}</div></div>`;
    }

    function emptyState() {
      const prompts = {
        lesson: ["Quiz me on this lesson", "Summarize the key ideas in three sentences", "Show me how to check this on my own data"],
        reference: ["Explain one formula here with a worked example", "Quiz me on this sheet"],
        home: ["Where should I start?", "What will I be able to do by the end?"],
        page: ["Summarize this page", "How does this fit the course?"],
      }[KIND] || ["Summarize this page"];
      const help = KIND === "lesson"
        ? "Claude reads this page with you. Select a passage in the lesson to ask about it, or start here."
        : "Claude reads this page with you. Ask anything about it, or start here.";
      return `<div class="ask-empty"><h3>Ask about “${esc(SHORT)}”</h3><p>${help}</p>
        <div class="suggestions">${prompts.map((p) => `<button type="button" data-suggest>${esc(p)}</button>`).join("")}</div></div>`;
    }

    const scrollDown = () => { body.scrollTop = body.scrollHeight; };

    // ---------- Sending ----------

    function save() {
      markFab();
      if (!store) return;
      store.save(items).catch(() => {
        hint.textContent = "Couldn't save the last message. It stays here until you leave the page.";
        hint.classList.add("unsaved");
      });
    }

    function newTopic() {
      if (busy || !items.length || items[items.length - 1].t === "topic") return;
      items.push({ t: "topic", at: new Date().toISOString() });
      save();
      render();
      input.focus({ preventScroll: true });
    }

    function ask(text, quote) {
      if (busy) return;
      if (!isOpen()) setOpen(true);
      const item = { t: "user", text, at: new Date().toISOString() };
      if (quote) item.quote = quote;
      items.push(item);
      save();
      render();
      reply();
    }

    function retry() {
      if (busy || !items.length || items[items.length - 1].t !== "user") return;
      render();
      reply();
    }

    async function reply() {
      busy = true;
      sendBtn.disabled = true;
      body.querySelector(".msg-error")?.remove();
      const out = document.createElement("div");
      out.className = "msg msg-claude";
      out.innerHTML = '<span class="typing" aria-label="Claude is thinking"><i></i><i></i><i></i></span>';
      body.appendChild(out);
      scrollDown();

      let frame = 0;
      let latest = "";
      const paint = () => {
        frame = 0;
        const stick = body.scrollHeight - body.scrollTop - body.clientHeight < 40;
        out.innerHTML = markdown(latest);
        (out.lastElementChild || out).classList.add("caret");
        typeset(out);
        if (stick) scrollDown();
      };
      try {
        const { text, truncated } = await sample(buildInput(), {
          cache: false,
          onText: ({ text }) => { latest = text; if (!frame) frame = requestAnimationFrame(paint); },
        });
        if (frame) cancelAnimationFrame(frame);
        const final = truncated ? text + "\n\n*(Cut short. Ask for less at a time.)*" : text;
        items.push({ t: "claude", text: final, at: new Date().toISOString() });
        save();
        render();
      } catch (e) {
        if (frame) cancelAnimationFrame(frame);
        out.remove();
        const partial = e && e.text;
        if (partial && e.code !== "refused") {
          items.push({ t: "claude", text: partial + "\n\n*(Interrupted.)*", at: new Date().toISOString() });
          save();
          render();
        } else if (e && e.code !== "cancelled") {
          showError(e && e.code);
        }
      } finally {
        busy = false;
        sendBtn.disabled = !input.value.trim();
      }
    }

    function showError(code) {
      const permanent = ["not_granted", "sampling_disabled", "not_declared", "capability_disabled", "capability_removed"].includes(code);
      const text = permanent ? "Claude isn't available to you on this page."
        : code === "rate_limited" ? "Claude is busy with too many questions. Your question is kept; retry in a minute."
        : code === "session_expired" ? "You've been signed out. Sign in to claude.ai again, then retry."
        : "Claude didn't answer. Your question is kept.";
      body.insertAdjacentHTML("beforeend", `<div class="msg-error"><span>${text}</span>${permanent ? "" : '<button class="btn btn-secondary" type="button" data-retry>Retry</button>'}</div>`);
      scrollDown();
    }

    // ---------- Prompt ----------

    function buildInput() {
      let since = 0;
      items.forEach((it, k) => { if (it.t === "topic") since = k + 1; });
      const turns = items.slice(since).filter((it) => it.t !== "topic").slice(-MAX_TURNS)
        .map((it) => ({ role: it.t === "user" ? "user" : "assistant", content: it.t === "user" ? userTurn(it) : it.text }));
      while (turns.length && turns[0].role !== "user") turns.shift();
      return [{ role: "user", content: instructions() }, ...turns];
    }

    function userTurn(it) {
      if (!it.quote) return it.text;
      return `About this passage, from ${it.quote.where}:\n\n> ${it.quote.text.replace(/\n/g, "\n> ")}\n\n${it.text}`;
    }

    function instructions() {
      let brief = { course: "", mission: "", glossary: [] };
      try { brief = JSON.parse(document.getElementById("course-brief").textContent); } catch (e) { /* missing brief */ }
      const glossary = (brief.glossary || []).map((g) => `- ${g.term}: ${g.definition}`).join("\n");
      const kindName = { lesson: "a lesson", reference: "a reference sheet", home: "the course dashboard", page: "a course page" }[KIND] || "a course page";
      return [
        `You are the teacher of "${brief.course}", a self-paced course on algorithmic trading, answering the learner in a chat beside the page they are reading.`,
        "",
        "How to answer:",
        "- Answer what the learner asked about this page, plainly and briefly: a few short paragraphs, or a short list. Offer to go deeper rather than writing everything at once.",
        "- Use the glossary terms exactly as defined below. Stay consistent with the page; if you add something the page does not say, say so.",
        "- The page text includes the practice questions with their solutions. Do not give away a solution unless the learner asks for it or has already answered.",
        "- Format with Markdown. Write math only as \\( … \\) inline and \\[ … \\] on its own line, never with $ signs; a dollar amount is plain text like $1.89.",
        "- Messages may quote a passage the learner selected on the page, with its section. Explain that passage in the context of the page.",
        "",
        "Course mission:",
        brief.mission || "(none)",
        "",
        "Glossary:",
        glossary || "(none)",
        "",
        `The learner is on ${kindName} titled "${TITLE}". Its full text:`,
        "<page>",
        pageText(),
        "</page>",
      ].join("\n");
    }

    function pageText() {
      const src = document.querySelector(".content .prose") || document.querySelector(".home") || document.querySelector("main");
      if (!src) return "";
      const clone = src.cloneNode(true);
      clone.querySelectorAll(".toc-inline, .ask-cta, script, svg, .row, .feedback").forEach((el) => el.remove());
      clone.querySelectorAll(".katex").forEach((el) => {
        const tex = el.querySelector('annotation[encoding="application/x-tex"]');
        const block = el.querySelector('math[display="block"]');
        if (tex) el.replaceWith(block ? `\\[${tex.textContent}\\]` : `\\(${tex.textContent}\\)`);
      });
      clone.querySelectorAll("h1, h2, h3").forEach((h) => h.prepend("#".repeat(Number(h.tagName[1])) + " "));
      clone.querySelectorAll(".qn").forEach((el) => el.append(": "));
      clone.querySelectorAll(".choice .mark").forEach((el) => el.append(") "));
      clone.querySelectorAll(".explain").forEach((el) => el.prepend("Solution: "));
      clone.querySelectorAll("p, li, h1, h2, h3, tr, pre, .choice, .explain, .q, aside, .key, .note, blockquote").forEach((el) => el.append("\n"));
      clone.querySelectorAll("td, th").forEach((el) => el.append(" | "));
      return clone.textContent.replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim().slice(0, MAX_PAGE_CHARS);
    }

    // ---------- Selection popover (lessons only) ----------

    const prose = document.querySelector(".content .prose");
    let pop = null;
    let pointerDown = false;
    let selTimer = 0;
    function closePop() { if (pop) { pop.remove(); pop = null; } }

    if (KIND === "lesson" && prose) {
      document.addEventListener("pointerdown", (e) => {
        if (pop && !e.target.closest(".sel-pop")) closePop();
        pointerDown = true;
      });
      document.addEventListener("pointerup", (e) => { pointerDown = false; if (!e.target.closest(".sel-pop")) schedule(10); });
      document.addEventListener("pointercancel", () => { pointerDown = false; });
      document.addEventListener("selectionchange", () => schedule(350));
      addEventListener("resize", closePop);
    }

    function schedule(ms) { clearTimeout(selTimer); selTimer = setTimeout(checkSelection, ms); }

    function checkSelection() {
      if (pointerDown) return;
      const sel = getSelection();
      const text = sel ? sel.toString().trim() : "";
      if (pop && pop.dataset.menu) return;                       // the menu is open: keep it
      if (!text || !sel.rangeCount) { closePop(); return; }
      if (pop && pop.dataset.text === text) return;              // same selection: keep the button
      const range = sel.getRangeAt(0);
      const node = range.commonAncestorContainer;
      const el = node.nodeType === 1 ? node : node.parentElement;
      if (!prose.contains(el) || el.closest(".quiz, .numeric, button, input, textarea, .toc-inline, .ask-cta, .page-head")) { closePop(); return; }
      const rects = range.getClientRects();
      const r = rects[rects.length - 1];
      if (!r) return;
      closePop();
      const quote = { text: text.length > 1200 ? text.slice(0, 1197) + "…" : text, where: sectionOf(range.startContainer) };
      pop = document.createElement("div");
      pop.className = "sel-pop";
      pop.dataset.text = text;
      const docW = document.documentElement.clientWidth;
      pop.style.left = Math.max(8, Math.min(r.right + scrollX + 6, docW + scrollX - 44)) + "px";
      pop.style.top = Math.max(scrollY + 4, r.top + scrollY - 38) + "px";
      pop.dataset.below = String(r.bottom + scrollY + 8);
      pop.innerHTML = `<button class="sel-btn" type="button" aria-label="Ask Claude about the selection">${icon("spark")}</button>`;
      document.body.appendChild(pop);
      pop.querySelector(".sel-btn").addEventListener("click", () => openMenu(quote));
    }

    function sectionOf(node) {
      const el = node.nodeType === 1 ? node : node.parentElement;
      let block = el;
      while (block && block.parentElement !== prose) block = block.parentElement;
      while (block && block.tagName !== "H2") block = block.previousElementSibling;
      return block ? "§ " + block.textContent.trim() : "the introduction";
    }

    function openMenu(quote) {
      const docW = document.documentElement.clientWidth;
      const width = Math.min(280, docW - 16);
      pop.dataset.menu = "1";
      pop.style.left = Math.max(8 + scrollX, Math.min(parseFloat(pop.style.left), docW + scrollX - width - 8)) + "px";
      pop.style.top = pop.dataset.below + "px";     // below the selection, away from the system's selection menu
      pop.innerHTML = `<div class="sel-menu" role="dialog" aria-label="Ask about the selection" style="width:${width}px">
        <button class="sel-explain" type="button">${icon("spark")}Explain this</button>
        <form><input id="sel-prompt" type="text" placeholder="Ask something else…" aria-label="Your question about the selection" autocomplete="off">
        <button class="send-btn" type="submit" aria-label="Ask" disabled>${icon("send")}</button></form></div>`;
      const field = pop.querySelector("input");
      const go = pop.querySelector(".send-btn");
      pop.querySelector(".sel-explain").focus();
      pop.querySelector(".sel-explain").addEventListener("click", () => { closePop(); ask("Explain this", quote); });
      field.addEventListener("input", () => { go.disabled = !field.value.trim(); });
      pop.querySelector("form").addEventListener("submit", (e) => {
        e.preventDefault();
        const v = field.value.trim();
        if (!v) return;
        closePop();
        ask(v, quote);
      });
    }
  }

  // ---------- Markdown and math in replies ----------

  let libs = null;
  function loadLibs() {
    if (libs) return libs;
    const load = (src) => new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src; s.onload = resolve; s.onerror = reject;
      document.head.appendChild(s);
    });
    libs = Promise.all([
      load("https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"),
      load("https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.1.6/purify.min.js"),
    ]).catch(() => null);
    return libs;
  }

  // Math is cut out before Markdown runs (Markdown would eat the backslashes) and put back after.
  function markdown(text) {
    const math = [];
    const guarded = String(text).replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]+?\$\$/g, (m) => {
      math.push(m);
      return `@@MATH${math.length - 1}@@`;
    });
    let html;
    if (window.marked && window.DOMPurify) {
      html = window.DOMPurify.sanitize(window.marked.parse(guarded, { gfm: true, breaks: false }));
      html = html.replace(/<table>/g, '<div class="table-wrap"><table>').replace(/<\/table>/g, "</table></div>");
    } else {
      html = guarded.split(/\n{2,}/).map((p) => `<p>${esc(p)}</p>`).join("");
    }
    return html.replace(/@@MATH(\d+)@@/g, (_, k) => esc(math[Number(k)].replace(/^\$\$([\s\S]*)\$\$$/, "\\[$1\\]")));
  }

  function typeset(el) { if (window.courseTypeset) window.courseTypeset(el); }
})();
