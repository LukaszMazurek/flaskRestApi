from flask_restful import reqparse, marshal_with, fields

from app import Resource, db
from app import auth
from app.models.todo import Todo
from app.models.user import User


class TodoController(Resource):

    __parser = reqparse.RequestParser()
    __resources_fields = dict()

    def __init__(self):
        self.__parser.add_argument('id')
        self.__parser.add_argument('text')
        self.__parser.add_argument('complete')
        self.__resources_fields['id'] = fields.Integer
        self.__resources_fields['text'] = fields.String
        self.__resources_fields['complete'] = fields.Boolean

    @auth.login_required
    def get(self):
        user = User.query.filter_by(name=auth.username()).first()

        todos = [{
            "id": todo.id,
            "text": todo.text,
            "complete": todo.complete} for todo in Todo.query.filter_by(user_id=user.id).all()]

        return todos, 200

    @marshal_with(__resources_fields)
    @auth.login_required
    def post(self):
        args = self.__parser.parse_args()
        user = User.query.filter_by(name=auth.username()).first()

        todo = Todo(
            text=args['text'],
            complete=False,
            user_id=user.id
        )

        db.session.add(todo)
        db.session.commit()

        return todo, 200

    @marshal_with(__resources_fields)
    @auth.login_required
    def put(self):
        args = self.__parser.parse_args()

        todo = Todo.query.filter_by(id=args['id']).first()

        if args['text'] is not None:
            todo.text = args['text']
        if args['complete'] is not None:
            todo.complete = bool(args['complete'])

        db.session.commit()

        return todo, 201

    @marshal_with(__resources_fields)
    @auth.login_required
    def delete(self):
        args = self.__parser.parse_args()

        todo = Todo.query.filter_by(id=args['id']).first()

        db.session.delete(todo)
        db.session.commit()

        return todo, 201

