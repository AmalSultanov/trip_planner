import pytest

from app import app as flask_app
from database import engine, SessionLocal


@pytest.fixture(scope='session')
def app():
    flask_app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_ECHO': True
    })
    yield flask_app


@pytest.fixture
def app_context(app):
    with app.app_context():
        with app.test_request_context():
            yield


@pytest.fixture(scope='function')
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def user_data():
    return {
        'username': 'test-user1',
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'secure-password',
        'confirm_password': 'secure-password'
    }


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client
