"""The monthly usage report.

One line per account, most usage first. What counts as usage is decided
upstream: this module is handed the events that already belong to the month.
"""


def totals(accounts, events):
    """Units used per account id, including accounts with no events."""
    used = {account["id"]: 0 for account in accounts}
    for event in events:
        if event["account"] in used:
            used[event["account"]] += event["units"]
    return used


def monthly(accounts, events):
    """The report: `(id, name, units)` per account, most units first.

    Accounts with equal usage keep the order they arrive in, which is the
    order the account list is maintained in.
    """
    used = totals(accounts, events)
    rows = [(account["id"], account["name"], used[account["id"]])
            for account in accounts]
    return sorted(rows, key=lambda row: -row[2])
