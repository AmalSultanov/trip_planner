from unittest.mock import patch


def test_home_route(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_autocomplete_no_query(client):
    response = client.get('/autocomplete')

    assert response.status_code == 200
    assert response.json == []


@patch('services.fetch_autocomplete_results', return_value=['Paris'])
def test_autocomplete_with_query(mock_fetch, client):
    response = client.get('/autocomplete?query=Pari')

    assert response.status_code == 200
    assert response.json == ['Paris, France', 'Pauri, India',
                             'Keur Pari, Senegal', 'Pari de Pedras, Brazil',
                             'Pari, Estonia']


@patch('services.fetch_destination_validation', return_value=True)
def test_validate_destination_valid(mock_fetch, client):
    response = client.get('/validate-destination?destination=Paris')

    assert response.status_code == 200
    assert response.json == {'valid': True}


def test_validate_destination_no_input(client):
    response = client.get('/validate-destination')

    assert response.status_code == 200
    assert response.json == {'valid': False}


@patch('ai.services.generate_ai_response')
@patch('services.save_response_to_db')
def test_get_plans(mock_save, mock_ai, client):
    response = client.post('/plans', data={'destination': 'Paris, France',
                                           'travel_days': '1',
                                           'budget': '1000',
                                           'interests': ['Museums']})

    assert response.status_code == 200


@patch('services.get_plan_from_db', return_value=b'PDF Content')
@patch('services.generate_pdf', return_value=b'PDF Content')
def test_download_pdf(mock_pdf, mock_db, client):
    response = client.get('/plans/1/download')

    assert response.status_code == 200
    assert response.mimetype == 'application/pdf'


def test_is_authenticated(client):
    response = client.get('/is-authenticated')
    assert response.status_code == 200
    assert response.json == {'authenticated': False}

    client.set_cookie('access_token_cookie', 'xyz')
    response = client.get('/is-authenticated')

    assert response.json == {'authenticated': True}
