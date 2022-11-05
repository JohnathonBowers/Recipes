from flask_app import app 
from flask_app.controllers import ct_login_reg, ct_recipes_actions, ct_recipes_dashboard

if __name__ == "__main__":
    app.run(debug = True)