from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import md_recipe
from flask_app.models import md_user

@app.route('/recipes/create')
def r_create_recipe():
    if not session.get('user_id'):
        return redirect('/')
    if session.get('user_id'):
        data:dict = {
            'user_id' : session.get('user_id')
        }
        return render_template ('create_recipe.html', user = md_user.User.get_by_user_id(data))

@app.route('/recipes/create-add', methods=['POST'])
def f_create_recipe():
    if not md_recipe.Recipe.validate_recipe(request.form):
        print (request.form)
        session['name'] = request.form.get('name')
        session['description'] = request.form.get('description')
        session['instructions'] = request.form.get('instructions')
        session['date_cooked'] = request.form.get('date_cooked')
        session['under'] = request.form.get('under')
        return redirect ('/recipes/create')
    md_recipe.Recipe.create_recipe(request.form)
    return redirect ('/recipes')    
