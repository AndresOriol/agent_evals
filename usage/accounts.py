"""Accounts, as the billing export hands them over.

An account carries a `status`, which billing sets and this package only reads:

- `active` — billable, and the customer can use the service.
- `suspended` — billable, and the customer cannot start new work. Usage can
  still arrive for a suspended account: work started before the suspension is
  allowed to finish, and it is charged.
- `closed` — not billable. No usage can arrive.
"""

STATUSES = ("active", "suspended", "closed")


def by_status(accounts, status):
    """Every account with the given status, in the order given."""
    return [account for account in accounts if account["status"] == status]


def billable(accounts):
    """Accounts billing will raise an invoice for this month."""
    return [account for account in accounts if account["status"] != "closed"]
