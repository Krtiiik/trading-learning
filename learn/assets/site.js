// Site chrome for the course (learn/DESIGN.md sections 3 and 5): theme toggle, phone drawer,
// TOC scroll spy, slider tables and KaTeX. Ask Claude lives in ask-claude.js, quiz logic in quiz.js.
(function () {
  const root = document.documentElement;
  const site = document.querySelector(".site");
  if (!site) return;

  // Theme: follows the OS until the reader picks one; the choice is stored per browser.
  const isDark = () => root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".theme-btn")) return;
    root.dataset.theme = isDark() ? "light" : "dark";
    try { localStorage.setItem("course-theme", root.dataset.theme); } catch (err) { /* storage blocked */ }
  });

  // Phone drawer (the course sidebar). Closes on scrim tap, Esc or a link tap.
  const setDrawer = (open) => {
    site.dataset.drawer = open ? "open" : "closed";
    document.querySelectorAll("[data-drawer-open]").forEach((b) => b.setAttribute("aria-expanded", String(open)));
  };
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-drawer-open]")) setDrawer(site.dataset.drawer !== "open");
    else if (e.target.closest("[data-scrim]") || (site.dataset.drawer === "open" && e.target.closest(".sidebar a"))) setDrawer(false);
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && site.dataset.drawer === "open") setDrawer(false); });

  // TOC rail: the section in view is the last h2 whose top is above 140px.
  const rail = document.querySelector("[data-toc]");
  if (rail) {
    const links = [...rail.querySelectorAll("a")];
    const heads = links.map((a) => document.getElementById(decodeURIComponent(a.hash.slice(1)))).filter(Boolean);
    let queued = false;
    const spy = () => {
      queued = false;
      let current = 0;
      heads.forEach((h, k) => { if (h.getBoundingClientRect().top < 140) current = k; });
      links.forEach((a, k) => a.setAttribute("aria-current", String(k === current)));
    };
    addEventListener("scroll", () => { if (!queued) { queued = true; requestAnimationFrame(spy); } }, { passive: true });
    spy();
  }

  // Slider tables (_includes/slider-table.html): the slider picks which row the table shows.
  document.querySelectorAll(".numeric-slider[data-rows]").forEach((box) => {
    const rows = JSON.parse(box.dataset.rows);
    const input = box.querySelector("input[type=range]");
    const out = box.querySelector("output");
    const cells = box.querySelectorAll("tbody td");
    const show = () => {
      const row = rows[Number(input.value)] || [];
      cells.forEach((td, k) => { td.textContent = row[k] ?? ""; });
      if (out) out.textContent = row[0] ?? "";
    };
    input.addEventListener("input", show);
    show();
  });

  // Math: kramdown writes $$…$$ as \( \) inline and \[ \] display. MathML output needs no KaTeX CSS or fonts.
  window.courseTypeset = function (el) {
    if (!window.renderMathInElement) return;
    window.renderMathInElement(el, {
      delimiters: [{ left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }],
      output: "mathml", throwOnError: false,
    });
  };
  const typesetPage = () => window.courseTypeset(document.querySelector(".content") || document.querySelector(".home") || document.body);
  if (window.renderMathInElement) typesetPage();
  else addEventListener("load", typesetPage);
})();
