from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "30cfc6ce08e46c94afc1ddb27c93dd99"

bcrypt = Bcrypt(app)