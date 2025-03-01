from flask import (
    Blueprint,
    flash,
    redirect,
    url_for,
    render_template,
    make_response
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies
)

from users.forms import RegistrationForm, LoginForm
from users.services import (
    get_user_by_username,
    create_user,
    get_user_by_email
)

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        check_by_username = get_user_by_username(form.username.data)
        check_by_email = get_user_by_email(form.email.data)

        if check_by_username:
            flash('This username already exists, please try another one.',
                  'danger')
            return redirect(url_for('.register'))

        if check_by_email:
            flash('This email is already registered, please try another one.',
                  'danger')
            return redirect(url_for('.register'))

        create_user(form.username.data,
                    form.name.data,
                    form.email.data,
                    form.confirm_password.data)
        flash('Registration successful! Please log in.', 'success')

        return redirect(url_for('.login'))
    return render_template('register.html', form=form)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)

        if user and user.check_password(form.password.data):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            flash('You have successfully logged in!', 'success')

            response = make_response(redirect(url_for('home')))
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)

            return response

        flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)


@users_bp.route('/logout')
def logout():
    response = make_response(redirect(url_for('home')))
    unset_jwt_cookies(response)

    flash('You have logged out.', 'info')

    return response
