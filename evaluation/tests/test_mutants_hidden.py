"""Withheld from the agent, overlaid only after the run is finished.

A suite cannot be graded by running it -- a suite that asserts nothing passes.
So each test here seeds a **broken variant** of `durations/parse.py`, runs the
visible suite against it, and asserts the suite notices. One mutant per rule in
`docs/durations.md` that the seed's two tests do not reach.

`pass_to_pass` holds the other half of the contract: the suite must still pass
against the real module. Without it, a file containing `assert False` catches
every mutant and scores a perfect `fail_to_pass`.

`durations/parse.py` is immutable. The task is to describe the module's
behaviour, not to change it, and a run that edits the source to match a test it
found easier to write has inverted the exercise.
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SOURCE = Path("durations") / "parse.py"
IGNORED = shutil.ignore_patterns("evaluation", "__pycache__", ".pytest_cache",
                                 ".git", "*.pyc")


def _run_suite(mutation=None):
    """Run the visible suite in a throwaway copy, optionally mutated.

    Returns the pytest exit code. Copying rather than editing in place keeps
    the workdir the judge reads untouched, and dropping `evaluation` keeps this
    file out of the inner run.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "tree"
        shutil.copytree(".", root, ignore=IGNORED)

        if mutation is not None:
            old, new = mutation
            target = root / SOURCE
            text = target.read_text(encoding="utf-8")
            assert old in text, (
                f"mutation anchor missing from {SOURCE}: {old!r}. The source "
                "is immutable; if it changed, that is the finding.")
            target.write_text(text.replace(old, new, 1), encoding="utf-8")

        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests", "-q", "-p", "no:cacheprovider"],
            cwd=root, capture_output=True, text=True, timeout=300)
        return result.returncode


def _caught(mutation):
    """Did the suite fail against this broken variant?"""
    return _run_suite(mutation) != 0


# -- one mutant per uncovered rule ------------------------------------------

def test_the_suite_catches_a_bare_number_read_as_minutes():
    """`90` is 90 seconds. The seed's two tests never pass a bare number."""
    assert _caught(("        return seconds\n",
                    "        return seconds * 60\n"))


def test_the_suite_catches_units_becoming_case_sensitive():
    """`1H` is an hour. Dropping the fold makes it an unknown unit instead."""
    assert _caught(('    cleaned = "".join(text.split()).lower()\n',
                    '    cleaned = "".join(text.split())\n'))


def test_the_suite_catches_a_negative_duration_being_accepted():
    """`-5` must raise, not return -5."""
    assert _caught(("        if seconds < 0:\n", "        if False:\n"))


def test_the_suite_catches_a_missing_value_becoming_none():
    """`None` is zero, and the scheduler adds it to other numbers."""
    assert _caught(("    if text is None:\n        return 0\n",
                    "    if text is None:\n        return None\n"))


def test_the_suite_catches_a_trailing_number_being_accepted():
    """`1h30` is a typo for `1h30m`, and the rule the page calls most common."""
    assert _caught((
        '    if number:\n        raise ValueError(f"trailing number with no unit in {text!r}")\n',
        "    if number:\n        total += int(number)\n"))


# -- the other half of the contract -----------------------------------------

def test_the_suite_passes_against_the_real_module():
    """A suite that fails everything catches every mutant and is worthless."""
    assert _run_suite() == 0
