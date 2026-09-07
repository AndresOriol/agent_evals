"""Local JSON storage for chat sessions and their message history.

Sessions live in `.ui_data/sessions.json`, keyed by id. The file is the whole
database: it is read in full, mutated, and written back on every change.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(".ui_data")
SESSIONS_FILE = DATA_DIR / "sessions.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not SESSIONS_FILE.exists():
        SESSIONS_FILE.write_text("{}", encoding="utf-8")


def _load_all() -> dict:
    _ensure_storage()
    try:
        return json.loads(SESSIONS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        # A truncated or hand-edited file must not take the app down with it.
        return {}


def _save_all(data: dict) -> None:
    _ensure_storage()
    SESSIONS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                             encoding="utf-8")


def create_session(title: str = "New Task") -> str:
    """Make an empty session and return its id."""
    data = _load_all()
    session_id = str(uuid.uuid4())[:8]
    now = _now()
    data[session_id] = {
        "id": session_id,
        "title": title,
        "created_at": now,
        "updated_at": now,
        "messages": [],
        "status": "idle",
    }
    _save_all(data)
    return session_id


def get_session(session_id: str) -> dict | None:
    return _load_all().get(session_id)


def get_all_sessions() -> list[dict]:
    """Every session, newest activity first."""
    sessions = list(_load_all().values())
    sessions.sort(key=lambda s: s.get("updated_at", s.get("created_at", "")),
                  reverse=True)
    return sessions


def update_session(session_id: str, messages: list[dict],
                   status: str = "idle", title: str | None = None) -> None:
    """Replace a session's messages and status. Unknown ids are ignored."""
    data = _load_all()
    if session_id not in data:
        return
    data[session_id]["messages"] = messages
    data[session_id]["status"] = status
    data[session_id]["updated_at"] = _now()
    if title:
        data[session_id]["title"] = title
    _save_all(data)


def delete_session(session_id: str) -> None:
    data = _load_all()
    if data.pop(session_id, None) is not None:
        _save_all(data)
