import pytest
import os
import json
from todo import add_todo, remove_todo, load_todos, TODO_FILE

@pytest.fixture
def clean_todo_file():
    # Setup
    if os.path.exists(TODO_FILE):
        os.remove(TODO_FILE)
    yield
    # Teardown
    if os.path.exists(TODO_FILE):
        os.remove(TODO_FILE)

def test_add_todo(clean_todo_file):
    add_todo("Test task")
    todos = load_todos()
    assert todos == ["Test task"]

def test_remove_todo(clean_todo_file):
    add_todo("Test task")
    remove_todo("Test task")
    todos = load_todos()
    assert todos == []

def test_list_empty(clean_todo_file):
    todos = load_todos()
    assert todos == []
