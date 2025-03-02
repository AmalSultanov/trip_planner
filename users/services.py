from flask import flash, redirect, url_for, make_response, Response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies
)

from database import get_db
from database.models import User
from users.forms import RegistrationForm


def register_user(form: RegistrationForm) -> None:
    create_user(
        form.username.data,
        form.name.data,
        form.email.data,
        form.confirm_password.data
    )


def create_user(username: str, name: str, email: str, password: str) -> None:
    db = next(get_db())
    user = User(username=username, name=name, email=email)
    user.set_password(password=password)

    db.add(user)
    db.commit()


def get_user_by_username(username: str) -> User | None:
    db = next(get_db())
    return db.query(User).filter_by(username=username).first()


def get_user_by_email(email: str) -> User | None:
    db = next(get_db())
    return db.query(User).filter_by(email=email).first()


def validate_registration_form(form: RegistrationForm) -> str | None:
    if get_user_by_username(form.username.data):
        return 'This username already exists, please try another one.'

    if get_user_by_email(form.email.data):
        return 'This email is already registered, please try another one.'

    return None


def authenticate_user(username: str, password: str) -> User | None:
    user = get_user_by_username(username)
    return user if user and user.check_password(password) else None


def handle_successful_login(user: User) -> Response:
    access_token = create_access_token(identity=user.username)
    refresh_token = create_refresh_token(identity=user.username)

    flash('You have successfully logged in!', 'success')

    response = make_response(redirect(url_for('home')))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response
