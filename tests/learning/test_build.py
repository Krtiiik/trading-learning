import importlib.util
import json
import sys
import textwrap
from pathlib import Path

import pytest

LEARNING = Path(__file__).resolve().parents[2] / "learning"
_spec = importlib.util.spec_from_file_location("learning_build", LEARNING / "build.py")
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


def add_lesson(root: Path, slug="first-chart", added="2026-11-20", builds_on="[candle]", body="Look at a [[candle]].") -> None:
    write(root, f"banners/{slug}.svg", SVG)
    write(
        root,
        f"content/lessons/{slug}.md",
        f"""
        ---
        title: First chart {slug}
        summary: Reading a chart.
        added: {added}
        builds_on: {builds_on}
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
    assert site.pages["trend"].backlinks == ["candle", "first-chart"]
    assert site.pages["candle"].backlinks == ["first-chart"]
    assert site.pages["first-chart"].links == ["candle"]


def test_lessons_are_sorted_newest_first(site_root):
    add_lesson(site_root, slug="older", added="2026-01-01")
    add_lesson(site_root, slug="newer", added="2026-06-01")
    site = build.load_site(site_root)
    assert [p.slug for p in site.lessons] == ["newer", "older"]


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
                                "status": "planned", "group": "Charts"}
    assert by_slug["first-chart"]["kind"] == "lesson"


def test_pages_use_root_relative_prefixes(site_root, tmp_path):
    out = tmp_path / "dist"
    build.build(site_root, out)
    home = (out / "index.html").read_text(encoding="utf-8")
    concept = (out / "concepts/candle.html").read_text(encoding="utf-8")
    assert 'data-root=""' in home and 'href="static/site.css"' in home
    assert 'data-root="../"' in concept and 'href="../static/site.css"' in concept


def test_cards_put_written_concepts_before_planned_ones(site_root):
    write(site_root, "banners/wick.svg", SVG)
    write(site_root, "content/concepts/charts/wick.md", "x")
    site = build.load_site(site_root)
    order = [p.slug for p in build._cards(site.groups[0].concepts)]
    assert order == ["candle", "wick", "trend"]


def test_publish_files_lists_everything_but_the_home_page(site_root, tmp_path):
    out = tmp_path / "dist"
    build.build(site_root, out)
    paths = [f["path"] for f in build.publish_files(out)]
    assert "index.html" not in paths
    assert {"concepts/candle.html", "lessons/index.html", "static/index.js"} <= set(paths)


def test_real_site_builds(tmp_path):
    build.build(LEARNING, tmp_path / "dist")
