import textwrap

import libcst as cst
import pytest

from .feedback import Error, Violation
from .position import Location, Position
from .report import Report


@pytest.mark.parametrize(
    "filename, error_infos, expected_msg",
    [
        # empty report
        ("no_errors.py", [], ""),
        # errors only
        (
            "errors_only.py",
            ["No position", (10, 2, "A position")],
            """
            errors_only.py: No position
            errors_only.py:10:2: A position
            """,
        ),
        # violations only
        (
            "violations_only.py",
            [("1", False), (2, 3, "2", False), (40, 1, "None", False)],
            """
            violations_only.py: 1
            violations_only.py:2:3: 2
            violations_only.py:40:1: None
            """,
        ),
        # multiline code
        (
            "multiline.py",
            [(1, 5, "(\n    (),\n  )", False)],
            """
            multiline.py:1:5: (
              (),
            )
            """,
        ),
        # violations and fixes
        (
            "violations_and_fixes.py",
            [("1", False), (2, 3, "2", True), (3, 4, "3", True)],
            """
            violations_and_fixes.py: 1
            2 fixes applied
            """,
        ),
        # combination
        (
            "combination.py",
            ["Big error", ("1", False), (2, 3, "2", True)],
            """
            combination.py: Big error
            combination.py: 1
            1 fix applied
            """,
        ),
    ],
)
def test_file_report_display(
    filename: str,
    error_infos: list[tuple[int, int, str, bool] | tuple[int, int, str] | tuple[str, bool] | str],
    expected_msg: str,
    capsys: pytest.CaptureFixture,
) -> None:
    feedback = []
    for error_info in error_infos:
        match error_info:
            case str() as code:
                position = None
            case [str() as code, bool() as fixed]:
                position = None
            case [int() as line, int() as char, str() as code]:
                position = Position(line, char)
            case [int() as line, int() as char, str() as code, bool() as fixed]:
                position = Position(line, char)
            case _:
                pytest.fail("Unable to parse error info.")
        try:
            cst.parse_expression(code)
        except cst.ParserSyntaxError:
            msg = code
            feedback.append(Error(Location(filename, position), msg))
        else:
            feedback.append(Violation(Location(filename, position), code, fixed))  # type: ignore
    report = Report.from_feedback(iter(feedback))
    report.display()
    out, err = capsys.readouterr()
    assert err == ""
    expected_msg = textwrap.dedent(expected_msg).strip()
    assert out.strip() == expected_msg
