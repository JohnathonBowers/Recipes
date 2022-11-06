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
    def validate_recipe(recipe:dict):
        is_valid = True
        if len(recipe.get('name')) < 3:
            flash('Recipe name must be at least three characters long.', 'name')
            is_valid = False
        if len(recipe.get('description')) < 3:
            flash('Recipe description must be at least three characters long.', 'description')
            is_valid = False
        if len(recipe.get('instructions')) < 3:
            flash('Recipe instructions must be at least three characters long.', 'instructions')
            is_valid = False
        if len(recipe.get('instructions')) > 1000:
            flash('Recipe instructions must not exceed 1000 characters.', 'instructions')
            is_valid = False
        try: # I referred to Stack Overflow for how to validate a date input
            datetime.datetime.strptime(recipe.get('date_cooked'), '%Y-%m-%d')
        except ValueError:
            flash('Please enter a valid date', 'date_cooked')
            is_valid = False
        if not recipe.get('under'):
            flash('Please indicate whether this recipe can be prepared in under 30 minutes.', 'under')
            is_valid = False
        return is_valid

    @classmethod
    def create_recipe(cls, data:dict):
        query = 'INSERT INTO recipes (name, description, instructions, date_cooked, under, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under)s, %(user_id)s);'
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def get_all_recipes_with_creator(cls):
        query = 'SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id ORDER BY recipes.name ASC;'
        results = connectToMySQL('recipes_schema').query_db(query)
        all_recipes:list[cls] = []
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
    
    @classmethod
    def get_one_recipe_with_creator(cls, data):
        query = 'SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(recipe_id)s;'
        result:dict = connectToMySQL('recipes_schema').query_db(query, data)
        recipe = cls(result[0])
        recipe_author_info = {
            'id' : result[0].get('users.id'),
            'first_name' : result[0].get('first_name'),
            'last_name' : result[0].get('last_name'),
            'email' : result[0].get('email'),
            'password' : result[0].get('password'),
            'created_at' : result[0].get('created_at'),
            'updated_at' : result[0].get('updated_at'),
        }
        author = md_user.User(recipe_author_info)
        recipe.creator = author
        return recipe

    @classmethod
    def edit_recipe(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_cooked = %(date_cooked)s, under = %(under)s WHERE id = %(recipe_id)s'
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def destroy_recipe(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(recipe_id)s'
        return connectToMySQL('recipes_schema').query_db(query, data)