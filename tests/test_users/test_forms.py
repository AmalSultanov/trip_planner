from users.forms import RegistrationForm, LoginForm


def test_registration_form_valid(app_context):
    form = RegistrationForm(data={
        'username': 'test-user',
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'secure-password',
        'confirm_password': 'secure-password'
    })
    assert form.validate()


def test_registration_form_missing_fields(app_context):
    form = RegistrationForm(data={})

    assert not form.validate()
    assert 'username' in form.errors
    assert 'email' in form.errors
    assert 'password' in form.errors


def test_registration_form_invalid_email(app_context):
    form = RegistrationForm(data={
        'username': 'test-user',
        'name': 'Test User',
        'email': 'invalid-email',
        'password': 'secure-password',
        'confirm_password': 'secure-password'
    })

    assert not form.validate()
    assert 'email' in form.errors


def test_registration_form_password_mismatch(app_context):
    form = RegistrationForm(data={
        'username': 'test-user',
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'secure-password',
        'confirm_password': 'wrong-password'
    })

    assert not form.validate()
    assert 'confirm_password' in form.errors


def test_login_form_valid(app_context):
    form = LoginForm(data={
        'username': 'test-user',
        'password': 'secure-password'
    })
    assert form.validate()


def test_login_form_missing_fields(app_context):
    form = LoginForm(data={})

    assert not form.validate()
    assert 'username' in form.errors
    assert 'password' in form.errors
