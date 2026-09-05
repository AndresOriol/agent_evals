import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stocktake.reconcile import reconcile


def test_delta_is_counted_minus_expected():
    report = reconcile({"A-1": 4}, {"A-1": 6})
    assert report["lines"][0]["delta"] == -2


def test_lines_are_ordered_by_sku():
    # The importer merges reports by walking both line lists in step.
    report = reconcile({"C-3": 1, "A-1": 1, "B-2": 1}, {})
    assert [line["sku"] for line in report["lines"]] == ["A-1", "B-2", "C-3"]
