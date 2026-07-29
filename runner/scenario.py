"""Loading and materializing scenarios.

A scenario is an orphan branch in this repo, frozen as an immutable tag
(`scenario/<id>/v1`). Runs always reference the tag, never the branch, so
editing a scenario can never change what an old result meant.

Materializing extracts *only* `seed/` -- never `verify/`, `reference/` or the
`.git` dir. That split is the whole integrity story: the agent is jailed to its
workdir, so anything extracted there is something it can read.
"""

import hashlib
import io
import subprocess
import tarfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class Task:
    id: str
    scenario_id: str
    prompt: str
    suite: list
    tags: list
    judge_notes: str = ""


@dataclass
class Scenario:
    id: str
    tag: str
    title: str
    category: str
    difficulty: str
    tags: list
    context_mode: str
    immutable: list
    fail_to_pass: list
    pass_to_pass: list
    timeout_s: int
    tasks: list = field(default_factory=list)


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def _read(repo: Path, tag: str, path: str) -> Optional[str]:
    """One file out of a tag, or None if it isn't there."""
    result = subprocess.run(["git", "-C", str(repo), "show", f"{tag}:{path}"],
                            capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None


def list_scenarios(repo: Path) -> list:
    """Every scenario id that has at least one version tag."""
    tags = _git(repo, "tag", "--list", "scenario/*").split()
    return sorted({t.split("/")[1] for t in tags if len(t.split("/")) == 3})


def latest_tag(repo: Path, scenario_id: str) -> str:
    """Highest vN tag for a scenario. Pin an older one explicitly to reproduce."""
    tags = _git(repo, "tag", "--list", f"scenario/{scenario_id}/v*").split()
    if not tags:
        raise RuntimeError(f"No tags for scenario {scenario_id!r}")
    return max(tags, key=lambda t: int(t.rsplit("/v", 1)[1]))


def _parse_task(text: str, task_id: str, scenario_id: str) -> Task:
    """Front-matter + '## Prompt' / '## Judge notes' sections."""
    meta, body = {}, text
    if text.startswith("---"):
        _, raw, body = text.split("---", 2)
        meta = yaml.safe_load(raw) or {}

    sections, current = {}, None
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections[current] = []
        elif current:
            sections[current].append(line)
    joined = {k: "\n".join(v).strip() for k, v in sections.items()}

    return Task(
        id=meta.get("id", task_id),
        scenario_id=scenario_id,
        prompt=joined.get("prompt", "").strip(),
        suite=meta.get("suite", []),
        tags=meta.get("tags", []),
        judge_notes=joined.get("judge notes", ""),
    )


def load(repo: Path, scenario_id: str, tag: Optional[str] = None) -> Scenario:
    tag = tag or latest_tag(repo, scenario_id)
    raw = _read(repo, tag, "scenario.yaml")
    if raw is None:
        raise RuntimeError(f"{tag} has no scenario.yaml")
    meta = yaml.safe_load(raw)

    scenario = Scenario(
        id=meta["id"],
        tag=tag,
        title=meta.get("title", ""),
        category=meta.get("category", "unknown"),
        difficulty=meta.get("difficulty", "unknown"),
        tags=meta.get("tags", []),
        context_mode=meta.get("context_mode", "none"),
        immutable=meta.get("immutable", []),
        fail_to_pass=meta.get("fail_to_pass", []),
        pass_to_pass=meta.get("pass_to_pass", []),
        timeout_s=meta.get("timeout_s", 900),
    )

    listing = _git(repo, "ls-tree", "--name-only", f"{tag}", "tasks/").split()
    for path in listing:
        text = _read(repo, tag, path)
        if text is not None:
            scenario.tasks.append(
                _parse_task(text, Path(path).stem, scenario.id))
    return scenario


def materialize(repo: Path, tag: str, subdir: str, dest: Path) -> None:
    """Extract one subtree of a tag into dest, without its top-level dir name.

    `git archive` to an in-memory tar rather than piping to the `tar` binary:
    no shell, and no dependency on which tar happens to be on PATH.
    """
    dest.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "-C", str(repo), "archive", "--format=tar", tag, subdir],
        capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"git archive {tag}:{subdir} failed: "
                           f"{result.stderr.decode(errors='replace').strip()}")

    prefix = subdir.rstrip("/") + "/"
    with tarfile.open(fileobj=io.BytesIO(result.stdout)) as tar:
        for member in tar.getmembers():
            if not member.name.startswith(prefix):
                continue
            member.name = member.name[len(prefix):]
            if member.name:
                tar.extract(member, dest, filter="data")


def hash_files(root: Path, relative_paths: list) -> dict:
    """sha256 per path; missing files hash to None so deletion is detectable."""
    digests = {}
    for rel in relative_paths:
        target = root / rel
        digests[rel] = (hashlib.sha256(target.read_bytes()).hexdigest()
                        if target.is_file() else None)
    return digests
