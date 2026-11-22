import importlib.util
import json
import re
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("learning_build", ROOT / "scripts" / "build.py")
build = importlib.util.module_from_spec(_spec)
sys.modules["learning_build"] = build
_spec.loader.exec_module(build)

CATALOG = """
groups:
  - slug: charts
    title: Charts
    blurb: Reading charts.
    concepts:
      - {slug: candle, title: Candle, summary: One bar of price.}
      - {slug: trend, title: Trend, summary: The general direction.}
      - {slug: wick, title: Wick, summary: The thin line.}
  - slug: assets
    title: Assets
    blurb: Things to trade.
    concepts:
      - {slug: stock, title: Stock, summary: A share of a company.}
"""

SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 400"></svg>'


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")


@pytest.fixture
def site_root(tmp_path: Path) -> Path:
    write(tmp_path, "catalog.yaml", CATALOG)
    write(tmp_path, "banners/_planned.svg", SVG)
    write(tmp_path, "banners/candle.svg", SVG)
    write(tmp_path, "content/concepts/charts/candle.md", "A candle has a [[wick]] and shows a [[trend|trending]] move.\n")
    return tmp_path


def add_lesson(
    root: Path, slug="first-chart", added="2026-11-20", builds_on="[candle]", body="Look at a [[candle]].", step=None
) -> None:
    write(root, f"banners/{slug}.svg", SVG)
    step_line = "" if step is None else f"step: {step}"
    write(
        root,
        f"content/lessons/{slug}.md",
        f"""
        ---
        title: First chart {slug}
        summary: Reading a chart.
        added: {added}
        builds_on: {builds_on}
        {step_line}
        ---
        {body}
        """,
    )


def test_concept_is_written_only_when_its_file_exists(site_root):
    site = build.load_site(site_root)
    assert site.pages["candle"].written
    assert not site.pages["trend"].written
    assert site.groups[0].written_count == 1


def test_links_resolve_with_custom_text_and_mark_planned_targets(site_root):
    site = build.load_site(site_root)
    html = build.render_body(site, site.pages["candle"], "../")
    assert '<a class="concept-link is-planned" data-slug="trend" href="../concepts/trend.html">trending</a>' in html
    assert 'data-slug="wick" href="../concepts/wick.html">wick</a>' in html


@pytest.mark.parametrize(
    "title, text",
    [("Price chart", "price chart"), ("OHLC", "OHLC"), ("RSI", "RSI"), ("ETF", "ETF"), ("Risk/reward", "risk/reward")],
)
def test_default_link_text_reads_mid_sentence(title, text):
    assert build.default_link_text(title) == text


def test_unknown_link_fails_the_build(site_root):
    write(site_root, "content/concepts/charts/candle.md", "See [[nonsense]].")
    with pytest.raises(build.BuildError, match=r"candle: links to unknown \[\[nonsense\]\]"):
        build.load_site(site_root)


def test_unquoted_comma_in_catalog_summary_fails_the_build(site_root):
    # In a YAML flow mapping, an unquoted comma ends the value and starts a new key,
    # so the summary would be cut off silently.
    catalog = CATALOG.replace("summary: The thin line.}", "summary: The thin line, above or below.}")
    write(site_root, "catalog.yaml", catalog)
    with pytest.raises(build.BuildError, match=r"wick: unknown catalog keys \['above or below.'\]"):
        build.load_site(site_root)


def test_word_count_counts_link_text_and_headings_but_not_tables_or_marks(site_root):
    body = """
    ## Two words

    - A **bold** [[wick]] and a [[trend|long trend]] at $40.50 — done.

    | Price | Volume |
    |---|---|
    | $40 | 100 |
    """
    write(site_root, "content/concepts/charts/candle.md", body)
    site = build.load_site(site_root)
    # "Two words" (2) + "A bold wick and a long trend at $40.50 done." (10)
    assert build.word_count(site, site.pages["candle"]) == 12


