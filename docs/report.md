# The monthly report

`usage.report.monthly` renders one line per account — id, name, units — most
usage first. Accounts with equal usage keep the order the account list is
maintained in.

## What it is for

Two people read this report and they read it for different reasons.

**Support** reads it at the start of the month to see who has been busy, and
opens the accounts near the top. For them a line with zero units is noise; the
report is how they find the accounts that were *active* over the period.

**Billing** reconciles it against the invoices they raised. For them the report
has to line up with what `usage.accounts.billable` returns, because an invoice
with no matching report line is a query they have to answer by hand.

## Statuses

`usage.accounts` documents what a status means. The one that surprises people:
a **suspended** account can still accrue usage. Work that started before the
suspension is allowed to finish, and it is charged, so a suspended account with
units on it is normal rather than a data error.

A **closed** account cannot accrue usage and is not billable.

## Ordering

Descending by units, stable within a tie. The stability matters: the account
list is maintained in onboarding order and support reads ties as "oldest
customer first".
