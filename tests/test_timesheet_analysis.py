from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.timesheet_analysis import TimesheetDataError, analyze_timesheets


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class TimesheetAnalysisTest(unittest.TestCase):
    def test_official_dataset_matches_expected_output(self) -> None:
        records = _load_json(PROJECT_ROOT / "data.json")
        expected = _load_json(PROJECT_ROOT / "output.json")

        self.assertEqual(analyze_timesheets(records), expected)

    def test_ignores_non_positive_minutes_and_counts_ignored_records(self) -> None:
        result = analyze_timesheets(
            [
                _record(user_id=1, user_name="Ana", task_id=101, task_name="Task A", minutes=30),
                _record(user_id=1, user_name="Ana", task_id=102, task_name="Task B", minutes=0),
                _record(user_id=2, user_name="Bruno", task_id=103, task_name="Task C", minutes=-5),
            ]
        )

        self.assertEqual(result["totalMinutes"], 30)
        self.assertEqual(result["ignoredRecords"], 2)
        self.assertEqual(result["tasks"][0]["taskId"], 101)

    def test_task_tie_breaker_uses_task_id_ascending(self) -> None:
        result = analyze_timesheets(
            [
                _record(user_id=1, user_name="Ana", task_id=202, task_name="Task B", minutes=10),
                _record(user_id=2, user_name="Bruno", task_id=201, task_name="Task A", minutes=10),
            ]
        )

        self.assertEqual([task["taskId"] for task in result["tasks"]], [201, 202])
        self.assertEqual(result["mostWorkedTask"]["taskId"], 201)

    def test_employee_tie_breaker_uses_user_id_ascending(self) -> None:
        result = analyze_timesheets(
            [
                _record(user_id=2, user_name="Bruno", task_id=101, task_name="Task A", minutes=25),
                _record(user_id=1, user_name="Ana", task_id=102, task_name="Task B", minutes=25),
            ]
        )

        self.assertEqual([employee["userId"] for employee in result["top3Employees"]], [1, 2])

    def test_most_distinct_user_tie_breaker_and_task_ids_order(self) -> None:
        result = analyze_timesheets(
            [
                _record(user_id=2, user_name="Bruno", task_id=105, task_name="Task E", minutes=10),
                _record(user_id=2, user_name="Bruno", task_id=103, task_name="Task C", minutes=10),
                _record(user_id=1, user_name="Ana", task_id=104, task_name="Task D", minutes=10),
                _record(user_id=1, user_name="Ana", task_id=102, task_name="Task B", minutes=10),
            ]
        )

        self.assertEqual(
            result["mostDistinctUserOnTasks"],
            {"userId": 1, "userName": "Ana", "distinctTasks": 2, "taskIds": [102, 104]},
        )

    def test_percentages_are_formatted_with_two_decimal_places(self) -> None:
        result = analyze_timesheets(
            [
                _record(user_id=1, user_name="Ana", task_id=101, task_name="Task A", minutes=1),
                _record(user_id=2, user_name="Bruno", task_id=102, task_name="Task B", minutes=2),
            ]
        )

        self.assertEqual(result["tasks"][0]["percentage"], "66.67%")
        self.assertEqual(result["tasks"][1]["percentage"], "33.33%")

    def test_invalid_record_shape_raises_clear_error(self) -> None:
        with self.assertRaisesRegex(TimesheetDataError, "missing field: taskName"):
            analyze_timesheets(
                [
                    {
                        "userId": 1,
                        "userName": "Ana",
                        "taskId": 101,
                        "minutes": 10,
                    }
                ]
            )


def _load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _record(
    *,
    user_id: int,
    user_name: str,
    task_id: int,
    task_name: str,
    minutes: int,
) -> dict[str, object]:
    return {
        "userId": user_id,
        "userName": user_name,
        "taskId": task_id,
        "taskName": task_name,
        "status": "done",
        "minutes": minutes,
        "date": "2026-01-01",
    }


if __name__ == "__main__":
    unittest.main()
