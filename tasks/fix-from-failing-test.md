---
id: fix-from-failing-test
suite: [smoke, full]
tags: [bugfix, test-driven, L0]
---

## Prompt
The test in tests/test_retry.py fails. Fix the code in retry.py so it passes.
Do not modify the test. Run `python -m pytest tests` to check your work before
you finish.

## Judge notes
The fix is to match the header name case-insensitively. HTTP header names are
case-insensitive, so lowercasing the lookup key or iterating the mapping are
both correct; hard-coding the exact string "Retry-After" alongside the existing
lowercase check is a worse fix that still passes, and should score lower on
correctness-beyond-tests.

Out of scope: validating the value, handling the HTTP-date form of
Retry-After, or touching anything other than parse_retry_after.
