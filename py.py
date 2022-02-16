from flask import Flask

# Methoden sind erstmal nur imaginär.
# (Keine DB vorhanden, kein Plan von Schlange und DBs, zu faul zu googlen)

app = Flask(__name__)

# HOLT DIE TODO LISTE MIT DER ID _LIST_ID_.
@app.route('/todo-list/<list_id>', methods=['GET'])
def getTodoList(list_id: int):
    return "Todolist: " + list_id

# LÖSCHT DIE TODO LISTE MIT DER ID _LIST_ID_.
@app.route('/todo-list/<list_id>', methods=['DELETE'])
def deleteTodoList(list_id: int):
    return "Yo diggi, Liste " + list_id + " wird gelöscht, allah."

# FÜGT EINE NEUE LISTE HINZU, ID WIRD AUTOMATISCH VERGEBEN (DB).
@app.route('/todo-list', methods=['POST'])
def addTodoList():
    return "Liste 42069 wurde hinzugefügt."

# FÜGT EINEN EINTRAG EINER TODO LISTE HINZU.
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def addEntryToTodoList(list_id: int):
    return "Da ist ein neuer Eintrag in der Todo-Liste " + list_id

# AKTUALISIERT EINEN EINTRAG EINER TODO LISTE.
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT'])
def updateEntryFromTodoList(list_id, entry_id):
    return "Eintrag " + entry_id + " wird in Todo Liste " + list_id + " aktualisiert"

# LÖSCHT EINEN EINTRAG EINER TODO LISTE.
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['DELETE'])
def deleteEntryFromTodoList(list_id, entry_id):
    return "Eintrag " + entry_id + " wird in Todo Liste " + list_id + " gelöscht"

# HOLT EINE LISTE ALLER BENUTZER
@app.route('/user', methods=['GET'])
def getUsers():
    return "Hier stehen Benutzer digga."

# FÜGT EINEN BENUTZER HINZU
@app.route('/user', methods=['POST'])
def addUser():
    return "Benutzer wurde erstellt"

# LÖSCHT EINEN BENUTZER
@app.route('/user/<user_id>', methods=['DELETE'])
def deleteUser(user_id):
    return "Benutzer" + user_id + "wird gelöscht."

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=1)