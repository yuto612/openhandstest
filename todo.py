import argparse
import json
import os

TODO_FILE = "todo.json"

def load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f)

def add_todo(task):
    todos = load_todos()
    todos.append(task)
    save_todos(todos)
    print(f"Added: {task}")

def remove_todo(task):
    todos = load_todos()
    if task in todos:
        todos.remove(task)
        save_todos(todos)
        print(f"Removed: {task}")
    else:
        print(f"Task not found: {task}")

def list_todos():
    todos = load_todos()
    if not todos:
        print("No tasks.")
    else:
        for i, task in enumerate(todos, 1):
            print(f"{i}. {task}")

def main():
    parser = argparse.ArgumentParser(description="Simple TODO CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("task", type=str)

    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("task", type=str)

    subparsers.add_parser("list")

    args = parser.parse_args()

    if args.command == "add":
        add_todo(args.task)
    elif args.command == "remove":
        remove_todo(args.task)
    elif args.command == "list":
        list_todos()

if __name__ == "__main__":
    main()
