from database import get_db
from database.models import User


def create_user(username, name, email, password):
    db = next(get_db())
    user = User(username=username, name=name, email=email)
    user.set_password(password=password)

    db.add(user)
    db.commit()


def get_user_by_username(username):
    db = next(get_db())
    user = db.query(User).filter_by(username=username).first()

    if user:
        return user
    return False


def get_user_by_email(email):
    db = next(get_db())
    user = db.query(User).filter_by(email=email).first()

    if user:
        return user
    return False
