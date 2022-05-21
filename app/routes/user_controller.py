from flask_restful import reqparse, marshal_with, fields

from werkzeug.security import generate_password_hash

from app import Resource, db
from app import auth
from app.models.todo import Todo
from app.models.user import User


class UserController(Resource):

    __parser = reqparse.RequestParser()
    __resources_fields = dict()

    def __init__(self):
        self.__parser.add_argument('public_id')
        self.__parser.add_argument('name')
        self.__parser.add_argument('password')
        self.__parser.add_argument('admin')
        self.__parser.add_argument('token')
        self.__resources_fields['name'] = fields.String
        self.__resources_fields['id'] = fields.Integer
        self.__resources_fields['admin'] = fields.Boolean

    @marshal_with(__resources_fields)
    @auth.login_required
    def get(self):
        name = auth.username()
        user = User.query.filter_by(name=name).first()
        return user

    def post(self):
        args = self.__parser.parse_args()

        user = User(
            name=args['name'],
            password=generate_password_hash(args['password']),
            admin=bool(args['admin'])
        )

        db.session.add(user)
        db.session.commit()

        return {'name': args['name']}, 201

    @marshal_with(__resources_fields)
    @auth.login_required
    def put(self):
        args = self.__parser.parse_args()

        user = User.query.filter_by(name=auth.username()).first()

        user.name = args['name']
        user.admin = bool(args['admin'])

        db.session.commit()

        return user
