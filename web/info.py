import sqlite3 as db
# *Importamos la libreria para conectar con sqlite3 como db
import json
# *Importar la libreria para leer y escribir json
from flask import redirect, make_response
from statistics import mode
import hashlib
# conectar con la base de datos mediante la ruta

def data_db():
    #conexion con la base de datos
    route = db.connect('db/data.sqlite3')
    try:
        # *Seleccionar todo la informacion de la base de datos desde la tabla Users
        users = route.execute("SELECT * FROM Users").fetchall()
        info_json = []
        for user in users:
            data = {
                "id" : user[0],
                "user" : user[1],
                "password" : user[2]
            }
            info_json.append(data)
        # *Abrir el archivo json en el que se escribira la informacion
        document = open('static/json/user.json', 'w')
        # *Escribir los datos obtenidos desde la db para posteriormente usarlos en el front-end
        json.dump(info_json, document, indent=4)
        # *Cerrar el documento para que se escriba la información
        document.close()
        print("Datos obtenidos")
    # !Lanzar una frase en caso de que haya un error de operacion con la base de datos
    except db.OperationalError:
        print("ptm otro error")

def auth_user(user_name, password):
    route = db.connect('db/data.sqlite3')
    try:
        user_name_DB = route.execute("SELECT * FROM Users WHERE user_name='{}'".format(user_name)).fetchall()
        document = open('static/json/user.json', "w")
        json.dump(user_name_DB, document, indent=4)
        document.close()
    except db.OperationalError:
        print("ptm un error")
    print(len(user_name_DB) == 1)
    if(len(user_name_DB) == 1):
        username_DB = user_name_DB[0][1]
        password_DB = user_name_DB[0][2]
    else:
        password_DB = "0"
        username_DB = "0"
    if user_name == username_DB and password == password_DB:
        dates = [True, user_name_DB[0][0]]
        return dates
    else:
        dates = [False, 0]
        return dates


def create_user_db(username, password):
    route = db.connect('db/data.sqlite3')
    try:
        id = len(route.execute("SELECT id FROM Users").fetchall()) + 1
        route.execute("INSERT INTO Users VALUES ({}, '{}', '{}')".format(id, username, password))
        route.commit()
        route.close()
    except db.OperationalError:
        print('PTM un error')

def modify_username_db(new_username, id):
    route = db.connect('db/data.sqlite3')
    try:
        route.execute("UPDATE Users SET user_name='{}' WHERE id={}".format(new_username, int(id)))
        route.commit()
        route.close()
    except db.OperationalError:
        print("PTM un error")

def modify_password_db(new_password, id):
    route = db.connect('db/data.sqlite3')
    try:
        route.execute("UPDATE Users SET user_password='{}' WHERE id={}".format(new_password, int(id)))
        route.commit()
        route.close()
    except db.OperationalError:
        print('PTM un error')
