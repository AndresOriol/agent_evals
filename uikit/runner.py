"""How the UI launches the coding agent.

The contract is fixed and not ours to change: `python -m agent.code <workspace>`,
the whole prompt on stdin, EOF ends the task, exit code 0 means success. This
module builds the invocation and reads the result; it never runs anything
itself, so it stays testable without spawning a process.
"""

from __future__ import annotations

DONE_MARKER = "=== DONE"
STOPPED_MARKER = "=== STOPPED"


def build_command(workspace: str, executable: str = "python") -> list[str]:
    """The argv for one agent run over `workspace`."""
    if not workspace:
        raise ValueError("a workspace is required")
    return [executable, "-m", "agent.code", workspace]


def extract_reply(output: str) -> str:
    """The agent's own answer, without the run log around it.

    Everything before the end marker is the router's log -- routing lines, HTTP
    statuses, token counts. Replaying that back into the next prompt costs the
    conversation its context window and tells the model nothing, so only the
    tail after the marker is kept.
    """
    for marker in (DONE_MARKER, STOPPED_MARKER):
        index = output.rfind(marker)
        if index == -1:
            continue
        tail = output[index:].split("===", 2)
        if len(tail) >= 3:
            return tail[2].strip()
    return output.strip()


def describe_exit(code: int, user_stopped: bool = False) -> str:
    """What to record as the assistant's message when a run ends.

    A stop the user asked for, a crash and a clean finish are three different
    things, and reporting all of them as one loses the only clue about which
    happened.
    """
    if user_stopped:
        return "Stopped by the user."
    if code == 0:
        return "completed"
    return f"Agent exited with code {code}."
