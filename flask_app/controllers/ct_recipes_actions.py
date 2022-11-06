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

@app.route('/recipes/create/new')
def p_create_new_recipe():
    if not session.get('user_id'):
        return redirect('/')
    if session.get('user_id'):
        if session.get('name'):
            session.pop('name')
        if session.get('description'):
            session.pop('description')
        if session.get('instructions'):
            session.pop('instructions')
        if session.get('date_cooked'):
            session.pop('date_cooked')
        if session.get('under'):
            session.pop('under')
        return redirect ('/recipes/create')

@app.route('/recipes/create-add', methods=['POST'])
def f_create_recipe():
    if not md_recipe.Recipe.validate_recipe(request.form):
        session['name'] = request.form.get('name')
        session['description'] = request.form.get('description')
        session['instructions'] = request.form.get('instructions')
        session['date_cooked'] = request.form.get('date_cooked')
        session['under'] = request.form.get('under')
        return redirect ('/recipes/create')
    md_recipe.Recipe.create_recipe(request.form)
    return redirect ('/recipes')

@app.route('/recipes/view/<int:recipe_id>')
def r_view_recipe(recipe_id):
    if not session.get('user_id'):
        return redirect('/')
    if session.get('user_id'):
        recipe_data = {
            'recipe_id' : recipe_id
        }
        user_data = {
            'user_id' : session.get('user_id')
        }
        return render_template ('view_recipe.html', recipe = md_recipe.Recipe.get_one_recipe_with_creator(recipe_data), user = md_user.User.get_by_user_id(user_data))

@app.route('/recipes/edit/<int:recipe_id>')
def r_edit_recipe(recipe_id):
    if not session.get('user_id'):
        return redirect('/')
    if session.get('user_id'):
        recipe_data = {
            'recipe_id' : recipe_id
        }
        user_data = {
            'user_id' : session.get('user_id')
        }
        recipe = md_recipe.Recipe.get_one_recipe_with_creator(recipe_data)
        if session.get('user_id') != recipe.creator.id:
            return redirect('/recipes')
        return render_template ('edit_recipe.html', recipe = md_recipe.Recipe.get_one_recipe_with_creator(recipe_data), user = md_user.User.get_by_user_id(user_data))

@app.route('/recipes/edit-submit', methods=['POST'])
def f_edit_recipe():
    if not md_recipe.Recipe.validate_recipe(request.form):
        recipe_id = request.form.get('recipe_id')
        return redirect (f'/recipes/edit/{recipe_id}')
    md_recipe.Recipe.edit_recipe(request.form)
    return redirect ('/recipes')

@app.route('/recipes/destroy/<int:recipe_id>')
def p_destroy_recipe(recipe_id):
    if not session.get('user_id'):
        return redirect('/')
    if session.get('user_id'):
        recipe_data = {
            'recipe_id' : recipe_id
        }
        recipe = md_recipe.Recipe.get_one_recipe_with_creator(recipe_data)
        if session.get('user_id') != recipe.creator.id:
            return redirect ('/recipes')
    md_recipe.Recipe.destroy_recipe(recipe_data)
    return redirect('/recipes')
        