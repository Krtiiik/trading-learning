// Behaviour for the learning site: link hover previews, search, the theme switch, and shelf arrows.
// Data comes from index.js (window.LEARNING_INDEX); URLs there are relative to the site root.
(function () {
  "use strict";
  var data = window.LEARNING_INDEX || { pages: [], groups: [] };
  var root = document.documentElement.getAttribute("data-root") || "";
  var bySlug = {};
  data.pages.forEach(function (p) { bySlug[p.slug] = p; });

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }

  // Hover preview on links to concepts and lessons (cards already show the summary).
  var preview = document.querySelector(".link-preview");
  function showPreview(link) {
    var p = bySlug[link.getAttribute("data-slug")];
    if (!p || !preview) return;
    preview.innerHTML = "";
    preview.appendChild(el("span", "link-preview__group", p.group || "Lesson"));
    preview.appendChild(el("strong", "link-preview__title", p.title));
    preview.appendChild(el("p", "link-preview__summary", p.summary));
    if (p.status === "planned") preview.appendChild(el("span", "link-preview__status", "Not written yet"));
    var r = link.getBoundingClientRect();
    var maxLeft = window.scrollX + document.documentElement.clientWidth - preview.offsetWidth - 8;
    preview.hidden = false;
    preview.style.left = Math.max(8, Math.min(r.left + window.scrollX, maxLeft)) + "px";
    preview.style.top = (r.bottom + window.scrollY + 6) + "px";
  }
  document.addEventListener("mouseover", function (e) {
    var link = e.target.closest && e.target.closest("a.concept-link");
    if (link) showPreview(link);
  });
  document.addEventListener("mouseout", function (e) {
    var link = e.target.closest && e.target.closest("a.concept-link");
    if (link && preview && !link.contains(e.relatedTarget)) preview.hidden = true;
  });

  // Search over titles, summaries and group names.
  var input = document.querySelector(".search__input");
  var results = document.querySelector(".search__results");
  if (input && results) {
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      results.innerHTML = "";
      if (!q) { results.hidden = true; return; }
      var inTitle = function (p) { return p.title.toLowerCase().indexOf(q) !== -1 ? 1 : 0; };
      var hits = data.pages.filter(function (p) {
        return (p.title + " " + p.summary + " " + (p.group || "lesson")).toLowerCase().indexOf(q) !== -1;
      }).sort(function (a, b) { return inTitle(b) - inTitle(a); }).slice(0, 12);
      hits.forEach(function (p) {
        var li = el("li", "search__result is-" + p.status);
        var a = el("a", "search__link");
        a.href = root + p.url;
        a.appendChild(el("strong", "search__title", p.title));
        a.appendChild(el("span", "search__meta", (p.group || "Lesson") + (p.status === "planned" ? " · not written yet" : "")));
        li.appendChild(a);
        results.appendChild(li);
      });
      if (!hits.length) results.appendChild(el("li", "search__empty", "No matches"));
      results.hidden = false;
    });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { input.value = ""; results.hidden = true; }
      if (e.key === "Enter") { var a = results.querySelector("a"); if (a) location.href = a.href; }
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".search")) results.hidden = true;
    });
  }

  // "/" focuses search from anywhere outside a text field.
  if (input) {
    document.addEventListener("keydown", function (e) {
      if (e.key !== "/" || e.ctrlKey || e.metaKey || e.altKey) return;
      var t = e.target;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      e.preventDefault();
      input.focus();
    });
  }

  // Theme switch: one button cycles System > Light > Dark. System removes data-theme
  // (prefers-color-scheme decides); Light and Dark set it.
  // The choice is kept in localStorage; the head script in base.html applies it before first paint.
  var themeButton = document.querySelector(".theme");
  var THEMES = ["system", "light", "dark"];
  var THEME_NAMES = { system: "System", light: "Light", dark: "Dark" };
  function nextTheme(choice) { return THEMES[(THEMES.indexOf(choice) + 1) % THEMES.length]; }
  function showTheme(choice) {
    if (!themeButton) return;
    themeButton.setAttribute("data-theme-current", choice);
    themeButton.setAttribute("aria-label",
      "Colour theme: " + THEME_NAMES[choice] + ". Change to " + THEME_NAMES[nextTheme(choice)]);
    themeButton.title = THEME_NAMES[choice] + " theme";
  }
  function setTheme(choice) {
    var d = document.documentElement;
    if (choice === "light" || choice === "dark") d.setAttribute("data-theme", choice);
    else { choice = "system"; d.removeAttribute("data-theme"); }
    try {
      if (choice === "system") localStorage.removeItem("learning-theme");
      else localStorage.setItem("learning-theme", choice);
    } catch (e) {}
    showTheme(choice);
  }
  showTheme(document.documentElement.getAttribute("data-theme") || "system");
  if (themeButton) {
    themeButton.addEventListener("click", function () {
      setTheme(nextTheme(themeButton.getAttribute("data-theme-current")));
    });
  }

  // Shelf arrows scroll the single card row by most of its visible width.
  // Arrows disable at either end; a shelf whose cards all fit gets .is-static (arrows hidden).
  document.documentElement.classList.add("js");
  document.querySelectorAll(".shelf").forEach(function (shelf) {
    var row = shelf.querySelector(".shelf__row");
    var prev = shelf.querySelector(".shelf__arrow--prev");
    var next = shelf.querySelector(".shelf__arrow--next");
    if (!row) return;
    function update() {
      var max = row.scrollWidth - row.clientWidth;
      if (prev) prev.disabled = row.scrollLeft <= 2;
      if (next) next.disabled = row.scrollLeft >= max - 2;
      shelf.classList.toggle("is-static", max <= 2);
    }
    shelf.querySelectorAll(".shelf__arrow").forEach(function (btn) {
      var dir = btn.classList.contains("shelf__arrow--prev") ? -1 : 1;
      btn.addEventListener("click", function () {
        row.scrollBy({ left: dir * row.clientWidth * 0.9, behavior: "smooth" });
      });
    });
    row.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  });
})();
