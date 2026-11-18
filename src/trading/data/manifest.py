"""Dataset identity: a manifest of content hashes for every file of a Store dataset.

A dataset is one directory of Parquet files under the Store root (`binance/spot/1d`, or `1d`
for the Yahoo ETF bars). Its manifest gives it an id, so a run can record exactly which data
it used and a later reader can tell whether the Store still holds that data.
"""

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

MANIFEST_NAME = "MANIFEST.json"


class ManifestError(Exception):
    """A dataset has no manifest, or its files no longer match it."""


@dataclass(frozen=True)
class FileEntry:
    content_hash: str
    rows: int
    first: str
    last: str
    size: int
    mtime_ns: int
    source_files: int = 0
    source_digest: str = ""
    """How many provider files the rows came from, and a digest of their names and checksums."""


@dataclass(frozen=True)
class Manifest:
    dataset: str
    id: str
    provider: str
    built_at: str
    files: dict[str, FileEntry] = field(default_factory=dict)

    @property
    def short_id(self) -> str:
        return self.id[:12]


def content_hash(frame: pd.DataFrame) -> str:
    """A hash of a frame's values, index, column names and types, independent of file encoding."""
    digest = hashlib.sha256()
    digest.update(repr([(str(name), str(dtype)) for name, dtype in frame.dtypes.items()]).encode())
    digest.update(f"{frame.index.name}:{frame.index.dtype}".encode())
    digest.update(pd.util.hash_pandas_object(frame, index=True).to_numpy().tobytes())
    return digest.hexdigest()


def source_digest(names_and_checksums: list[tuple[str, str]]) -> str:
    lines = "\n".join(f"{name}:{checksum}" for name, checksum in sorted(names_and_checksums))
    return hashlib.sha256(lines.encode()).hexdigest()


def build_manifest(
    root: Path,
    dataset: str,
    provider: str,
    sources: dict[str, list[tuple[str, str]]] | None = None,
) -> Manifest:
    """Hash every Parquet file directly inside `<root>/<dataset>` and write the manifest there.

    `sources` maps a file name to the provider files (name, checksum) its rows came from.
    """
    directory = Path(root) / dataset
    files: dict[str, FileEntry] = {}
    for path in sorted(directory.glob("*.parquet")):
        frame = pd.read_parquet(path)
        stat = path.stat()
        origin = (sources or {}).get(path.name, [])
        files[path.name] = FileEntry(
            content_hash=content_hash(frame),
            rows=len(frame),
            first=str(frame.index[0]) if len(frame) else "",
            last=str(frame.index[-1]) if len(frame) else "",
            size=stat.st_size,
            mtime_ns=stat.st_mtime_ns,
            source_files=len(origin),
            source_digest=source_digest(origin) if origin else "",
        )
    if not files:
        raise ManifestError(f"dataset {dataset!r} has no Parquet files in {directory}")
    manifest = Manifest(
        dataset=dataset,
        id=_identity(files),
        provider=provider,
        built_at=datetime.now(UTC).isoformat(timespec="seconds"),
        files=files,
    )
    (directory / MANIFEST_NAME).write_text(json.dumps(asdict(manifest), indent=1), encoding="utf-8")
    return manifest


def read_manifest(root: Path, dataset: str) -> Manifest:
    path = Path(root) / dataset / MANIFEST_NAME
    if not path.is_file():
        raise ManifestError(
            f"dataset {dataset!r} has no manifest in {path.parent}; run `uv run trading rebuild`"
        )
    raw = json.loads(path.read_text(encoding="utf-8"))
    files = {name: FileEntry(**entry) for name, entry in raw.pop("files").items()}
    return Manifest(files=files, **raw)


def verify_manifest(root: Path, dataset: str, deep: bool = False) -> list[str]:
    """Ways in which the dataset's files differ from its manifest; empty when they match.

    The quick check compares file names, sizes and modification times. `deep` re-reads every
    file and compares content hashes.
    """
    manifest = read_manifest(root, dataset)
    directory = Path(root) / dataset
    present = {path.name: path for path in directory.glob("*.parquet")}
    problems = [f"{name}: listed in the manifest but missing" for name in manifest.files.keys() - present.keys()]
    problems += [f"{name}: on disk but not in the manifest" for name in present.keys() - manifest.files.keys()]
    for name in sorted(manifest.files.keys() & present.keys()):
        entry, stat = manifest.files[name], present[name].stat()
        if deep:
            if content_hash(pd.read_parquet(present[name])) != entry.content_hash:
                problems.append(f"{name}: content differs from the manifest")
        elif (stat.st_size, stat.st_mtime_ns) != (entry.size, entry.mtime_ns):
            problems.append(f"{name}: changed on disk since the manifest was written")
    return problems


def dataset_id(root: Path, dataset: str) -> str:
    """The dataset's id, after checking the files still match the manifest (quick check)."""
    problems = verify_manifest(root, dataset)
    if problems:
        shown = "; ".join(problems[:3])
        raise ManifestError(
            f"dataset {dataset!r} does not match its manifest ({len(problems)} problems: {shown}); "
            "run `uv run trading rebuild`"
        )
    return read_manifest(root, dataset).id


def _identity(files: dict[str, FileEntry]) -> str:
    lines = "\n".join(f"{name}:{entry.content_hash}" for name, entry in sorted(files.items()))
    return hashlib.sha256(lines.encode()).hexdigest()
