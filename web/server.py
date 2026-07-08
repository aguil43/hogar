#from crypt import methods
from http import cookies
from urllib import request, response
from flask import Flask, jsonify, render_template, url_for, make_response
from flask import request as req
from venta import *
from info import *
from variable import *
import time

# TODO: Todas las acciones que estan en GET cambiarlas a POST 

app = Flask(__name__)

# Ruta para mostrar la pagina de inicio donde se mostrara
@app.route('/')
def inicio():
    url_for('static', filename='css/home.css')
    url_for('static', filename='img/croquis.png')
    return render_template('html/home.html')

# El inicio de sesion se gestiona desde la misma ruta, pero se define por el tipo de peticion recibido 
@app.route('/login', methods=['GET', 'POST'])
def saludo():
    # Segun el metodo usado en la peticion post, se define si tiene que mostrar la pagina o comprobar el inicio de sesion
    if req.method == 'POST':
        user_name = req.form['username']
        password = req.form['password']
        print(user_name)
        print(password)
        bool = auth_user(user_name, password)
        print(bool)
        if bool[0] == True:
            resp = make_response(redirect('/'))
            resp.set_cookie('log', 'True')
            resp.set_cookie('id', '{}'.format(bool[1]))
            return resp
        else:
            return redirect('/err') 
    else:
        data_db()
        url_for('static', filename='style.css')
        url_for('static', filename='app.js')
        return render_template('index.html')

# Pagina de error, renderiza la pagina principal pero mostrando un mensaje de error 
@app.route('/err')
def err():
    return render_template('index.html', err=True)

# Ruta para mostrar todos los productos faltantes en la tienda
@app.route('/compras')
def compras():
    data_stock()
    url_for('static', filename='js/lista.js')
    url_for('static', filename='css/lista.css')
    return render_template('html/lista.html')

# Ruta para mostrar los productos existentes en la tienda
@app.route('/venta')
def venta():
    data_stock()
    url_for('static', filename='css/productos.css')
    url_for('static', filename='js/ventas.js')
    return render_template('html/productos.html')

# Mostrar la informacion de algun producto y realizar su venta
@app.route('/store/<product_name>')
def variable(product_name):
    data_stock()
    charge_product(product_name)
    url_for('static', filename='css/variable.css')
    return render_template('html/variable.html')

# Realizar la accion de agregar stock a un producto
@app.route('/store/<product_name>/fill/<filled>')
def fill_route(product_name, filled):
    fill(product_name, filled)
    time.sleep(3)
    return redirect('/store/' + product_name)

# Realizar la accion de vender un producto
@app.route('/store/<product_name>/sell/<selled>')
def sell_route(product_name, selled):
    sell(product_name, selled)
    time.sleep(3)
    return redirect('/store/' + product_name)

# Realizar la accion de cambiar un precio
@app.route('/store/<product_name>/changeprice/<new_price>')
def price(product_name, new_price):
    change_price(product_name, new_price)
    time.sleep(3)
    return redirect('/store/' + product_name)

# Realizar la accion de agregar un nuevo producto
@app.route('/store/new/<new_product>')
def create(new_product):
    create_product(new_product)
    time.sleep(3)
    return redirect('/store/' + new_product)

# Pagina para crear o eliminar usuarios
@app.route('/users')
def users():
    data_db()
    return render_template('html/usuarios.html')

# Accion de crear usuario
@app.route('/users/createuser/<user_name>/<password>')
def create_user(user_name, password):
    create_user_db(user_name, password)
    time.sleep(3)
    return redirect('/users')

# Accion para modificar un nombre de usaurio 
@app.route('/users/modify/username/<change_user>/<id>')
def modify_username(change_user, id):
    modify_username_db(change_user, id)
    # ! Funcion para modificar el nombre de usuario correspondiente
    time.sleep(3)
    return redirect('/users')

# Accion para cambiar una contrasena
@app.route('/users/modify/password/<change_password>/<id>')
def modify_password(change_password, id):
    modify_password_db(change_password, id)
    # ! Funcion para cambiar la contraseña del usuario
    time.sleep(3)
    return redirect('/users')

# Condicion para ejecutar el archivo de server como un script
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=8080)
