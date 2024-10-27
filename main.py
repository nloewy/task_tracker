import json
import os
from datetime import datetime
import argparse

JSON_FILE_NAME = "info.json"

def add(description):
    data = read_data()
    task_id = str(int(max(data.keys(), key = lambda x: int(x))) + 1)
    curr_time = str(datetime.now().strftime("%Y-%m-%d %H:%M"))
    data[task_id]={
        "description": description,
        "status": "TODO",
        "createdAt": curr_time,
        "modifiedAt": curr_time}
    write_data(data)
    print(f"Task added successfully (ID : {task_id})") 

def update(task_id, new_description):
    data = read_data()
    print(data.keys())
    if task_id not in data:
        raise Exception("Data with ID={task_id} not found.")
    data[task_id]["description"] = new_description
    data[task_id]["modifiedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    write_data(data)

def mark(task_id, new_marker):
    print(new_marker)
    if new_marker not in ["todo", "in-progress", "done"]:
        raise Exception(f"Marker {new_marker} is not valid. Must be todo, in-progress, or done")
    data = read_data()
    if task_id not in data:
        raise Exception("Data with ID={task_id} not found.")
    data[task_id]["status"] = new_marker
    write_data(data)

def list(list_only = None):
    if list_only and list_only not in ["todo", "in-progress", "done"]:
        raise Exception(f"Marker {list_only} is not valid. Must be todo, in-progress, or done (or left blank)")
    data = read_data()
    for id, task in data.items():
        if not list_only or task["status"] == list_only:
            print(f"Task ID {id} : Description {task['description']}. Last Modified {task['modifiedAt']}")

def delete(task_id):
    data = read_data()
    if task_id not in data:
        raise Exception("Data with ID={task_id} not found.")
    del data[task_id]
    write_data(data)

def write_data(data):
    with open(JSON_FILE_NAME, 'w') as write_file:
        json.dump(data, write_file)

def read_data():
    if not os.path.exists(JSON_FILE_NAME):
        return {}
    with open(JSON_FILE_NAME) as file:
        data = json.load(file)
    return data
        
def main():
    parser = argparse.ArgumentParser(description="A command-line tool for managing tasks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_add = subparsers.add_parser("add", help="Add an item")
    parser_add.add_argument("item", help="The item to add")

    parser_update = subparsers.add_parser("update", help="Update an item")
    parser_update.add_argument("item", help="The item to update")
    parser_update.add_argument("value", help="The new value for the item")

    parser_mark_in_progress = subparsers.add_parser("mark-in-progress", help="Mark item as in-progress")
    parser_mark_in_progress.add_argument("item", help="The item to mark as in-progress")

    parser_mark_done = subparsers.add_parser("mark-done", help="Mark item as done")
    parser_mark_done.add_argument("item", help="The item to mark as done")

    parser_list = subparsers.add_parser("list", help="List items")
    parser_list.add_argument("status", nargs="?", default=None, help="Optional status to filter list")

    parser_delete = subparsers.add_parser("delete", help="Delete an item")
    parser_delete.add_argument("item", help="The item to delete")

    args = parser.parse_args()

    if args.command == "add":
        add(args.item)
    elif args.command == "update":
        update(args.item, args.value)
    elif args.command == "mark-in-progress":
        mark(args.item, "in-progress")
    elif args.command == "mark-done":
        mark(args.item, "done")
    elif args.command == "list":
        list(args.status)
    elif args.command == "delete":
        delete(args.item)
    else:
        raise Exception("Invalid Command")

if __name__ == "__main__":
    main()