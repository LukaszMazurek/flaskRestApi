from app import auth
from app import db
from app.models.user import User

from werkzeug.security import check_password_hash


@auth.verify_password
def authenticate(name, password):
    user = User.query.filter_by(name=name).first()

    if user is not None:
        return check_password_hash(user.password, password)

    return False
