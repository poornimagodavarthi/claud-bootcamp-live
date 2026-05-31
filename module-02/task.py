#!/usr/bin/env python3
"""task — a single-file CLI task manager.

Stores tasks in a JSON file (tasks.json) in the current working directory.
Stdlib only. Exit codes: 0 success, 1 user error, 2 internal error.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TASKS_FILE = Path("tasks.json")

EXIT_OK = 0
EXIT_USER_ERROR = 1
EXIT_INTERNAL_ERROR = 2


class UserError(Exception):
    """Raised for invalid user input (maps to exit code 1)."""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_tasks() -> list[dict]:
    if not TASKS_FILE.exists():
        return []
    try:
        raw = TASKS_FILE.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Cannot read {TASKS_FILE}: {exc}") from exc
    if not raw.strip():
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{TASKS_FILE} is corrupted: {exc}") from exc
    if not isinstance(data, list):
        raise RuntimeError(f"{TASKS_FILE} is corrupted: expected a list of tasks")
    return data


def save_tasks(tasks: list[dict]) -> None:
    try:
        TASKS_FILE.write_text(
            json.dumps(tasks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    except OSError as exc:
        raise RuntimeError(f"Cannot write {TASKS_FILE}: {exc}") from exc


def next_id(tasks: list[dict]) -> int:
    return max((t["id"] for t in tasks), default=0) + 1


def find_task(tasks: list[dict], task_id: int) -> dict:
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise UserError(f"No task with id {task_id}")


def cmd_add(args: argparse.Namespace) -> int:
    text = args.text.strip()
    if not text:
        raise UserError("Task text cannot be empty")
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "status": "todo",
        "created_at": now_iso(),
        "text": text,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {task['text']}")
    return EXIT_OK


def cmd_list(_: argparse.Namespace) -> int:
    tasks = load_tasks()
    if not tasks:
        print('No tasks yet. Add one with: task add "..."')
        return EXIT_OK

    headers = ("ID", "STATUS", "CREATED_AT", "TEXT")
    rows = [
        (str(t["id"]), t["status"], t["created_at"], t["text"]) for t in tasks
    ]
    widths = [
        max(len(headers[i]), max(len(row[i]) for row in rows))
        for i in range(len(headers))
    ]
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*headers))
    for row in rows:
        print(fmt.format(*row))
    return EXIT_OK


def cmd_done(args: argparse.Namespace) -> int:
    tasks = load_tasks()
    task = find_task(tasks, args.id)
    task["status"] = "done"
    save_tasks(tasks)
    print(f"Marked #{task['id']} as done")
    return EXIT_OK


def cmd_delete(args: argparse.Namespace) -> int:
    tasks = load_tasks()
    task = find_task(tasks, args.id)
    tasks.remove(task)
    save_tasks(tasks)
    print(f"Deleted task #{task['id']}")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task", description="A single-file CLI task manager."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("text", help="The task description")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List all tasks")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="Mark a task as done")
    p_done.add_argument("id", type=int, help="The task id")
    p_done.set_defaults(func=cmd_done)

    p_delete = sub.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", type=int, help="The task id")
    p_delete.set_defaults(func=cmd_delete)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except UserError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_USER_ERROR
    except Exception as exc:  # noqa: BLE001 — top-level safety net
        print(f"Internal error: {exc}", file=sys.stderr)
        return EXIT_INTERNAL_ERROR


if __name__ == "__main__":
    sys.exit(main())
