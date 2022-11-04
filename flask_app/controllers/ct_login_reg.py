from flask_app import app
from flask_app.__init__ import bcrypt
from flask import render_template, redirect, request, session, flash

from flask_app.models.md_user import User

@app.route('/')
def p_home():
    return redirect ('/login')

@app.route('/login')
def r_login_registration():
    return render_template ('login_registration.html')

@app.route('/login-register', methods=['POST'])
def f_register_user():
    if not User.validate_registration(request.form):
        session['first_name'] = request.form.get('first_name')
        session['last_name'] = request.form.get('last_name')
        session['email'] = request.form.get('email')
        return redirect ('/login')
    data:dict = {
        'email': request.form.get('email')
    }
    user_in_db = User.get_by_email(data)
    if user_in_db:
        session['first_name'] = request.form.get('first_name')
        session['last_name'] = request.form.get('last_name')
        session['email'] = request.form.get('email')
        flash('This email is already associated with an account. Please try logging in with this email or creating an account with a different email.', 'email')
        return redirect ('/login')
    if not user_in_db:
        if session:
            session.clear()
        pw_hash = bcrypt.generate_password_hash(request.form.get('password'))
        data:dict = {
            'first_name' : request.form.get('first_name'),
            'last_name' : request.form.get('last_name'),
            'email' : request.form.get('email'),
            'password' : pw_hash
        }
        session['user_id'] = User.save(data)
        return redirect ('/recipes')

@app.route('/login-login', methods=['POST'])
def f_login():
    if not User.validate_login(request.form):
        session.pop('first_name')
        session.pop('last_name')
        session.pop('email')
        session['login_email'] = request.form.get('login_email')
        return redirect ('/login')
    data:dict = {
        'email' : request.form.get('login_email')
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        session['login_email'] = request.form.get('login_email')
        flash('No user associated with this email. Try using a different email or registering for a new account.', 'login_email')
        return redirect ('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form.get('login_password')):
        session['login_email'] = request.form.get('login_email')
        flash('Incorrect password', 'login_password')
        return redirect ('/')
    session.clear()
    session['user_id'] = user_in_db.id
    return redirect ('/recipes')

@app.route('/logout')
def p_logout():
    session.clear()
    return redirect ('/')