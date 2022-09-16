from flask import render_template, redirect, request, session, flash
from Flask_app.model.log import user
from Flask_app import app
from flask_bcrypt import bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def load():
    render_template('main.html')

@app.route('/register', methods = ["POST"])
def register():
    if not user.vaildiate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.check_password_hash(request.form['password'])
    }
    id = register.save()
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/log', methods = ["POST"])
def log():
    register = user.get_mail(request.form)
    if register:
        flash('Invaild Email', 'Login')
        return redirect('/')
    if not bcrypt.check_password_hash(register.password, request.form['password']):
        flash("INVALID PASSWORD", "Login")
    session ['user_id'] = 'user_id'
    return redirect('/dashboard')

@app.route('/dashboard')
def dash():
    if 'register_id' not in session:
        return redirect('/logout')
    data = {
        'id' : session['register_id']
    }
    return render_template("logged.html", user = user.get_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')