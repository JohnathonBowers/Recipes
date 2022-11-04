from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.md_recipe import Recipe
from flask_app.models.md_user import User

@app.route('/recipes')
def r_show_recipes():
    if not session.get('user_id'):
        return redirect('/')
    if session.get('user_id'):
        data:dict = {
            'user_id' : session.get('user_id')
        }
        user = User.get_by_user_id(data)
        return render_template ('recipes.html', user = user)