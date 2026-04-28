from __future__ import annotations

import sys
from pathlib import Path

from timesheet_analysis import TimesheetDataError, analyze_timesheets, load_records, write_result


def main() -> int:
    project_root = Path.cwd()
    input_path = project_root / "data.json"
    output_path = project_root / "result.json"

    try:
        records = load_records(input_path)
        result = analyze_timesheets(records)
        write_result(result, output_path)
    except TimesheetDataError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Analysis completed successfully: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
