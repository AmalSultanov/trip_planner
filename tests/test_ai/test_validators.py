from ai.validators import (
    validate_intro_field,
    validate_outro_field,
    validate_tips,
    validate_plans,
    validate_budget_tips,
    validate_ai_response,
    validate_tip,
    validate_budget_tip,
    validate_plan,
    validate_day,
    validate_activity
)


def test_validate_intro_field():
    assert validate_intro_field({'intro': 'Welcome to your trip!'}) is True
    assert validate_intro_field({'intro': ' '}) is False
    assert validate_intro_field({'intro': None}) is False
    assert validate_intro_field({}) is False


def test_validate_outro_field():
    assert validate_outro_field({'outro': 'Have a great trip!'}) is True
    assert validate_outro_field({'outro': ''}) is False
    assert validate_outro_field({'outro': None}) is False
    assert validate_outro_field({}) is False


def test_validate_tip():
    assert validate_tip({
        'id': 1,
        'category': 'Safety',
        'advice': 'Always keep your passport safe.'}
    ) is True
    assert validate_tip({
        'id': '1',
        'category': 'Safety',
        'advice': 'Keep hydrated.'}
    ) is False
    assert validate_tip({
        'category': 'Safety',
        'advice': 'Keep hydrated.'}
    ) is False


def test_validate_tips():
    assert validate_tips({
        'tips': [
            {
                'id': 1,
                'category': 'Safety',
                'advice': 'Stay aware.'
            }
        ]
    }) is True
    assert validate_tips({'tips': []}) is True
    assert validate_tips({
        'tips': [
            {
                'id': '1',
                'category': 'Safety',
                'advice': 'Be alert.'
            }
        ]
    }) is False
    assert validate_tips({'tips': 'not a list'}) is False


def test_validate_activity():
    assert validate_activity({
        'id': 1,
        'day_period': 'Morning',
        'description': 'Visit the Eiffel Tower'
    }) is True
    assert validate_activity({
        'id': '1',
        'day_period': 'Morning',
        'description': 'Visit museum'
    }) is False
    assert validate_activity({
        'day_period': 'Morning',
        'description': 'Have breakfast'
    }) is False


def test_validate_day():
    valid_day = {
        'id': 1,
        'title': 'Day 1',
        'activities': [
            {
                'id': 1,
                'day_period': 'Morning',
                'description': 'Walk tour'
            }
        ]
    }

    assert validate_day(valid_day) is True
    assert validate_day({
        'id': 1,
        'title': 'Day 1',
        'activities': 'not a list'
    }) is False
    assert validate_day({'id': 1, 'title': 'Day 1'}) is False


def test_validate_plan():
    valid_plan = {
        'id': 1,
        'title': 'Paris Trip',
        'days': [
            {
                'id': 1,
                'title': 'Day 1',
                'activities': [
                    {
                        'id': 1,
                        'day_period': 'Morning',
                        'description': 'Visit park'
                    }
                ]
            }
        ]
    }

    assert validate_plan(valid_plan) is True
    assert validate_plan({'id': 1, 'title': 'Trip'}) is False
    assert validate_plan({
        'id': 1,
        'title': 'Trip',
        'days': 'not a list'
    }) is False


def test_validate_plans():
    valid_plans = {
        'plans': [
            {
                'id': 1,
                'title': 'Trip to Rome',
                'days': [
                    {
                        'id': 1,
                        'title': 'Day 1',
                        'activities': [
                            {
                                'id': 1,
                                'day_period': 'Morning',
                                'description': 'Tour museum'
                            }
                        ]
                    }
                ]
            }
        ]
    }

    assert validate_plans(valid_plans) is True
    assert validate_plans({'plans': []}) is True
    assert validate_plans({'plans': 'invalid'}) is False


def test_validate_budget_tip():
    assert validate_budget_tip({
        'id': 1,
        'title': 'Save Money',
        'description': 'Use discount codes'
    }) is True
    assert validate_budget_tip({
        'id': '1',
        'title': 'Save',
        'description': 'Use cash'
    }) is False
    assert validate_budget_tip({
        'title': 'Save',
        'description': 'Use cash'
    }) is False


def test_validate_budget_tips():
    assert validate_budget_tips({
        'budget_tips': [
            {
                'id': 1,
                'title': 'Save',
                'description': 'Book early'
            }
        ]
    }) is True
    assert validate_budget_tips({'budget_tips': []}) is True
    assert validate_budget_tips({'budget_tips': 'not a list'}) is False


def test_validate_ai_response():
    valid_response = {
        'intro': 'Welcome!',
        'outro': 'Enjoy your trip!',
        'tips': [
            {'id': 1, 'category': 'Safety', 'advice': 'Keep documents safe'}
        ],
        'plans': [
            {
                'id': 1,
                'title': 'Trip to France',
                'days': [
                    {'id': 1,
                     'title': 'Day 1',
                     'activities': [
                         {
                             'id': 1,
                             'day_period': 'Morning',
                             'description': 'Visit Louvre'}
                     ]
                     }
                ]
            }
        ],
        'budget_tips': [
            {
                'id': 1,
                'title': 'Budget Travel',
                'description': 'Book early for discounts'
            }
        ]
    }

    assert validate_ai_response(valid_response) is True
    assert validate_ai_response({
        'intro': '',
        'outro': '',
        'tips': [],
        'plans': [],
        'budget_tips': []}
    ) is False
