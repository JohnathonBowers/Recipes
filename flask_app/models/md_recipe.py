from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import md_user
from flask import flash
import datetime

class Recipe:
    def __init__(self, db_data:dict):
        self.id = db_data.get('id')
        self.name = db_data.get('name')
        self.description = db_data.get('description')
        self.instructions = db_data.get('instructions')
        self.date_cooked = db_data.get('date_cooked')
        self.under = db_data.get('under')
        self.created_at = db_data.get('created_at')
        self.updated_at = db_data.get('updated_at')
        self.user_id = db_data.get('user_id')
        self.creator = None
    
    @staticmethod
    def validate_recipe(recipe:dict)
        is_valid = True
        if len(recipe.get('name')) < 2:
            flash('Recipe name must be two or more characters.', 'name')
            is_valid = False
        if len(recipe.get('description')) < 1:
            flash('Please give a brief description of the recipe.')
            is_valid = False
        if len(recipe.get('instructions')) < 1:
            flash('Please provide recipe instructions.')
            is_valid = False
        if len(recipe.get('instructions')) > 1000:
            flash('Recipe instructions must not exceed 1000 characters.', 'instructions')
            is_valid = False
        if not datetime.datetime.strptime(recipe.get('date_cooked'), '%Y-%m-%d')  # I referenced Stack Overflow for this validation
            flash('Please enter a valid date', 'date_cooked')
            is_valid = False
        if len(recipe.get('under')) < 1:
            flash('Please indicate whether this recipe can be prepared in under 30 minutes.', 'under')
            is_valid = False
        return is_valid

    @classmethod
    def create_recipe(cls, data:dict)
        query = 'INSERT INTO recipes (name, description, instructions, date_cooked, under, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under)s, %(user_id)s);'
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def get_all_recipes_with_creator(cls)
        query = 'SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;'
        results = connectToMySQL('recipes_schema').query_db(query)
        all_recipes:list[objects] = []
        for row in results:
            one_recipe = cls(row)
            one_recipes_author_info = {
                'id' : row.get('users.id'),
                'first_name' : row.get('first_name'),
                'last_name' : row.get('last_name'),
                'email' : row.get('email'),
                'password' : row.get('password'),
                'created_at' : row.get('users.created_at'),
                'updated_at' : row.get('users.updated_at')
            }
            author = md_user.User(one_recipes_author_info)
            one_recipe.creator = author
            all_recipes.append(one_recipe)
        return all_recipes