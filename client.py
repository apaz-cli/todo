#!/usr/bin/env python3
import subprocess


USER_ID = "Violet"
SERVER_URL = "http://127.0.0.1:5000"


def read_todo_list():
    response = subprocess.run(
        ["curl", "-s", "-f", "-H", f"X-User-ID: {USER_ID}", SERVER_URL],
        capture_output=True,
        text=True,
    )

    if response.returncode == 22:
        return ""
    elif response.returncode == 0:
        return response.stdout
    else:
        return None


def write_todo_list(todo_list):
    with open("todo.txt", "w") as file:
        file.write(todo_list)
    response = subprocess.run(
        [
            "curl",
            "-s",
            "-F",
            "file=@todo.txt",
            "-H",
            f"X-User-ID: {USER_ID}",
            SERVER_URL,
        ],
        capture_output=True,
        text=True,
    )
    if response.returncode != 0:
        print("Failed to upload TODO list.")


def edit_todo_list():
    todo_list = read_todo_list()
    if todo_list is not None:
        with open("todo_tmp.txt", "w") as file:
            file.write(todo_list)

        subprocess.run(["nano", "todo_tmp.txt"])

        with open("todo_tmp.txt", "r") as file:
            edited_list = file.read()

        write_todo_list(edited_list)
        subprocess.run(["rm", "todo_tmp.txt"])
    else:
        print("Failed to communicate with TODO list server.")


edit_todo_list()