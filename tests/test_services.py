from unittest.mock import MagicMock

from werkzeug.datastructures import MultiDict

from database.models import Plan
from services import (
    fetch_geonames_data,
    fetch_autocomplete_results,
    fetch_destination_validation,
    extract_fields,
    save_response_to_db,
    generate_pdf,
    generate_markdown
)


def test_fetch_geonames_data(mocker):
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.json.return_value = {
        'geonames': [{'name': 'Paris', 'countryName': 'France'}]}
    result = fetch_geonames_data('Paris', max_rows=1)

    assert result['geonames'][0]['name'] == 'Paris'
    assert result['geonames'][0]['countryName'] == 'France'


def test_fetch_autocomplete_results(mocker):
    mocker.patch('services.fetch_geonames_data', return_value={
        'geonames': [{'name': 'Paris', 'countryName': 'France'}]})
    result = fetch_autocomplete_results('Paris')

    assert result == ['Paris, France']


def test_fetch_destination_validation(mocker):
    mocker.patch('services.fetch_geonames_data',
                 return_value={'geonames': [{'name': 'Paris'}]})
    assert fetch_destination_validation('Paris') is True

    mocker.patch('services.fetch_geonames_data',
                 return_value={'geonames': []})
    assert fetch_destination_validation('UnknownCity') is False


def test_extract_fields():
    request = MagicMock()
    request.form = MultiDict({
        'destination': 'Paris',
        'travel_days': '5',
        'budget': '1000',
        'interests': ['Food', 'Museums']
    })
    travel_days, destination, budget, interests_str = extract_fields(request)

    assert travel_days == '5'
    assert destination == 'Paris'
    assert budget == '1000'
    assert interests_str == 'Food, Museums'


def test_save_response_to_db(mocker):
    mocker.patch('services.validate_ai_response', return_value=True)
    mocker.patch('services.save_intro', return_value=1)
    mocker.patch('services.save_outro', return_value=2)
    mocker.patch('services.save_plans_to_db', return_value=[1])
    mocker.patch('services.save_tips_and_budget_tips')
    mocker.patch('services.get_plan_from_db',
                 return_value=MagicMock(spec=Plan))
    response = {
        'intro': 'Welcome to Paris!',
        'outro': 'Enjoy your trip!',
        'plans': [{'title': 'Paris Tour', 'days': []}],
        'tips': [],
        'budget_tips': []
    }
    result = save_response_to_db(response)

    assert result is not None
    assert len(result) == 1


def test_generate_markdown():
    plan = MagicMock()
    plan.title = 'Test Plan'
    plan.intro.description = 'Intro Text'
    plan.outro.description = 'Outro Text'
    plan.tips = []
    plan.days = []
    plan.budget_tips = []
    markdown_text = generate_markdown(plan)

    assert '# Test Plan' in markdown_text
    assert '## Intro' in markdown_text
    assert 'Intro Text' in markdown_text


def test_generate_pdf(mocker):
    mocker.patch('weasyprint.HTML.write_pdf', return_value=b'PDF_DATA')
    plan = MagicMock()
    pdf_data = generate_pdf(plan)

    assert pdf_data == b'PDF_DATA'
