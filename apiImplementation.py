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
    '''
        Ermittelt, anhand der List-ID, die dazugehörige ToDo-Liste.
        Methode: GET
        
        Wenn eine ToDo-Liste mit der angegebenen ID nicht existiert wird der Code 404 zurückgegeben.
        Das Ergebnis wird als JSON zurückgegeben, mit dem Code 200.
        
        Beispiel: /todo-list/1 - Gibt die ToDo-Liste mit der ID "1" zurück.
    '''
    if not listExists(list_id):
        abort(404)
    
    return jsonify([i for i in todos if i['list'] == list_id]), 200


@app.route('/todo-list/<list_id>', methods=['DELETE'])
def deleteTodoList(list_id: int):
    '''
        Löscht, anhand der List-ID, die dazugehörige ToDo-Liste.
        Methode: DELETE
        
        Wenn eine ToDo-Liste mit der angegebenen ID nicht existiert wird der Code 404 zurückgegeben.
        Bei Erfolg wird ein leerer String mit dem Code 200 zurückgegeben. (Die erste Rückgabe kann Disposed (_) werden.)
        
        Beispiel: /todo-list/1 - Löscht die Liste mit der ID "1".
    '''
    if not listExists(list_id):
        abort(404)
    
    # Die zu löschende Liste suchen.
    list_item = None

    for todo_list in todo_lists:
        if todo_list['id'] == list_id:
            list_item = todo_list
    
    todo_lists.remove(list_item)

    return '', 200


@app.route('/todo-list', methods=['POST'])
def addTodoList():
    '''
        Fügt eine ToDo-Liste hinzu.
        Methode: POST
        
        Der neuen ToDo-Liste wird eine zufällige ID (UUID4) zugewiesen.
        Die neue ToDo-Liste wird in JSON zurückgegeben, zusammen mit dem Code 200.
        
        Beispiel: /todo-list/
    '''
    new_list = request.get_json(force=True)
    new_list['id'] = uuid.uuid4()

    todo_lists.append(new_list)

    return jsonify(new_list), 200

@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def addEntryToTodoList(list_id: int):
    '''
        Fügt einen Eintrag einer ToDo-Liste, mit der ID (list_id), hinzu.
        Methode: POST
        
        Dem neuen Eintrag wird eine zufällige ID (UUID4) zugewiesen.
        Der neue Eintrag wird in JSON zurückgegeben, zusammen mit dem Code 200.
        
        Beispiel: todo-list/1/entry
    '''
    new_entry = request.get_json(force=True)
    new_entry['id'] = uuid.uuid4()
    new_entry['list'] = list_id

    todos.append(new_entry)

    return jsonify(new_entry), 200


@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT'])
def updateEntryFromTodoList(list_id, entry_id):
    '''
        Aktualisiert einen Eintrag einer ToDo-Liste, mit der ID (list_id), der die ID (entry_id) hat.
        Methode: PUT
        
        Wenn die ToDo-Liste nicht existiert, wird der Code 404 zurückgegeben.
        Wenn der Eintrag in der Liste nicht existiert, wird ebenfalls der Code 404 zurückgegeben.
        Das Ergebnis wird als JSON zurückgegeben, mit dem Code 200.
        
        Beispiel: /todo-list/1/entry/1
    '''
    if not listExists(list_id):
        abort(404)

    # Existiert dieser Eintrag?
    entry_item = None
    for todo in todos:
        if todo['id'] == entry_id:
            entry_item = todo
    
    # Wenn nicht, 404 zurückgeben.
    if not entry_item:
        abort(404)
    
    entry = jsonify([i for i in todos if i['id'] == entry_id])
    new_entry = request.get_json(force=True)

    entry['name'] = new_entry['name']
    entry['description'] = new_entry['description']

    return jsonify(entry), 200
    

@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['DELETE'])
def deleteEntryFromTodoList(list_id, entry_id):
    '''
        Löscht einen Eintrag, mit der ID (entry_id), aus der ToDo-Liste, mit der ID (list_id)
        Methode: DELETE
        
        Wenn die Liste nicht existiert, wird der Code 404 zurückgegeben.
        Wenn der Eintrag in der Liste nicht existiert, wird ebenfalls der Code 404 zurückgegeben.
        Als Ergebnis wird ein leerer String, mit dem Code 200 zurückgegeben. (Den ersten Rückgabewert kann man Disposen (_))
        
        Beispiel: /todo-list/1/entry/1
    '''
    if not listExists(list_id):
        abort(404)
    
    entry_item = None

    # Existiert dieser Eintrag?
    for todo in todos:
        if todo['id'] == entry_id:
            entry_item = todo
    
    # Wenn nicht, 404 zurückgeben.
    if not entry_item:
        abort(404)
    
    todos.remove(entry_item)

    return '', 200

@app.route('/user', methods=['GET'])
def getUsers():
    '''
        Gibt eine Liste aller Nutzer aus.
        Methode: GET
        
        Das Ergebnis wird als JSON zurückgegeben, zusammen mit dem Code 200.
        
        Beispiel: /user
    '''
    return jsonify(user_list), 200

@app.route('/user', methods=['POST'])
def addUser():
    '''
        Fügt einen neuen Nutzer hinzu.
        Methode: POST
        
        Dem Nutzer wird eine zufällige ID (UUID4) zugewiesen.
        Das Ergebnis wird als JSON zurückgegeben, zusammen mit dem Code 200.
        
        Beispiel: /user
    '''
    new_user = request.get_json(force=True)
    new_user['id'] = uuid.uuid4()

    user_list.append(new_user)

    return jsonify(new_user), 200

@app.route('/user/<user_id>', methods=['DELETE'])
def deleteUser(user_id):
    '''
        Löscht einen Nutzer mit der ID (user_id)
        Methode: DELETE
        
        Wenn der Nutzer mit der ID nicht existiert, wird der Code 404 zurückgegeben.
        Als Ergebnis wird ein leerer String, zusammen mit dem Code 200 zurückgegeben. (Der erste Rückgabewert kann Disposed werden (_))
        
        Beispiel: /user/2
    '''
    user_item = None

    # Existiert dieser User?
    for user in user_list:
        if user['id'] == user_id:
            user_item = user
        
    # Wenn nicht, 404 zurückgeben.
    if not user_item:
        abort(404)

    user_list.remove(user_item)

    return '', 200

def listExists(list_id: int):
    '''
        Überprüft, ob die Liste, mit der übergebenen list_id, existiert.
    '''
    list_item = None

    # Existiert diese Liste?
    for todo_list in todo_lists:
        if todo_list['id'] == list_id:
            list_item = todo_list
    
    # Wenn nicht, False zurückgeben.
    if not list_item:
        return False # Im Kontext "if not" verwendet.

    # Die Liste existiert.
    return True # Im Kontext "if not" verwendet.

# Applikation mit Flask starten.
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=1)
