from flask import (
    Blueprint,
    flash,
    redirect,
    url_for,
    render_template,
    make_response,
    Response
)
from flask_jwt_extended import (
    unset_jwt_cookies
)

from users.forms import RegistrationForm, LoginForm
from users.services import (
    register_user,
    authenticate_user,
    handle_successful_login,
    validate_registration_form
)

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/register', methods=['GET', 'POST'])
def register() -> Response | str:
    form = RegistrationForm()

    if form.validate_on_submit():
        validation_response = validate_registration_form(form)

        if validation_response:
            flash(validation_response, 'danger')
            return redirect(url_for('.register'))

        register_user(form)
        flash('Registration successful! Please log in.', 'success')

        return redirect(url_for('.login'))
    return render_template('register.html', form=form)


@users_bp.route('/login', methods=['GET', 'POST'])
def login() -> Response | str:
    form = LoginForm()

    if form.validate_on_submit():
        user = authenticate_user(form.username.data, form.password.data)

        if user:
            return handle_successful_login(user)

        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)


@users_bp.route('/logout')
def logout() -> Response:
    response = make_response(redirect(url_for('home')))
    unset_jwt_cookies(response)
    flash('You have logged out.', 'info')

    return response
