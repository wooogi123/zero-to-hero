from dataclasses import dataclass
from typing import Any
from uuid import uuid4


@dataclass
class Todo:
    id: str
    title: str
    content: str
    is_done: bool


@dataclass
class State:
    todos: list[Todo]


class Store:
    state: State = State(todos=[])

    def dispatch(self, type: str, payload: Any):
        match (type, payload):
            case ("add", {"title": title, "content": content}):
                self.state.todos.append(
                    Todo(
                        id=uuid4().hex,
                        title=title,
                        content=content,
                        is_done=False,
                    )
                )
            case ("done", {"id": id}):
                for todo in self.state.todos:
                    if todo.id == id:
                        todo.is_done = True
            case ("delete", {"id": id}):
                self.state.todos = [t for t in self.state.todos if t.id != id]


def print_init():
    print("1. All todos")
    print("2. Add todo")
    print("3. Done todo")
    print("4. Delete todo")


def main():
    store = Store()

    while True:
        print_init()

        option = int(input("Select: "))

        match option:
            case 1:
                print(store.state.todos)
            case 2:
                title = input("Title: ")
                content = input("Content: ")
                store.dispatch(type="add", payload={"title": title, "content": content})
            case 3:
                id = input("Todo id: ")
                store.dispatch(type="done", payload={"id": id})
            case 4:
                id = input("Todo id: ")
                store.dispatch(type="delete", payload={"id": id})


if __name__ == "__main__":
    main()
