"""Build the learning site from Markdown sources into static HTML pages.

Usage: uv run python learning/build.py [--out DIR]

Sources (all under learning/):
  catalog.yaml                         concept groups and every concept's title and summary
  content/concepts/<group>/<slug>.md   body of a written concept (no frontmatter)
  content/lessons/<slug>.md            a lesson: YAML frontmatter, then the body
  banners/<slug>.svg                   banner of a written concept or lesson
  banners/_planned.svg                 shared banner of planned concepts
  templates/, static/                  page templates (Jinja2) and assets copied to dist/static/

Links in bodies are written [[slug]] or [[slug|text]] and must name a concept or lesson.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

HERE = Path(__file__).resolve().parent
LINK = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LESSON_KEYS = {"title", "summary", "added", "builds_on"}
PLANNED_BANNER = "_planned"


class BuildError(Exception):
    """The sources are inconsistent; carries every problem found, not just the first."""

    def __init__(self, problems: list[str]):
        self.problems = problems
        super().__init__("\n".join(problems))


@dataclass
class Page:
    kind: str  # "concept" or "lesson"
    slug: str
    title: str
    summary: str
    url: str  # relative to the site root
    written: bool
    body_md: str = ""
    banner_svg: str = ""
    group: Group | None = None
    added: dt.date | None = None
    builds_on: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)  # slugs linked from the body, in order, unique
    backlinks: list[str] = field(default_factory=list)  # slugs of pages linking here

    @property
    def status(self) -> str:
        return "written" if self.written else "planned"


@dataclass
class Group:
    slug: str
    title: str
    blurb: str
    url: str
    concepts: list[Page] = field(default_factory=list)

    @property
    def written_count(self) -> int:
        return sum(c.written for c in self.concepts)


@dataclass
class Site:
    groups: list[Group]
    lessons: list[Page]  # newest first
    pages: dict[str, Page]  # every concept and lesson by slug


def _read_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = re.split(r"^---[ \t]*$", text, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        raise ValueError("frontmatter is not closed with ---")
    meta = yaml.safe_load(parts[1]) or {}
    return meta, parts[2].lstrip("\n")


def _ordered_unique(items):
    return list(dict.fromkeys(items))


def load_site(root: Path) -> Site:
    """Read the catalog, content and banners under root, and check they agree."""
    problems: list[str] = []
    catalog = yaml.safe_load((root / "catalog.yaml").read_text(encoding="utf-8"))
    banners = root / "banners"
    planned_banner = (banners / f"{PLANNED_BANNER}.svg")
    planned_svg = planned_banner.read_text(encoding="utf-8") if planned_banner.exists() else ""
    if not planned_svg:
        problems.append(f"missing shared planned banner banners/{PLANNED_BANNER}.svg")

    def banner_for(slug: str, written: bool) -> str:
        if not written:
            return planned_svg
        path = banners / f"{slug}.svg"
        if not path.exists():
            problems.append(f"{slug}: written page has no banner banners/{slug}.svg")
            return planned_svg
        return path.read_text(encoding="utf-8")

    pages: dict[str, Page] = {}
    groups: list[Group] = []
    concepts_dir = root / "content" / "concepts"
    for g in catalog["groups"]:
        group = Group(g["slug"], g["title"], g.get("blurb", ""), f"groups/{g['slug']}.html")
        groups.append(group)
        for c in g["concepts"]:
            slug = c["slug"]
            if not SLUG.match(slug):
                problems.append(f"{slug}: slug must be lowercase words joined by hyphens")
            if slug in pages:
                problems.append(f"{slug}: listed twice in the catalog")
                continue
            source = concepts_dir / group.slug / f"{slug}.md"
            written = source.exists()
            page = Page(
                kind="concept",
                slug=slug,
                title=c["title"],
                summary=c["summary"],
                url=f"concepts/{slug}.html",
                written=written,
                group=group,
                body_md=source.read_text(encoding="utf-8") if written else "",
            )
            page.banner_svg = banner_for(slug, written)
            pages[slug] = page
            group.concepts.append(page)

    if concepts_dir.exists():
        for source in sorted(concepts_dir.glob("*/*.md")):
            slug, group_slug = source.stem, source.parent.name
            page = pages.get(slug)
            if page is None:
                problems.append(f"{source.relative_to(root).as_posix()}: concept is not in catalog.yaml")
            elif page.group.slug != group_slug:
                problems.append(
                    f"{source.relative_to(root).as_posix()}: catalog puts {slug} in group {page.group.slug}"
                )

    lessons: list[Page] = []
    lessons_dir = root / "content" / "lessons"
    for source in sorted(lessons_dir.glob("*.md")) if lessons_dir.exists() else []:
        slug = source.stem
        where = source.relative_to(root).as_posix()
        if not SLUG.match(slug) or slug == "index":
            problems.append(f"{where}: invalid lesson slug")
            continue
        if slug in pages:
            problems.append(f"{where}: slug {slug} is already used by a concept")
            continue
        try:
            meta, body = _read_frontmatter(source.read_text(encoding="utf-8"))
        except (ValueError, yaml.YAMLError) as e:
            problems.append(f"{where}: {e}")
            continue
        missing = {"title", "summary", "added"} - meta.keys()
        unknown = meta.keys() - LESSON_KEYS
        if missing or unknown:
            problems.append(f"{where}: missing {sorted(missing)} unknown {sorted(unknown)} frontmatter keys")
            continue
        added = meta["added"]
        if not isinstance(added, dt.date):
            problems.append(f"{where}: added must be a date like 2026-11-20")
            continue
        page = Page(
            kind="lesson",
            slug=slug,
            title=meta["title"],
            summary=meta["summary"],
            url=f"lessons/{slug}.html",
            written=True,
            body_md=body,
            added=added,
            builds_on=list(meta.get("builds_on") or []),
        )
        page.banner_svg = banner_for(slug, True)
        pages[slug] = page
        lessons.append(page)
    lessons.sort(key=lambda p: (p.added, p.slug), reverse=True)

    for page in pages.values():
        page.links = _ordered_unique(m.group(1).strip() for m in LINK.finditer(page.body_md))
        for slug in page.links:
            if slug not in pages:
                problems.append(f"{page.slug}: links to unknown [[{slug}]]")
        for slug in page.builds_on:
            if pages.get(slug, None) is None or pages[slug].kind != "concept":
                problems.append(f"{page.slug}: builds_on names unknown concept {slug}")
    for page in pages.values():
        for slug in _ordered_unique([*page.builds_on, *page.links]):
            if slug in pages and slug != page.slug:
                pages[slug].backlinks.append(page.slug)

    if problems:
        raise BuildError(problems)
    return Site(groups, lessons, pages)


def default_link_text(title: str) -> str:
    """A title as it reads mid-sentence: 'Price chart' -> 'price chart', but 'OHLC' and 'RSI' stay."""
    first = title.split()[0]
    if len(first) > 1 and first[1].isupper():
        return title
    return title[:1].lower() + title[1:]


def _link_html(site: Site, root_prefix: str):
    def replace(m: re.Match) -> str:
        slug = m.group(1).strip()
        page = site.pages[slug]
        text = (m.group(2) or default_link_text(page.title)).strip()
        return (
            f'<a class="concept-link is-{page.status}" data-slug="{slug}" '
            f'href="{root_prefix}{page.url}">{text}</a>'
        )

    return replace


def render_body(site: Site, page: Page, root_prefix: str) -> str:
    linked = LINK.sub(_link_html(site, root_prefix), page.body_md)
    return markdown.markdown(linked, extensions=["tables", "fenced_code", "sane_lists"])


def site_index(site: Site) -> dict:
    """The data behind hover previews and search, with URLs relative to the site root."""

    def entry(p: Page) -> dict:
        d = {"slug": p.slug, "kind": p.kind, "title": p.title, "summary": p.summary,
             "url": p.url, "status": p.status}
        if p.group:
            d["group"] = p.group.title
        return d

    return {
        "groups": [{"slug": g.slug, "title": g.title, "url": g.url} for g in site.groups],
        "pages": [entry(p) for p in site.pages.values()],
    }


def _cards(pages: list[Page]) -> list[Page]:
    """Written pages first, then planned ones, each in catalog order."""
    return [p for p in pages if p.written] + [p for p in pages if not p.written]


def render_site(site: Site, out: Path, templates: Path, static: Path) -> list[Path]:
    env = Environment(
        loader=FileSystemLoader(templates),
        undefined=StrictUndefined,
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    written: list[Path] = []

    def emit(rel: str, template: str, **ctx) -> None:
        depth = rel.count("/")
        root_prefix = "../" * depth
        html = env.get_template(template).render(
            site=site, root=root_prefix, current=rel, cards=_cards, **ctx
        )
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        written.append(path)

    emit("index.html", "home.html", title="Home")
    for group in site.groups:
        emit(group.url, "group.html", title=group.title, group=group)
    emit("lessons/index.html", "lessons.html", title="Lessons")
    for page in site.pages.values():
        rel = page.url
        prefix = "../" * rel.count("/")
        body = render_body(site, page, prefix) if page.written else ""
        template = "concept.html" if page.kind == "concept" else "lesson.html"
        emit(rel, template, title=page.title, page=page, body=body)

    static_out = out / "static"
    shutil.copytree(static, static_out)
    index_js = static_out / "index.js"
    index_js.write_text(
        "window.LEARNING_INDEX = " + json.dumps(site_index(site), ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )
    written.extend(p for p in static_out.rglob("*") if p.is_file())
    return written


def build(root: Path = HERE, out: Path | None = None) -> Site:
    out = out or root / "dist"
    site = load_site(root)
    render_site(site, out, HERE / "templates", HERE / "static")
    return site


def publish_files(out: Path) -> list[dict]:
    """Every built file except the home page, as the `files` list of an Artifact publish rooted at out."""
    return [
        {"path": p.relative_to(out).as_posix()}
        for p in sorted(out.rglob("*"))
        if p.is_file() and p != out / "index.html"
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=HERE / "dist")
    parser.add_argument("--files-json", action="store_true",
                        help="after building, print the Artifact `files` list as JSON on stdout")
    args = parser.parse_args(argv)
    try:
        site = build(HERE, args.out)
    except BuildError as e:
        print("Build failed:", file=sys.stderr)
        for p in e.problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    if args.files_json:
        print(json.dumps(publish_files(args.out)))
        return 0
    concepts = [p for p in site.pages.values() if p.kind == "concept"]
    print(
        f"Built {args.out}: {sum(p.written for p in concepts)}/{len(concepts)} concepts written, "
        f"{len(site.lessons)} lessons."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
