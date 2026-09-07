"""The behaviour contract for `uikit`, whatever language it is written in.

These tests describe what the UI's core must do. They are the specification a
port has to keep satisfying, so read them before changing anything.
"""

import json
import os
from pathlib import Path

import pytest

from uikit import prompt, runner, storage


@pytest.fixture(autouse=True)
def _in_tmp(tmp_path, monkeypatch):
    """Each test gets its own `.ui_data`, since the store is a fixed path."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path / ".ui_data")
    monkeypatch.setattr(storage, "SESSIONS_FILE",
                        tmp_path / ".ui_data" / "sessions.json")


# --- storage -----------------------------------------------------------------

def test_a_new_session_starts_empty_and_idle():
    sid = storage.create_session("First task")
    session = storage.get_session(sid)
    assert session["title"] == "First task"
    assert session["messages"] == []
    assert session["status"] == "idle"
    assert session["created_at"] and session["updated_at"]


def test_sessions_survive_a_restart():
    sid = storage.create_session("Persisted")
    assert json.loads((storage.SESSIONS_FILE).read_text(encoding="utf-8"))[sid]
    assert storage.get_session(sid)["title"] == "Persisted"


def test_sessions_are_listed_newest_activity_first():
    old = storage.create_session("older")
    new = storage.create_session("newer")
    storage.update_session(old, [{"role": "user", "content": "hi"}])
    assert [s["id"] for s in storage.get_all_sessions()][0] == old
    storage.update_session(new, [{"role": "user", "content": "hi"}])
    assert [s["id"] for s in storage.get_all_sessions()][0] == new


def test_updating_replaces_messages_and_status():
    sid = storage.create_session()
    storage.update_session(sid, [{"role": "user", "content": "a"}], "working")
    assert storage.get_session(sid)["status"] == "working"
    storage.update_session(sid, [], "completed", title="Renamed")
    assert storage.get_session(sid)["messages"] == []
    assert storage.get_session(sid)["title"] == "Renamed"


def test_updating_an_unknown_session_is_a_no_op():
    storage.update_session("nope", [{"role": "user", "content": "a"}])
    assert storage.get_all_sessions() == []


def test_deleting_removes_it_and_deleting_twice_is_harmless():
    sid = storage.create_session()
    storage.delete_session(sid)
    storage.delete_session(sid)
    assert storage.get_session(sid) is None


def test_a_corrupt_store_reads_as_empty_rather_than_crashing():
    storage._ensure_storage()
    storage.SESSIONS_FILE.write_text("{ not json", encoding="utf-8")
    assert storage.get_all_sessions() == []


# --- prompt ------------------------------------------------------------------

def test_the_whole_history_is_replayed_oldest_first():
    text = prompt.combine([
        {"role": "user", "content": "one"},
        {"role": "assistant", "content": "two"},
        {"role": "user", "content": "three"},
    ])
    assert text == "User: one\n\nAssistant: two\n\nUser: three"


def test_an_unknown_role_reads_as_user():
    assert prompt.label_for("wizard") == "User"
    assert prompt.label_for("system") == "System"


def test_blank_turns_are_dropped():
    assert prompt.combine([{"role": "user", "content": "   "},
                           {"role": "user", "content": "real"}]) == "User: real"


def test_a_short_title_is_used_whole():
    assert prompt.title_from("Fix the parser") == "Fix the parser"


def test_a_long_title_is_cut_on_a_word_boundary():
    title = prompt.title_from("the quick brown fox jumps over the lazy dog", 20)
    assert title.endswith("...")
    assert not title[:-3].endswith(" ")
    assert len(title) <= 23


def test_an_empty_prompt_still_gets_a_title():
    assert prompt.title_from("") == "New Task"


# --- runner ------------------------------------------------------------------

def test_the_subprocess_contract_is_fixed():
    assert runner.build_command("/work") == ["python", "-m", "agent.code", "/work"]


def test_a_missing_workspace_is_refused():
    with pytest.raises(ValueError):
        runner.build_command("")


def test_the_reply_is_taken_from_after_the_done_marker():
    output = "12:00 INFO routing\n12:01 INFO 200 OK\n\n=== DONE after 4 message(s) ===\n\nThe answer is 5.\n"
    assert runner.extract_reply(output) == "The answer is 5."


def test_a_stopped_run_still_yields_its_tail():
    output = "log line\n=== STOPPED (step budget spent) ===\n\nWhat I got done.\n"
    assert runner.extract_reply(output) == "What I got done."


def test_output_with_no_marker_is_returned_whole():
    assert runner.extract_reply("  no marker here  ") == "no marker here"


def test_the_three_ways_a_run_ends_are_distinguished():
    assert runner.describe_exit(0) == "completed"
    assert runner.describe_exit(1, user_stopped=True) == "Stopped by the user."
    assert "1" in runner.describe_exit(1)
