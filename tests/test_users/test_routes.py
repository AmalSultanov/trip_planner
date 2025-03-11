from flask import url_for


def test_register_user(client, session):
    data = {
        'username': 'test-user2',
        'name': 'Test User',
        'email': 'test1@example.com',
        'password': 'secure-password',
        'confirm_password': 'secure-password'
    }
    response = client.post(url_for('users.register'), data=data,
                           follow_redirects=True)
    session.commit()

    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == '/users/login'


def test_register_user_invalid_data(client):
    response = client.post(url_for('users.register'), data={},
                           follow_redirects=True)

    assert response.status_code == 200


def test_login_user(client, user_data):
    data = {
        'username': 'test-user2',
        'name': 'Test User',
        'email': 'test1@example.com',
        'password': 'secure-password',
        'confirm_password': 'secure-password'
    }
    response = client.post(url_for('users.register'), data=data,
                           follow_redirects=True)

    login_data = {'username': 'test-user2',
                  'password': 'secure-password'}
    response = client.post(url_for('users.login'), data=login_data,
                           follow_redirects=True)

    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == '/'


def test_login_invalid_credentials(client):
    response = client.post(url_for('users.login'),
                           data={'username': 'wrong', 'password': 'wrong'},
                           follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid username or password' in response.data


def test_logout_user(client):
    response = client.get(url_for('users.logout'), follow_redirects=True)

    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == '/'
