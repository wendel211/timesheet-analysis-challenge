from __future__ import annotations

import json
from pathlib import Path
from typing import Any


Record = dict[str, Any]
AnalysisResult = dict[str, Any]


class TimesheetDataError(ValueError):
    """Raised when the input file does not match the expected structure."""


def load_records(input_path: Path) -> list[Record]:
    try:
        with input_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise TimesheetDataError(f"Input file not found: {input_path}") from exc
    except json.JSONDecodeError as exc:
        raise TimesheetDataError(f"Invalid JSON in input file: {input_path}") from exc

    if not isinstance(data, list):
        raise TimesheetDataError("Input JSON must be a list of records")

    return data


def write_result(result: AnalysisResult, output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
        file.write("\n")


def analyze_timesheets(records: list[Record]) -> AnalysisResult:
    tasks: dict[int, dict[str, Any]] = {}
    employees: dict[int, dict[str, Any]] = {}
    ignored_records = 0
    total_minutes = 0

    for index, record in enumerate(records):
        minutes = _get_minutes(record, index)

        if minutes <= 0:
            ignored_records += 1
            continue

        _validate_valid_record(record, index)

        user_id = record["userId"]
        user_name = record["userName"]
        task_id = record["taskId"]
        task_name = record["taskName"]

        total_minutes += minutes

        task = tasks.setdefault(
            task_id,
            {"taskId": task_id, "taskName": task_name, "totalMinutes": 0},
        )
        task["totalMinutes"] += minutes

        employee = employees.setdefault(
            user_id,
            {"userId": user_id, "userName": user_name, "totalMinutes": 0, "taskIds": set()},
        )
        employee["totalMinutes"] += minutes
        employee["taskIds"].add(task_id)

    sorted_tasks = sorted(
        tasks.values(),
        key=lambda task: (-task["totalMinutes"], task["taskId"]),
    )
    task_summaries = [_format_task(task, total_minutes) for task in sorted_tasks]

    sorted_employees = sorted(
        employees.values(),
        key=lambda employee: (-employee["totalMinutes"], employee["userId"]),
    )
    top3_employees = [
        {
            "userId": employee["userId"],
            "userName": employee["userName"],
            "totalMinutes": employee["totalMinutes"],
        }
        for employee in sorted_employees[:3]
    ]

    most_distinct_user = _find_most_distinct_user(employees)

    return {
        "totalMinutes": total_minutes,
        "tasks": task_summaries,
        "mostWorkedTask": task_summaries[0] if task_summaries else None,
        "top3TasksPercentage": [
            {
                "taskId": task["taskId"],
                "taskName": task["taskName"],
                "percentage": task["percentage"],
            }
            for task in task_summaries[:3]
        ],
        "top3Employees": top3_employees,
        "mostDistinctUserOnTasks": most_distinct_user,
        "ignoredRecords": ignored_records,
    }


def _get_minutes(record: Any, index: int) -> int:
    if not isinstance(record, dict):
        raise TimesheetDataError(f"Record at index {index} must be an object")

    if "minutes" not in record:
        raise TimesheetDataError(f"Record at index {index} is missing field: minutes")

    minutes = record["minutes"]
    if isinstance(minutes, bool) or not isinstance(minutes, int):
        raise TimesheetDataError(f"Record at index {index} has invalid minutes")

    return minutes


def _validate_valid_record(record: Record, index: int) -> None:
    required_fields = ("userId", "userName", "taskId", "taskName")
    for field in required_fields:
        if field not in record:
            raise TimesheetDataError(f"Record at index {index} is missing field: {field}")

    if isinstance(record["userId"], bool) or not isinstance(record["userId"], int):
        raise TimesheetDataError(f"Record at index {index} has invalid userId")

    if isinstance(record["taskId"], bool) or not isinstance(record["taskId"], int):
        raise TimesheetDataError(f"Record at index {index} has invalid taskId")

    if not isinstance(record["userName"], str) or not record["userName"]:
        raise TimesheetDataError(f"Record at index {index} has invalid userName")

    if not isinstance(record["taskName"], str) or not record["taskName"]:
        raise TimesheetDataError(f"Record at index {index} has invalid taskName")


def _format_task(task: dict[str, Any], total_minutes: int) -> dict[str, Any]:
    return {
        "taskId": task["taskId"],
        "taskName": task["taskName"],
        "totalMinutes": task["totalMinutes"],
        "percentage": _format_percentage(task["totalMinutes"], total_minutes),
    }


def _format_percentage(minutes: int, total_minutes: int) -> str:
    if total_minutes == 0:
        return "0.00%"

    return f"{minutes / total_minutes * 100:.2f}%"


def _find_most_distinct_user(employees: dict[int, dict[str, Any]]) -> dict[str, Any] | None:
    if not employees:
        return None

    sorted_by_distinct_tasks = sorted(
        employees.values(),
        key=lambda employee: (-len(employee["taskIds"]), employee["userId"]),
    )
    employee = sorted_by_distinct_tasks[0]
    task_ids = sorted(employee["taskIds"])

    return {
        "userId": employee["userId"],
        "userName": employee["userName"],
        "distinctTasks": len(task_ids),
        "taskIds": task_ids,
    }
