from usage import accounts, report

ACCOUNTS = [
    {"id": "a1", "name": "Northwind", "status": "active"},
    {"id": "a2", "name": "Initech", "status": "suspended"},
    {"id": "a3", "name": "Umbrella", "status": "active"},
    {"id": "a4", "name": "Cyberdyne", "status": "closed"},
]

EVENTS = [
    {"account": "a1", "units": 30},
    {"account": "a2", "units": 12},
    {"account": "a1", "units": 10},
]


def test_totals_count_every_event():
    assert report.totals(ACCOUNTS, EVENTS) == {"a1": 40, "a2": 12, "a3": 0,
                                               "a4": 0}


def test_totals_ignore_an_event_for_an_unknown_account():
    stray = EVENTS + [{"account": "nope", "units": 99}]
    assert report.totals(ACCOUNTS, stray)["a1"] == 40


def test_the_report_is_ordered_by_usage():
    units = [units for _, _, units in report.monthly(ACCOUNTS, EVENTS)]
    assert units == sorted(units, reverse=True)


def test_the_busiest_account_is_first():
    assert report.monthly(ACCOUNTS, EVENTS)[0][0] == "a1"


def test_billable_excludes_only_closed_accounts():
    assert [a["id"] for a in accounts.billable(ACCOUNTS)] == ["a1", "a2", "a3"]


def test_by_status_keeps_the_order_given():
    assert [a["id"] for a in accounts.by_status(ACCOUNTS, "active")] == ["a1",
                                                                        "a3"]
