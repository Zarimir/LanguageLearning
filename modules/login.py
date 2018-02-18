import config
from modules.db import get_users


def login(username, password):
    users = get_users()
    return users.find_one({'username': username, 'password': password})


def register(username, password):
    users = get_users()
    if not users.find_one({'username' : username}):
        users.insert_one({'username': username, 'password': password})
        return True


def delete(username):
    users = get_users()
    return users.delete_one({'username': username}).deleted_count


username = "Archling"
password = "12"
print(login(username, password))
password = "123"
print(login(username, password))

print(register(username, password))
username = "Voidling"
print(register(username, password))

if delete(username):
    print("Deleted")

if delete(username):
    print("Deleted")

if delete(username):
    print("Deleted")