# Importiert die nötigen Libraries und Funktionen für das Python-Skript.
import uuid
from flask import Flask, request, jsonify, abort

# Initialisiert den Flask-Server.
app = Flask(__name__)

# IDs für die initiale Datenstruktur erzeugen.
# Todo-Listen haben für bessere Testbarkeit eine feste ID.
user_id_bob = uuid.uuid4()
user_id_alice = uuid.uuid4()
user_id_eve = uuid.uuid4()
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

# Datenstruktur für die User.
user_list = [
    {'id': user_id_bob, 'name': 'Bob'},
    {'id': user_id_alice, 'name': 'Alice'},
    {'id': user_id_eve, 'name': 'Eve'},
]

# Datenstruktur für Todo-Listen.
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]

# Datenstruktur für die Einträge einer Todo-Liste, zugeordnet durch 'list' (Todo-Listen ID) und durch 'user' (User ID).
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id, 'user': user_id_bob},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id, 'user': user_id_alice},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id, 'user': user_id_eve},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id, 'user': user_id_eve},
]


@app.route('/todo-list/<list_id>', methods=['GET'])
def getTodoList(list_id: int):
    if not listExists(list_id):
        abort(404)
    
    return jsonify([i for i in todos if i['list'] == list_id]), 200


@app.route('/todo-list/<list_id>', methods=['DELETE'])
def deleteTodoList(list_id: int):
    if not listExists(list_id):
        abort(404)
    
    list_item = None

    for todo_list in todo_lists:
        if todo_list['id'] == list_id:
            list_item = todo_list
    
    todo_lists.remove(list_item)

    return '', 200


@app.route('/todo-list', methods=['POST'])
def addTodoList():
    new_list = request.get_json(force=True)
    new_list['id'] = uuid.uuid4()

    todo_lists.append(new_list)

    return jsonify(new_list), 200

@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def addEntryToTodoList(list_id: int):
    new_entry = request.get_json(force=True)
    new_entry['id'] = uuid.uuid4()
    new_entry['list'] = list_id

    todos.append(new_entry)

    return jsonify(new_entry), 200


@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT'])
def updateEntryFromTodoList(list_id, entry_id):
    if not listExists(list_id):
        abort(404)

    entry = jsonify([i for i in todos if i['id'] == entry_id])
    new_entry = request.get_json(force=True)

    entry['name'] = new_entry['name']
    entry['description'] = new_entry['description']

    return entry, 200
    

@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['DELETE'])
def deleteEntryFromTodoList(list_id, entry_id):
    if not listExists(list_id):
        abort(404)
    
    entry_item = None

    for todo in todos:
        if todo['id'] == entry_id:
            entry_item = todo

    todos.remove(entry_item)

    return '', 200

@app.route('/user', methods=['GET'])
def getUsers():
    return jsonify(user_list), 200

@app.route('/user', methods=['POST'])
def addUser():
    new_user = request.get_json(force=True)
    new_user['id'] = uuid.uuid4()

    user_list.append(new_user)

    return jsonify(new_user), 200

@app.route('/user/<user_id>', methods=['DELETE'])
def deleteUser(user_id):
    user_item = None

    for user in user_list:
        if user['id'] == user_id:
            user_item = user
        
    if not user_item:
        abort(404)

    user_list.remove(user_item)

    return '', 200

def listExists(list_id: int):
    list_item = None

    for todo_list in todo_lists:
        if todo_list['id'] == list_id:
            list_item = todo_list
        
    if not list_item:
        return False

    return True

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=1)
