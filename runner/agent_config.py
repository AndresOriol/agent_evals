"""Resolving an agent configuration to something runnable.

A config is a pinned commit of the agent repo plus overrides. It resolves via
`git worktree add --detach`, so a comparison runs from a clean tree while you
keep editing the branch it came from.

The recorded fingerprint is the resolved SHA plus a hash of the effective
overrides -- `ref: master` today and `ref: master` next month are different
configurations, and the results must say so rather than silently comparing
two different things.
"""

import hashlib
import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# What actually launches the agent. Overridable so the pipeline can be tested
# against a stub without spending free-tier quota on the real pool.
DEFAULT_AGENT_CMD = ["python", "-m", "agent.coding_agent", "{workdir}"]


@dataclass
class AgentConfig:
    name: str
    repo: Path
    ref: str
    sha: str
    worktree: Path
    agent_cmd: list
    env: dict = field(default_factory=dict)
    router_config: str = ""

    @property
    def fingerprint(self) -> str:
        payload = json.dumps({"sha": self.sha, "env": self.env,
                              "router_config": self.router_config,
                              "agent_cmd": self.agent_cmd}, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()[:12]


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def load(path: Path, worktree_root: Path) -> AgentConfig:
    spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    repo = (path.parent / spec["repo"]).resolve()
    ref = spec.get("ref", "master")
    sha = _git(repo, "rev-parse", ref)

    overrides = spec.get("overrides") or {}
    worktree = worktree_root / f"{spec['name']}-{sha[:8]}"
    if not worktree.exists():
        worktree.parent.mkdir(parents=True, exist_ok=True)
        _git(repo, "worktree", "add", "--detach", str(worktree), sha)

    return AgentConfig(
        name=spec["name"],
        repo=repo,
        ref=ref,
        sha=sha,
        worktree=worktree,
        agent_cmd=spec.get("agent_cmd", DEFAULT_AGENT_CMD),
        env={str(k): str(v) for k, v in (overrides.get("env") or {}).items()},
        router_config=overrides.get("router_config") or "",
    )
