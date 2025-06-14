import argparse
import enum
import json
import os
from datetime import datetime, timedelta, timezone
from pprint import pprint

DB_PATH = 'db.json'

class StatusEnum(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

def add_task(tasks: dict, description: str):
    task_id = int(max(tasks.keys()))+1 if tasks else 1
    time = datetime.now(timezone(timedelta(hours=-4))).isoformat()
    tasks[task_id] = {
        "description": description,
        "status": StatusEnum.TODO.value,
        "createdAt":time,
        "updatedAt":time
    }
    return tasks, f"Created new task: (ID: {task_id})"

def update_task(tasks: dict, task_id: int, new_description: str):
    if task_id not in tasks:
        raise Exception(f"Task id {task_id} does not exist")
    tasks[task_id]["description"] = new_description
    tasks[task_id]["updatedAt"] = datetime.now(timezone(timedelta(hours=-4))).isoformat()
    return tasks, f"Task updated successfully"

def delete_task(tasks: dict, task_id: int):
    if task_id not in tasks:
        raise Exception(f"Task id {task_id} does not exist")
    del tasks[task_id]
    return tasks, f"Task deleted successfully"

def list_tasks(tasks: dict, filter_by: str):
    if filter_by not in StatusEnum._value2member_map_:
        raise Exception(f"Cannot filter by {filter_by}")
    result = []
    for task_id, task in tasks.items():
        if not filter_by or task.get("status") == filter_by:
            result.append(
                {
                    "id": task_id,
                    "description": task["description"],
                    "createdAt": task["createdAt"],
                    "updatedAt": task["updatedAt"],
                    "status": task["status"]
                }
            )
    pprint(result, indent=4)
    return None, None

def mark_task_in_progress(tasks: dict, task_id: int):
    tasks[task_id]["status"] = StatusEnum.IN_PROGRESS.value
    return tasks, f"Task moved to 'in-progress'"

def mark_task_done(tasks: dict, task_id: int):
    tasks[task_id]["status"] = StatusEnum.DONE.value
    return tasks, f"Task moved to 'done'"

def __main__():
    args = _get_parser()
    tasks = _read_db()
    try:
        if args.command == "add":
            updated_tasks, msg = add_task(tasks, args.description)
        elif args.command == "update":
            updated_tasks, msg = update_task(tasks, args.task_id, args.description)
        elif args.command == "delete":
            updated_tasks, msg = delete_task(tasks, args.task_id)
        elif args.command == "mark-in-progress":
            updated_tasks, msg = mark_task_in_progress(tasks, args.task_id)
        elif args.command == "mark-done":
            updated_tasks, msg = mark_task_done(tasks, args.task_id)
        elif args.command == "list":
            updated_tasks, msg = list_tasks(tasks,args.status)
        else:
            print(f"Unknown command: {args.command}")
            return
        if updated_tasks is not None:
            _write_to_db(updated_tasks)
        if msg:
            print(msg)
    except Exception as e:
        print(f"Error: {str(e)}")

def _read_db() -> dict:
    if os.path.exists(DB_PATH):
        with open(DB_PATH) as json_file:
            data = json.load(json_file)
            return data
    else:
        return dict()

def _write_to_db(data: dict) -> None:
    with open(DB_PATH, 'w') as json_file:
        json.dump(data, json_file)

def _get_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A command-line tool for managing tasks.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", help="The description of the task to add")
    parser_update = subparsers.add_parser("update", help="Update a task")
    parser_update.add_argument("task_id", help="The id of task to update")
    parser_update.add_argument("description", help="The new description for the task")
    parser_mark_in_progress = subparsers.add_parser("mark-in-progress", help="Mark task as in-progress")
    parser_mark_in_progress.add_argument("task_id", help="The id of the task to mark in progress")
    parser_mark_done = subparsers.add_parser("mark-done", help="Mark task as done")
    parser_mark_done.add_argument("task_id", help="The id of the task to mark as done")
    parser_list = subparsers.add_parser("list", help="List tasks")
    parser_list.add_argument("status", nargs="?", help="Optional status to filter list")
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("task_id", help="The task_id to delete")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    __main__()