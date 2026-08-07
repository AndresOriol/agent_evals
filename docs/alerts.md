# Alerts

## When an alert fires

`should_alert(value, threshold)` returns true when the value is greater than or
equal to the threshold, so a measurement landing exactly on the threshold does
alert.

## What the message says

`format_alert(name, value)` produces `"<name> is <value>"` — for example,
`cpu is 82`.
