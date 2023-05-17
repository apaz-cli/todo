#!/usr/bin/env python3
from flask import Flask, request, abort
from threading import Lock
from pickle import dumps, loads
from os.path import exists

app = Flask(__name__)
list_loc = "./TODO_LISTS"
list_lock = Lock()
TODO_LISTS = None


def todo_new():
    global TODO_LISTS, list_lock, list_loc
    try:
        if exists(list_loc):
            with open(list_loc, 'rb') as f:
                TODO_LISTS = loads(f.read())
    except:
        pass
    if not TODO_LISTS:
        TODO_LISTS = {}
    print(f"Loaded {len(TODO_LISTS)} todo lists.")
todo_new()

def todo_get(user_id):
    global TODO_LISTS, list_lock
    with list_lock:
        if user_id in TODO_LISTS:
            return TODO_LISTS[user_id]
        else:
            abort(404)

def todo_set(user_id, list):
    global TODO_LISTS, list_lock, list_loc
    with list_lock:
        TODO_LISTS[user_id] = list
        try:
            with open(list_loc, 'wb') as f:
                f.write(dumps(TODO_LISTS))
        except:
            print("Failed to save TODO lists.")
            abort(500)

@app.route('/', methods=['GET'])
def get_todo_list():
    user_id = request.headers.get('X-User-ID')
    return todo_get(user_id)

@app.route('/', methods=['POST'])
def upload_todo_list():
    user_id = request.headers.get('X-User-ID')
    todo_list = request.files['file'].read().decode('utf-8')
    todo_set(user_id, todo_list)
    return "OK"

if __name__ == '__main__':
    app.run()
