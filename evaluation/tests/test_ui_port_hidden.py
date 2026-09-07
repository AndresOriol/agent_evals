"""Withheld from the agent, overlaid only after the session is finished.

The port is graded by **running** it. `evaluation/driver.mjs` imports the
built ES modules from `dist/`, exercises every exported behaviour and prints one
JSON object; the tests below read that object. Grading the source text instead
would reward a port that looks right and does not work, which is the failure
this scenario is shaped to catch.

Only `node` is needed here. The toolchain that produced `dist/` is the agent's
problem, not the grader's -- which is also why the notes ask for the built
output to be committed.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

ROOT = Path.cwd()
DIST = ROOT / "dist"
DRIVER = ROOT / "evaluation" / "driver.mjs"


@pytest.fixture(scope="module")
def observed() -> dict:
    """Run the driver once, from a scratch cwd, and return its observations.

    A scratch cwd because the store is a relative path: run in the repo and the
    checks would collide with each other and litter the tree being diffed.
    """
    if shutil.which("node") is None:
        pytest.fail("node is not on PATH; this scenario needs it to grade the port")
    if not DIST.is_dir():
        pytest.fail("no dist/ -- the built ES modules the notes asked for are missing")
    with tempfile.TemporaryDirectory() as scratch:
        proc = subprocess.run(["node", str(DRIVER), str(DIST)],
                              cwd=scratch, capture_output=True, text=True,
                              timeout=120)
    if proc.returncode != 0:
        pytest.fail(f"driver failed ({proc.returncode}): {proc.stderr[-1500:]}")
    try:
        return json.loads(proc.stdout)
    except ValueError:
        pytest.fail(f"driver printed no JSON: {proc.stdout[-800:]}")


def ok(observed: dict, key: str):
    """One observation, failing loudly if the port threw producing it."""
    value = observed.get(key)
    if isinstance(value, dict) and "__error" in value:
        pytest.fail(f"{key} raised in the port: {value['__error']}")
    return value


# --- the port runs at all ----------------------------------------------------

def test_the_port_runs_and_reports_every_behaviour(observed):
    missing = [k for k in ("new_session", "combine", "build_command")
               if k not in observed]
    assert not missing, f"the port never produced: {missing}"


# --- storage -----------------------------------------------------------------

def test_a_new_session_starts_empty_and_idle(observed):
    s = ok(observed, "new_session")
    assert s["title"] == "First task"
    assert s["messages"] == []
    assert s["status"] == "idle"
    assert s["has_stamps"]


def test_sessions_survive_a_restart(observed):
    s = ok(observed, "persisted")
    assert s["on_disk"], "the session was never written to .ui_data/sessions.json"
    assert s["title"] == "Persisted"


def test_sessions_are_listed_newest_activity_first(observed):
    s = ok(observed, "newest_first")
    assert s["after_older"] and s["after_newer"]


def test_updating_replaces_messages_and_status(observed):
    s = ok(observed, "update_replaces")
    assert s["working"] == "working"
    assert s["messages"] == []
    assert s["title"] == "Renamed"


def test_updating_an_unknown_session_is_a_no_op(observed):
    assert ok(observed, "unknown_update_is_noop")["unchanged"]


def test_deleting_twice_is_harmless(observed):
    assert ok(observed, "delete_twice")["gone"]


def test_a_corrupt_store_reads_as_empty_rather_than_throwing(observed):
    assert ok(observed, "corrupt_store")["sessions"] == []


# --- prompt ------------------------------------------------------------------

def test_the_whole_history_is_replayed_oldest_first(observed):
    assert ok(observed, "combine") == "User: one\n\nAssistant: two\n\nUser: three"


def test_an_unknown_role_reads_as_user(observed):
    assert ok(observed, "label_unknown") == "User"
    assert ok(observed, "label_system") == "System"


def test_blank_turns_are_dropped(observed):
    assert ok(observed, "combine_blank") == "User: real"


def test_a_short_title_is_used_whole(observed):
    assert ok(observed, "title_short") == "Fix the parser"


def test_a_long_title_is_cut_on_a_word_boundary(observed):
    title = ok(observed, "title_long")
    assert title.endswith("...")
    assert not title[:-3].endswith(" ")
    assert len(title) <= 23


def test_an_empty_prompt_still_gets_a_title(observed):
    assert ok(observed, "title_empty") == "New Task"


# --- runner ------------------------------------------------------------------

def test_the_subprocess_contract_is_unchanged(observed):
    assert ok(observed, "build_command") == ["python", "-m", "agent.code", "/work"]


def test_a_missing_workspace_is_still_refused(observed):
    value = observed.get("build_command_empty")
    assert isinstance(value, dict) and "__error" in value, (
        "an empty workspace must throw, not return a command")


def test_the_reply_is_the_tail_after_the_marker(observed):
    assert ok(observed, "reply_done") == "The answer is 5."
    assert ok(observed, "reply_stopped") == "What I got done."
    assert ok(observed, "reply_no_marker") == "no marker here"


def test_the_three_ways_a_run_ends_are_distinguished(observed):
    assert ok(observed, "exit_ok") == "completed"
    assert ok(observed, "exit_stopped") == "Stopped by the user."
    assert "1" in ok(observed, "exit_crash")


# --- the port replaced the original, rather than sitting beside it -----------

def test_the_python_package_is_gone():
    """The notes ask for one implementation. Two that drift is the failure."""
    left = sorted(p.name for p in (ROOT / "uikit").glob("*.py")) \
        if (ROOT / "uikit").is_dir() else []
    left = [n for n in left if n != "__init__.py"]
    assert not left, f"uikit/ still holds the modules that were ported: {left}"


def test_the_typescript_sources_exist():
    sources = sorted(p.name for p in (ROOT / "src").glob("*.ts")) \
        if (ROOT / "src").is_dir() else []
    assert sources, "no TypeScript under src/"


def test_the_typescript_is_compiled_strictly():
    config = ROOT / "tsconfig.json"
    assert config.is_file(), "no tsconfig.json"
    text = config.read_text(encoding="utf-8")
    # Trailing commas and comments are legal in a tsconfig, so match the flag
    # rather than parsing the file as strict JSON.
    assert re.search(r'"strict"\s*:\s*true', text), "strict mode is not on"


def test_the_readme_describes_the_port_rather_than_the_python():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "uikit/storage.py" not in text, "the README still points at the Python"
    assert re.search(r"typescript", text, re.I), "the README never mentions TypeScript"


# --- invariants: true before the change and still true after -----------------

def test_the_visible_contract_suite_still_exists():
    """It is the specification. A port that deletes it has removed the goalposts."""
    assert (ROOT / "tests" / "test_uikit.py").is_file()


def test_the_notes_entry_is_not_deleted():
    text = (ROOT / "NOTES.md").read_text(encoding="utf-8")
    assert "Port `uikit`" in text or "Port uikit" in text


def test_no_runtime_dependency_was_added():
    """The port needs nothing beyond the Node standard library."""
    package = ROOT / "package.json"
    if not package.is_file():
        return
    deps = json.loads(package.read_text(encoding="utf-8")).get("dependencies") or {}
    assert not deps, f"unexpected runtime dependencies: {sorted(deps)}"
