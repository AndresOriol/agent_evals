"""Flatten a conversation into the single prompt the agent reads on stdin.

The agent is a one-shot process: it gets one block of text and exits at EOF, so
a multi-turn chat has to be replayed as one string on every turn.
"""

from __future__ import annotations

ROLE_LABELS = {"user": "User", "assistant": "Assistant", "system": "System"}


def label_for(role: str) -> str:
    """The display label for a role. Anything unrecognised reads as `User`."""
    return ROLE_LABELS.get(role, "User")


def combine(messages: list[dict]) -> str:
    """One prompt from the whole history, oldest first.

    Messages with empty content are dropped: a blank turn adds a stray label
    and nothing else, and the agent reads it as an instruction with no content.
    """
    parts = []
    for message in messages:
        content = (message.get("content") or "").strip()
        if not content:
            continue
        parts.append(f"{label_for(message.get('role', 'user'))}: {content}")
    return "\n\n".join(parts)


def title_from(prompt: str, limit: int = 40) -> str:
    """A session title from its first prompt, trimmed to `limit`.

    Trimmed on a word boundary where there is one, so a title does not end
    mid-word; an over-long single word is cut where it must be.
    """
    text = " ".join(prompt.split())
    if len(text) <= limit:
        return text or "New Task"
    cut = text[:limit].rsplit(" ", 1)[0]
    return (cut or text[:limit]) + "..."
