# durations

Parses the duration strings used in this project's configuration files.

    parse_duration("30s")   # -> 30
    parse_duration("5m")    # -> 300
    parse_duration("2h")    # -> 7200

## Accepted format

A whole number followed by a one-letter unit: `s` for seconds, `m` for minutes,
`h` for hours. Anything else raises `ValueError`.
