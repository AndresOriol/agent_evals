"""The shape of the exporter's API. Not its behaviour.

These ship in the seed on purpose. Without them a build-it task is unfair
rather than hard: an agent that writes a correct exporter under a different
name would score zero for a reason that has nothing to do with capability.

They assert names, arity and return types, and deliberately nothing about what
the file contains -- that is in `docs/export_format.md`, and it is what the run
is actually graded on.
"""

RECORDS = [
    {"name": "Xanthan gum PM80", "category": "Thickener", "amount": 12.5,
     "unit": "kg"},
]


def test_the_module_exists():
    import catalogue.export  # noqa: F401


def test_to_lines_returns_a_list_of_strings():
    from catalogue.export import to_lines

    lines = to_lines(RECORDS)
    assert isinstance(lines, list)
    assert lines and all(isinstance(line, str) for line in lines)
    assert not any(line.endswith("\n") for line in lines)


def test_to_lines_accepts_an_empty_catalogue():
    from catalogue.export import to_lines

    assert isinstance(to_lines([]), list)


def test_write_creates_the_file_and_returns_a_record_count(tmp_path):
    from catalogue.export import write

    target = tmp_path / "catalogue.txt"
    written = write(RECORDS, target)
    assert target.is_file()
    assert isinstance(written, int)
