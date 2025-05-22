from flask import Flask, render_template, url_for, flash, redirect, request, session
from forms import RegistrationForm, LogInForm
import requests
import uuid

app = Flask(__name__)
app.secret_key = 'mikumikumi3939'

#APIs
api_obtener_productos = "http://127.0.0.1:5001/productos"
api_ver_carrito = "http://127.0.0.1:5001/carrito"
api_vaciar_carrito = "http://127.0.0.1:5001/vaciar_carrito"
api_agregar_producto_carrito = "http://127.0.0.1:5001/agregar_producto_carrito"
api_eliminar_producto_carrito = "http://127.0.0.1:5001/carrito_eliminar_producto="


#Rutas de Templates
@app.route('/')
@app.route('/home')
def home():
    productos = requests.get(api_obtener_productos)
    data_productos = productos.json()
    print(data_productos)
    if data_productos:
        return render_template('home.html', data=data_productos)
    else:
        return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/carrito')
def carrito():
    ver_carrito = requests.get(api_ver_carrito)
    data_estado_carrito = ver_carrito.json()
    print(data_estado_carrito)
    if data_estado_carrito:
        return render_template('carrito.html', data=data_estado_carrito)
    else:
        return render_template('carrito.html')

@app.route('/agregar_carrito_ui', methods=['POST'])
def agregar_carrito_ui():
    try:
        producto_id = request.form.get('producto_id')
        cantidad = int(request.form.get('cantidad', 1))
        data = {
            'session_id': session['session_id'],
            'producto_id': producto_id,
            'cantidad': cantidad
        }
        requests.post(api_agregar_producto_carrito, json=data)
        response = requests.post(api_agregar_producto_carrito, json=data)
        if response.status_code == 200:
            flash('Producto agregado al carrito correctamente.', 'success')
        else:
            flash('No se pudo agregar el producto al carrito.', 'danger')
    except Exception as e:
        flash('Error interno al procesar el carrito.', 'danger')

    # Redirige a la página de productos o carrito
    return redirect(url_for('carrito'))

@app.route('/ver_carrito')
def ver_carrito():
    carrito = session.get('carrito', {})
    items = []
    total = 0

    for producto_id, cantidad in carrito.items():
        respuesta = requests.get(api_ver_carrito + str(producto_id))
        if respuesta.status_code == 200:
            producto = respuesta.json()
            subtotal = producto['valor'] * cantidad
            total += subtotal
            items.append({
                'id': producto_id,
                'nombre': producto['nombre_producto'],
                'cantidad': cantidad,
                'precio_unitario': producto['valor'],
                'subtotal': subtotal
            })
        else:
            pass

    return render_template('carrito.html', items=items, total=total)

#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
@app.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Su cuenta fue generada correctamente, Bienvenido {form.username.data}!', 'success')
        return redirect((url_for('home')))
    return render_template('register.html',form=form)

@app.route('/login', methods=["GET","POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        if form.email.data == 'reigigas7650@gmail.com' and form.password.data == 'lol':
            flash('Iniciaste sesion correctamente! :D','success')
            return redirect(url_for('home'))
        else:
            flash('Login Fallido XD', 'danger')
    return render_template('login.html',form=form)
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#

#Actualiza las modificaciones realizadas sin reiniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, port="5000")