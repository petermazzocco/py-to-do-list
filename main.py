from typing import TypedDict
from typing_extensions import Any, Optional
import typer
import json
import uuid

app = typer.Typer()

class ToDoItem(TypedDict):
    id: int
    task: str
    completed: bool

# Mock JSON DB
db = "tasks.json"

# Find a task by ID in the JSON file
def findTaskById(id: int) -> Optional[ToDoItem]:
    try:
        with open(db, "r") as file:
            tasks = json.load(file)

            for item in tasks:
                if item["id"] == id:
                    return item

            return None
    except FileNotFoundError:
        return None

# CLI COMMANDS
@app.command()
def create(task: str, completed: bool = False):
    id = uuid.uuid4().int

    todo_item: ToDoItem = {"id": id, "task": task, "completed": completed}

    try:
        with open(db, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(todo_item)

    with open(db, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Added '{task}' to list (completed: {completed})")

@app.command()
def remove(id: int):
    task = findTaskById(id)

    if task:
        with open(db, 'r') as file:
            to_do_list = json.load(file)
            to_do_list.remove(task)
            with open(db, "w") as file:
                json.dump(to_do_list, file, indent=4)
            print(f"List after: {to_do_list}")
    else:
        print(f"Task with ID {id} not found")


@app.command()
def list():
    try:
        with open(db, 'r') as file:
            to_do_list = json.load(file)
            print(f"{to_do_list}")

            if not to_do_list:
                print("No tasks found.")
                return

            if len(to_do_list) == 0:
                print("No tasks found.")
                return

            for i, item in enumerate(to_do_list, 1):
                status = "✓" if item["completed"] else "✗"
                print(f"{i}. [{status}] {item['task']}")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No file found")
        return

if __name__ == "__main__":
    app()
