from unittest.mock import patch, mock_open

from ai.services import (
    generate_ai_response,
    load_prompt_file,
    call_ai_model,
    clean_ai_response,
    str_to_dict
)


@patch(
    'builtins.open',
    new_callable=mock_open,
    read_data='Generate several %s-day travel plans for visiting %s '
              'with a budget of $%s, focusing on %s.'
)
def test_load_prompt_file(mock_file):
    result = load_prompt_file('5', 'Paris', '1000', 'Museums')

    assert result == ('Generate several 5-day travel plans for visiting '
                      'Paris with a budget of $1000, focusing on Museums.')


@patch('ai.services.client.models.generate_content')
def test_call_ai_model(mock_generate):
    mock_generate.return_value.text = 'AI response'
    result = call_ai_model('Test prompt')

    assert result == 'AI response'
    mock_generate.assert_called_once()


def test_clean_ai_response():
    raw_response = '''```json
    {
        "intro": "Welcome to Paris!",
        "plans": [{"title": "Eiffel Tower Visit"}],
        "outro": "Enjoy your stay!"
    }
    ```'''

    cleaned = clean_ai_response(raw_response)

    expected = '''{
        "intro": "Welcome to Paris!",
        "plans": [{"title": "Eiffel Tower Visit"}],
        "outro": "Enjoy your stay!"
    }'''

    assert cleaned == expected.strip()


def test_str_to_dict_valid():
    json_str = '{"intro": "Hello", "plans": []}'
    result = str_to_dict(json_str)

    assert isinstance(result, dict)
    assert result['intro'] == 'Hello'
    assert 'plans' in result


def test_str_to_dict_invalid():
    invalid_json = '{invalid: json}'
    result = str_to_dict(invalid_json)

    assert result == {'error': 'Invalid JSON from AI'}


@patch(
    'builtins.open',
    new_callable=mock_open,
    read_data='Plan a %s-day trip to %s with a budget '
              'of %s USD, focusing on %s.')
@patch('ai.services.call_ai_model', return_value='AI response text')
@patch('ai.services.clean_ai_response', return_value='{"intro": "Welcome"}')
@patch('ai.services.str_to_dict', return_value={'intro': 'Welcome'})
def test_generate_ai_response(
        mock_str_to_dict,
        mock_clean,
        mock_call,
        mock_open
):
    result = generate_ai_response('5', 'Paris', '1000', 'Museums')
    assert result == {'intro': 'Welcome'}