def test_written_page_needs_its_own_banner(site_root):
    (site_root / "banners/candle.svg").unlink()
    with pytest.raises(build.BuildError, match="no banner"):
        build.load_site(site_root)


def test_planned_concept_uses_the_shared_planned_banner(site_root):
    write(site_root, "banners/_planned.svg", "<svg id='planned'></svg>")
    site = build.load_site(site_root)
    assert site.pages["trend"].banner_svg == "<svg id='planned'></svg>"


def test_concept_file_must_be_in_catalog_and_in_its_group_folder(site_root):
    write(site_root, "content/concepts/charts/unknown.md", "x")
    write(site_root, "banners/stock.svg", SVG)
    write(site_root, "content/concepts/charts/stock.md", "x")
    with pytest.raises(build.BuildError) as e:
        build.load_site(site_root)
    assert any("unknown.md: concept is not in catalog" in p for p in e.value.problems)
    assert any("catalog puts stock in group assets" in p for p in e.value.problems)


def test_backlinks_collect_links_and_lesson_prerequisites(site_root):
    add_lesson(site_root, builds_on="[trend]", body="Look at a [[candle]].")
    site = build.load_site(site_root)
    assert site.pages["wick"].backlinks == ["candle"]
    assert site.pages["trend"].backlinks == ["first-chart", "candle"]  # lessons first
    assert site.pages["candle"].backlinks == ["first-chart"]
    assert site.pages["first-chart"].links == ["candle"]


def test_lessons_are_sorted_newest_first(site_root):
    add_lesson(site_root, slug="older", added="2026-01-01")
    add_lesson(site_root, slug="newer", added="2026-06-01")
    site = build.load_site(site_root)
    assert [p.slug for p in site.lessons] == ["newer", "older"]


def test_path_lessons_come_first_in_step_order_then_the_rest_newest_first(site_root):
    add_lesson(site_root, slug="side-old", added="2026-01-01")
    add_lesson(site_root, slug="side-new", added="2026-06-01")
    add_lesson(site_root, slug="second", added="2026-09-01", step=2)
    add_lesson(site_root, slug="first", added="2026-02-01", step=1)
    site = build.load_site(site_root)
    assert [p.slug for p in site.lessons] == ["first", "second", "side-new", "side-old"]


def test_each_path_lesson_points_to_the_next_step(site_root):
    add_lesson(site_root, slug="first", step=1)
    add_lesson(site_root, slug="second", step=2)
    add_lesson(site_root, slug="side")
    site = build.load_site(site_root)
    assert site.pages["first"].next_lesson == "second"
    assert site.pages["second"].next_lesson is None
    assert site.pages["side"].next_lesson is None


def test_lesson_page_lists_linked_lessons_apart_from_concepts(site_root, tmp_path):
    add_lesson(site_root, slug="first", step=1)
    add_lesson(site_root, slug="second", step=2, body="After [[first]], look at a [[candle]].")
    out = tmp_path / "dist"
    build.build(site_root, out)
    second = (out / "lessons" / "second.html").read_text(encoding="utf-8")
    lessons_used = second[second.index("<h2>Lessons used</h2>"):second.index("<h2>Concepts used</h2>")]
    concepts_used = second[second.index("<h2>Concepts used</h2>"):]
    assert 'href="../lessons/first.html"' in lessons_used and "candle" not in lessons_used
    assert 'href="../concepts/candle.html"' in concepts_used and "first.html" not in concepts_used
    assert '<a class="article__group" href="../lessons/index.html">Lessons</a>' in second


