from unittest.mock import MagicMock

from database.models import User
from users.services import (
    get_user_by_username,
    get_user_by_email,
    validate_registration_form,
    authenticate_user,
    handle_successful_login, create_user
)


def test_get_user_by_username():
    create_user(username='test-user5', name='Test User5',
                email='test5@example.com', password='secure-password')
    user = get_user_by_username('test-user5')

    assert user.username == 'test-user5'


def test_get_user_by_email():
    create_user(username='test-user4', name='Test User4',
                email='test4@example.com', password='secure-password')
    user = get_user_by_email('test4@example.com')

    assert user.username == 'test-user4'


def test_validate_registration_form_existing_username(mocker):
    mocker.patch('users.services.get_user_by_username',
                 return_value=User(username='testuser'))
    form = MagicMock()
    form.username.data = 'testuser'
    form.email.data = 'new@example.com'
    error = validate_registration_form(form)

    assert error == 'This username already exists, please try another one.'


def test_validate_registration_form_existing_email(mocker):
    mocker.patch('users.services.get_user_by_username', return_value=None)
    mocker.patch('users.services.get_user_by_email',
                 return_value=User(email='test@example.com'))
    form = MagicMock()
    form.username.data = 'newuser'
    form.email.data = 'test@example.com'
    error = validate_registration_form(form)

    assert error == 'This email is already registered, please try another one.'


def test_authenticate_user_valid(mocker):
    user_mock = MagicMock()
    user_mock.check_password.return_value = True
    mocker.patch('users.services.get_user_by_username', return_value=user_mock)
    user = authenticate_user('testuser', 'password123')

    assert user is not None
    assert user.check_password.called


def test_authenticate_user_invalid(mocker):
    mocker.patch('users.services.get_user_by_username', return_value=None)
    user = authenticate_user('invaliduser', 'password123')

    assert user is None


def test_handle_successful_login(mocker, client, app):
    user = MagicMock(username='test-user4')

    mocker.patch('users.services.create_access_token',
                 return_value='access123')
    mocker.patch('users.services.create_refresh_token',
                 return_value='refresh123')
    mock_set_access_cookies = mocker.patch('users.services.set_access_cookies')
    mock_set_refresh_cookies = mocker.patch(
        'users.services.set_refresh_cookies')
    response = handle_successful_login(user)

    assert response.status_code == 302
    assert response.location == '/'

    mock_set_access_cookies.assert_called()
    mock_set_refresh_cookies.assert_called()
