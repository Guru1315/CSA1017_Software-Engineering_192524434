#!/usr/bin/env python3
"""A lightweight local CLI To-Do application."""

import argparse
import json
import sys
from pathlib import Path

TASKS_FILE = Path(__file__).resolve().parent / "tasks.json"


def load_tasks() -> dict:
    """Load tasks from tasks.json; return an empty dict if the file is missing."""
    if not TASKS_FILE.exists():
        return {}
    try:
        with TASKS_FILE.open("r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {}
            data = json.loads(content)
    except json.JSONDecodeError:
        print("Error: Could not read tasks file (invalid JSON)", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, dict):
        print("Error: Could not read tasks file (unexpected format)", file=sys.stderr)
        sys.exit(1)
    return data


def save_tasks(tasks: dict) -> None:
    """Persist tasks to tasks.json with indentation."""
    with TASKS_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(description: str) -> None:
    """Validate and add a new task, then print confirmation."""
    if description is None or not description.strip():
        print("Error: Task description cannot be empty", file=sys.stderr)
        sys.exit(1)
    description = description.strip()

    tasks = load_tasks()
    int_ids = []
    for key in tasks:
        try:
            int_ids.append(int(key))
        except ValueError:
            continue
    new_id = (max(int_ids) + 1) if int_ids else 1

    tasks[str(new_id)] = description
    save_tasks(tasks)
    print(f"Task added: [{new_id}] {description}")


def list_tasks() -> None:
    """Print all tasks, or a message if none exist."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    def sort_key(item):
        try:
            return (0, int(item[0]))
        except ValueError:
            return (1, 0)

    for task_id, description in sorted(tasks.items(), key=sort_key):
        print(f"[{task_id}] {description}")


def delete_task(task_id_str: str) -> None:
    """Delete a task by ID; exit with code 1 if the ID is invalid or missing."""
    try:
        task_id = int(task_id_str)
    except (ValueError, TypeError):
        print("Error: Task ID not found", file=sys.stderr)
        sys.exit(1)

    tasks = load_tasks()
    key = str(task_id)
    if key not in tasks:
        print("Error: Task ID not found", file=sys.stderr)
        sys.exit(1)

    del tasks[key]
    save_tasks(tasks)
    print(f"Task [{task_id}] deleted")


def main() -> None:
    """Configure the CLI and dispatch commands."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A simple command-line to-do list manager.",
    )
    subparsers = parser.add_subparsers(dest="command", title="commands")

    add_parser = subparsers.add_parser("add", help='Add a new task: todo add "<description>"')
    add_parser.add_argument("description", nargs="?", default=None,
                            help="Description of the task")

    subparsers.add_parser("list", help="List all tasks")

    delete_parser = subparsers.add_parser("delete", help="Delete a task by ID: todo delete <ID>")
    delete_parser.add_argument("id", help="ID of the task to delete")

    if len(sys.argv) <= 1:
        parser.print_help()
        return

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks()
    elif args.command == "delete":
        delete_task(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()