def test_nav_marks_the_current_page_and_the_section_of_a_child_page(site_root, tmp_path):
    add_lesson(site_root)
    out = tmp_path / "dist"
    build.build(site_root, out)
    def nav(rel):
        page = (out / rel).read_text(encoding="utf-8")
        return page[page.index('<nav class="site-nav"'):page.index("</nav>")]
    assert 'lessons/index.html" aria-current="page"' in nav("lessons/index.html")
    assert 'lessons/index.html" aria-current="true"' in nav("lessons/first-chart.html")
    assert 'aria-current="page"' not in nav("lessons/first-chart.html")
    assert 'aria-current="true"' in nav("concepts/candle.html") and 'aria-current="page"' not in nav("concepts/candle.html")


def test_search_index_lists_lessons_first_with_their_step(site_root, tmp_path):
    add_lesson(site_root, step=1)
    out = tmp_path / "dist"
    build.build(site_root, out)
    index_js = (out / "static/index.js").read_text(encoding="utf-8")
    data = json.loads(index_js.removeprefix("window.LEARNING_INDEX = ").rstrip(";\n"))
    assert data["pages"][0]["kind"] == "lesson" and data["pages"][0]["step"] == 1
    assert all("step" not in p for p in data["pages"] if p["kind"] == "concept")


def test_lesson_steps_must_be_unique_positive_numbers(site_root):
    add_lesson(site_root, slug="one", step=1)
    add_lesson(site_root, slug="also-one", step=1)
    add_lesson(site_root, slug="zero", step=0)
    with pytest.raises(build.BuildError) as e:
        build.load_site(site_root)
    assert any("one: step 1 is already used by also-one" in p for p in e.value.problems)
    assert any("zero.md: step must be a whole number from 1" in p for p in e.value.problems)


def test_lesson_page_links_to_the_next_lesson(site_root, tmp_path):
    add_lesson(site_root, slug="first", step=1)
    add_lesson(site_root, slug="second", step=2)
    out = tmp_path / "dist"
    build.build(site_root, out)
    first = (out / "lessons" / "first.html").read_text(encoding="utf-8")
    second = (out / "lessons" / "second.html").read_text(encoding="utf-8")
    assert 'class="next-lesson"' in first and 'href="../lessons/second.html"' in first
    assert 'class="next-lesson"' not in second


def test_lesson_needs_frontmatter_and_known_prerequisites(site_root):
    add_lesson(site_root, builds_on="[ghost]")
    write(site_root, "content/lessons/bare.md", "No frontmatter.")
    with pytest.raises(build.BuildError) as e:
        build.load_site(site_root)
    assert any("builds_on names unknown concept ghost" in p for p in e.value.problems)
    assert any("bare.md: missing" in p for p in e.value.problems)


def test_lesson_slug_cannot_reuse_a_concept_slug(site_root):
    add_lesson(site_root, slug="trend")
    with pytest.raises(build.BuildError, match="already used by a concept"):
        build.load_site(site_root)


def test_build_writes_every_page_and_the_index(site_root, tmp_path):
    add_lesson(site_root)
    out = tmp_path / "dist"
    build.build(site_root, out)
    for rel in ["index.html", "groups/charts.html", "groups/assets.html", "lessons/index.html",
                "lessons/first-chart.html", "concepts/candle.html", "concepts/trend.html",
                "static/site.css", "static/site.js"]:
        assert (out / rel).is_file(), rel
    index_js = (out / "static/index.js").read_text(encoding="utf-8")
    data = json.loads(index_js.removeprefix("window.LEARNING_INDEX = ").rstrip(";\n"))
    by_slug = {p["slug"]: p for p in data["pages"]}
    assert by_slug["trend"] == {"slug": "trend", "kind": "concept", "title": "Trend",
                                "summary": "The general direction.", "url": "concepts/trend.html",
                                "status": "planned", "group": "Charts",
                                "banner": by_slug["trend"]["banner"]}
    assert by_slug["first-chart"]["kind"] == "lesson"


