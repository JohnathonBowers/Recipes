from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import md_recipe, md_user

@app.route('/recipes')
def r_show_recipes():
    if not session.get('user_id'):
        return redirect('/')
    if session.get('user_id'):
        data:dict = {
            'user_id' : session.get('user_id')
        }
        return render_template ('recipes.html', user = md_user.User.get_by_user_id(data), recipes = md_recipe.Recipe.get_all_recipes_with_creator())