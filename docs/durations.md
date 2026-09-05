# Duration strings

Every interval in the scheduler config is written as a duration string.
`durations.parse.parse_duration` turns one into a number of seconds.

## What is accepted

| Input | Seconds | Rule |
| --- | --- | --- |
| `45s` | 45 | a number and a unit |
| `1h30m` | 5400 | units combined, largest first |
| `2h` | 7200 | one unit is fine |
| `90` | 90 | **a bare number is seconds** |
| `1H` | 3600 | units are **case insensitive** |
| `1h 30m` | 5400 | whitespace anywhere is ignored |
| `""` | 0 | an empty string is zero |
| `None` | 0 | **a missing value is zero, not an error** |

The units are `h`, `m` and `s`, worth 3600, 60 and 1 seconds.

## What is rejected

Everything below raises `ValueError`. The scheduler treats a bad interval as a
configuration error and refuses to start, so a rejection that silently becomes
a number is worse than a crash.

| Input | Why |
| --- | --- |
| `-5` | **a duration is never negative** |
| `-1h` | same |
| `5x` | `x` is not a unit |
| `1.5h` | fractions are not supported; write `90m` |
| `1m30h` | units must descend — the small one cannot come first |
| `1h2h` | and a unit cannot repeat |
| `h` | a unit with no number |
| `1h30` | **a trailing number with no unit** — almost always a typo for `1h30m` |

## Why the rejections matter more than the acceptances

The scheduler is configured by hand and the strings are short, so the mistakes
people actually make are `1h30` for `1h30m`, `-5` from a subtraction that went
the wrong way, and a copied value that still has its unit in the wrong case.
Every one of those has a defined answer here, and every one of them is a value
that would otherwise reach the scheduler as a plausible-looking number.
