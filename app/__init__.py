from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

app.config['SECRET_KEY'] = "this_is_secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
auth = HTTPBasicAuth()
api = Api(app)
db = SQLAlchemy(app)

from app.routes.utils import authenticate
from app.routes import user_controller
from app.routes import todo_controller

api.add_resource(user_controller.UserController, "/user")
api.add_resource(todo_controller.TodoController, "/todo")

