from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LogInForm
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '9cc5e035d4caa22b59b3a7fa6c08894d'

#APIs
api_obtener_productos = "http://127.0.0.1:5001/productos"

#Rutas de Templates
@app.route('/')
@app.route('/home')
def home():
    productos = requests.get(api_obtener_productos)
    data_productos = productos.json()
    print(data_productos)
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

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

#Actualiza las modificaciones realizadas sin reiniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, port="5000")