def test_index_lists_each_banner_once_for_the_hover_preview(site_root, tmp_path):
    write(site_root, "banners/_planned.svg", "<svg id='planned'>\n  <!-- note -->\n  <rect/>\n</svg>")
    write(site_root, "banners/candle.svg", "<svg id='candle'><rect/></svg>")
    out = tmp_path / "dist"
    build.build(site_root, out)
    index_js = (out / "static/index.js").read_text(encoding="utf-8")
    data = json.loads(index_js.removeprefix("window.LEARNING_INDEX = ").rstrip(";\n"))
    by_slug = {p["slug"]: p for p in data["pages"]}
    assert data["banners"][by_slug["candle"]["banner"]] == "<svg id='candle'><rect/></svg>"
    assert data["banners"][by_slug["trend"]["banner"]] == "<svg id='planned'> <rect/> </svg>"
    planned = [p["banner"] for p in data["pages"] if p["status"] == "planned"]
    assert len(set(planned)) == 1
    assert len(data["banners"]) == len(set(data["banners"]))


def test_pages_use_root_relative_prefixes(site_root, tmp_path):
    out = tmp_path / "dist"
    build.build(site_root, out)
    home = (out / "index.html").read_text(encoding="utf-8")
    concept = (out / "concepts/candle.html").read_text(encoding="utf-8")
    assert 'data-root=""' in home and 'href="static/site.css"' in home
    assert 'data-root="../"' in concept and 'href="../static/site.css"' in concept


def test_home_shows_lessons_groups_and_concepts_in_one_row_over_a_hidden_chart(site_root, tmp_path):
    out = tmp_path / "dist"
    build.build(site_root, out)
    home = (out / "index.html").read_text(encoding="utf-8")
    stats = home[home.index('<dl class="stats">'):home.index("</dl>")]
    assert re.findall(r"<dt>([^<]+)</dt>", stats) == ["Lessons", "Groups", "Concepts"]
    assert 'class="wide"' not in stats
    panel = home[home.index('<div class="intro__panel">'):home.index('<dl class="stats">')]
    assert '<svg class="ticker"' in panel and 'aria-hidden="true"' in panel


def test_lessons_come_first_in_the_nav_and_footer(site_root, tmp_path):
    out = tmp_path / "dist"
    build.build(site_root, out)
    for rel in ["index.html", "concepts/candle.html", "lessons/index.html"]:
        page = (out / rel).read_text(encoding="utf-8")
        nav = page[page.index('<nav class="site-nav"'):page.index("</nav>")]
        assert re.findall(r">([^<]+)</a>", nav)[0] == "Lessons", rel
        footer = page[page.index('<footer class="site-footer">'):page.index("</footer>")]
        assert re.search(r"<span>\d+ lessons? · \d+ concepts</span>", footer), rel


def test_every_page_has_the_theme_switch_and_applies_the_saved_theme_early(site_root, tmp_path):
    out = tmp_path / "dist"
    build.build(site_root, out)
    for rel in ["index.html", "concepts/candle.html", "lessons/index.html"]:
        page = (out / rel).read_text(encoding="utf-8")
        assert page.count('class="theme"') == 1, rel
        for choice in ["system", "light", "dark"]:
            assert f"theme__icon--{choice}" in page, (rel, choice)
        head = page.split("</head>")[0]
        assert "learning-theme" in head, rel
        assert head.index("learning-theme") < head.index("site.css"), rel


def test_cards_put_written_concepts_before_planned_ones(site_root):
    write(site_root, "banners/wick.svg", SVG)
    write(site_root, "content/concepts/charts/wick.md", "x")
    site = build.load_site(site_root)
    order = [p.slug for p in build._cards(site.groups[0].concepts)]
    assert order == ["candle", "wick", "trend"]


def test_real_site_builds(tmp_path):
    build.build(ROOT, tmp_path / "dist")


def test_stylesheet_has_no_control_characters():
    css = (ROOT / "static" / "site.css").read_text(encoding="utf-8")
    bad = [hex(ord(c)) for c in css if ord(c) < 32 and c not in "\n\r\t"]
    assert bad == []
