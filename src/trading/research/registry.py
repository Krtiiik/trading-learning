"""The hypothesis registry: one Markdown file per hypothesis, with structured front matter.

Registration means the file is committed before any test runs. Everything in the front matter
except a few bookkeeping fields is frozen at that commit: the harness compares the file with
the version first committed and refuses to run when the prediction, the test or the decision
rule has changed. A changed test is a new hypothesis.
"""

import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

FAMILIES = ("time-series", "cross-sectional", "derivatives", "cross-market")
ORIGINS = ("literature", "exploration")
CLAIMS = ("trading", "predictive")
DIRECTIONS = ("positive", "negative")

MUTABLE_FIELDS = ("status", "skeptic")
"""Front-matter fields that may change after registration; all others are frozen."""

REQUIRED_FIELDS = (
    "id",
    "title",
    "family",
    "origin",
    "claim",
    "motivation",
    "sources",
    "prediction",
    "primary_test",
    "decision",
    "power",
    "data",
    "status",
)

_ID = re.compile(r"^H\d{4}$")
_FRONT_MATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", re.DOTALL)


class RegistryError(Exception):
    """A hypothesis file is missing, malformed, unregistered or changed since registration."""


@dataclass(frozen=True)
class Hypothesis:
    path: Path
    meta: dict[str, Any]
    body: str

    @property
    def id(self) -> str:
        return self.meta["id"]

    @property
    def title(self) -> str:
        return self.meta["title"]

    @property
    def family(self) -> str:
        return self.meta["family"]

    @property
    def origin(self) -> str:
        return self.meta["origin"]

    @property
    def claim(self) -> str:
        return self.meta["claim"]

    @property
    def direction(self) -> str:
        return self.meta["prediction"]["direction"]

    @property
    def experiment(self) -> str:
        return self.meta["primary_test"]["experiment"]

    @property
    def params(self) -> dict[str, Any]:
        return dict(self.meta["primary_test"].get("params") or {})

    @property
    def dev_rule(self) -> dict[str, float]:
        return dict(self.meta["decision"]["dev"])

    @property
    def predictors(self) -> list[str]:
        """For a model: the hypotheses whose predictors it uses (each must be a candidate)."""
        return list(self.meta.get("predictors") or [])

    @property
    def skeptic(self) -> dict[str, Any] | None:
        return self.meta.get("skeptic") or None

    @property
    def spec_hash(self) -> str:
        """Hash of the frozen front matter: the registration this hypothesis stands for."""
        return spec_hash(self.meta)


def spec_hash(meta: dict[str, Any]) -> str:
    frozen = {key: value for key, value in meta.items() if key not in MUTABLE_FIELDS}
    canonical = json.dumps(frozen, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(canonical.encode()).hexdigest()


def parse(text: str, path: Path) -> Hypothesis:
    match = _FRONT_MATTER.match(text)
    if not match:
        raise RegistryError(f"{path.name}: no front matter between --- lines")
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        raise RegistryError(f"{path.name}: front matter is not valid YAML: {error}") from error
    if not isinstance(meta, dict):
        raise RegistryError(f"{path.name}: front matter must be a mapping")
    return Hypothesis(path, meta, match.group(2))


def validate(hypothesis: Hypothesis) -> list[str]:
    """Everything wrong with a hypothesis file's structure; empty when it can be registered."""
    meta, problems = hypothesis.meta, []
    missing = [name for name in REQUIRED_FIELDS if meta.get(name) in (None, "", [], {})]
    if missing:
        return [f"missing front-matter fields: {', '.join(missing)}"]
    if not _ID.match(str(meta["id"])):
        problems.append("id must look like H0001")
    elif not hypothesis.path.name.startswith(f"{meta['id']}-"):
        problems.append(f"file name must start with {meta['id']}-")
    for name, allowed in (("family", FAMILIES), ("origin", ORIGINS), ("claim", CLAIMS)):
        if meta[name] not in allowed:
            problems.append(f"{name} must be one of: {', '.join(allowed)}")
    prediction, test, decision = meta["prediction"], meta["primary_test"], meta["decision"]
    if not isinstance(prediction, dict) or prediction.get("direction") not in DIRECTIONS:
        problems.append("prediction.direction must be positive or negative")
    elif not prediction.get("size") or not prediction.get("unit"):
        problems.append("prediction needs a rough size and the unit of the estimate")
    if not isinstance(test, dict) or not test.get("experiment") or not test.get("description"):
        problems.append("primary_test needs an experiment module and a description")
    if not isinstance(decision, dict) or not decision.get("train") or "dev" not in decision:
        problems.append("decision needs a train rule and a dev rule")
    else:
        dev = decision["dev"]
        if not isinstance(dev, dict) or not _is_number(dev.get("min_size")):
            problems.append("decision.dev.min_size must be a number in the estimate's unit")
        elif meta["origin"] == "literature" and not _is_number(dev.get("min_ratio")):
            problems.append("decision.dev.min_ratio must be a number (share of the train estimate)")
    if not isinstance(meta["sources"], list):
        problems.append("sources must be a list")
    if not isinstance(meta["data"], list):
        problems.append("data must be a list of dataset names")
    return problems


def hypotheses_dir(records: Path) -> Path:
    return records / "hypotheses"


def load_all(records: Path) -> list[Hypothesis]:
    files = sorted(hypotheses_dir(records).glob("H[0-9][0-9][0-9][0-9]-*.md"))
    return [parse(path.read_text(encoding="utf-8"), path) for path in files]


def load(records: Path, hypothesis_id: str) -> Hypothesis:
    matches = sorted(hypotheses_dir(records).glob(f"{hypothesis_id}-*.md"))
    if len(matches) != 1:
        found = "no file" if not matches else f"{len(matches)} files"
        raise RegistryError(f"{found} for {hypothesis_id} in {hypotheses_dir(records)}")
    return parse(matches[0].read_text(encoding="utf-8"), matches[0])


def set_field(hypothesis: Hypothesis, name: str, value: Any) -> Hypothesis:
    """Rewrite one mutable front-matter field in the file, leaving everything else untouched."""
    if name not in MUTABLE_FIELDS:
        raise RegistryError(f"{name} is frozen at registration")
    text = hypothesis.path.read_text(encoding="utf-8")
    match = _FRONT_MATTER.match(text)
    assert match is not None
    lines = match.group(1).splitlines()
    start = next((i for i, line in enumerate(lines) if re.match(rf"^{name}\s*:", line)), None)
    if start is not None:
        stop = start + 1
        while stop < len(lines) and (lines[stop].startswith((" ", "\t")) or not lines[stop].strip()):
            stop += 1
        del lines[start:stop]
    dumped = yaml.safe_dump({name: value}, sort_keys=False, allow_unicode=True, width=88)
    lines += dumped.rstrip("\n").splitlines()
    hypothesis.path.write_text(
        "---\n" + "\n".join(lines) + "\n---\n" + match.group(2), encoding="utf-8", newline="\n"
    )
    return parse(hypothesis.path.read_text(encoding="utf-8"), hypothesis.path)


# Git: registration is proven by history, not by anyone's word.


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments], capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        raise RegistryError(f"git {' '.join(arguments)} failed: {result.stderr.strip()}")
    return result.stdout


def repository_root(path: Path) -> Path:
    return Path(git(path if path.is_dir() else path.parent, "rev-parse", "--show-toplevel").strip())


def head_commit(root: Path) -> str:
    return git(root, "rev-parse", "HEAD").strip()


def registered_spec_hash(hypothesis: Hypothesis) -> tuple[str, str]:
    """The spec hash and commit of the file's first committed version. Raises when uncommitted."""
    root = repository_root(hypothesis.path)
    relative = hypothesis.path.resolve().relative_to(root.resolve()).as_posix()
    commits = git(root, "log", "--diff-filter=A", "--format=%H", "--", relative).split()
    if not commits:
        raise RegistryError(
            f"{hypothesis.id} is not registered: commit {relative} before running anything"
        )
    first = commits[-1]
    original = parse(git(root, "show", f"{first}:{relative}"), hypothesis.path)
    return original.spec_hash, first


def check_registered(hypothesis: Hypothesis) -> str:
    """The registration commit, after checking the frozen fields are what was registered."""
    problems = validate(hypothesis)
    if problems:
        raise RegistryError(f"{hypothesis.id}: " + "; ".join(problems))
    registered, commit = registered_spec_hash(hypothesis)
    if registered != hypothesis.spec_hash:
        raise RegistryError(
            f"{hypothesis.id} has changed since it was registered in {commit[:10]}: its frozen "
            "fields (prediction, test, decision rule, motivation, data) no longer match. "
            "A changed test is a new hypothesis: restore the file and register a new one."
        )
    return commit


def uncommitted(root: Path, paths: list[Path]) -> list[str]:
    """Which of `paths` are untracked or differ from the last commit."""
    changed = set()
    for line in git(root, "status", "--porcelain", "--untracked-files=all").splitlines():
        changed.add(line[3:].split(" -> ")[-1].strip().strip('"'))
    dirty = []
    for path in paths:
        try:
            relative = path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            continue
        if relative in changed:
            dirty.append(relative)
    return sorted(dirty)


def _is_number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool)
