import logging
from typing import Any

import markdown
import requests
from jinja2 import Template
from sqlalchemy.orm import joinedload
from weasyprint import HTML
from werkzeug.local import LocalProxy

from ai.validators import validate_ai_response
from config import geonames_username
from database import get_db
from database.models import Intro, Outro, Tip, Plan, Day, Activity, BudgetTip

logger = logging.getLogger(__name__)


def fetch_geonames_data(query: str, max_rows: int) -> dict[str, Any]:
    url = f'http://api.geonames.org/searchJSON?q={query}&featureClass=P&maxRows={max_rows}&username={geonames_username}'

    try:
        response = requests.get(url)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f'GeoNames API request failed: {e}')
        return {}


def fetch_autocomplete_results(query: str) -> list[str]:
    data = fetch_geonames_data(query, max_rows=5)

    return [
        f'{city["name"]}, {city["countryName"]}'
        for city in data.get('geonames', [])
    ]


def fetch_destination_validation(dest: str) -> bool:
    data = fetch_geonames_data(dest, max_rows=1)
    return bool(data.get('geonames'))


def extract_fields(request: LocalProxy) -> tuple[str, str, str, str]:
    destination = request.form['destination']
    travel_days = request.form['travel_days']
    budget = request.form['budget']
    interests = request.form.getlist('interests')
    interests_str = ', '.join(interests) if interests \
        else 'General sightseeing'

    return travel_days, destination, budget, interests_str


def save_response_to_db(response: dict[str, Any]) -> list[Plan] | None:
    saved_plans = []

    try:
        if not validate_ai_response(response):
            logger.error('AI response validation failed.')
            return

        intro_id = save_intro(response.get('intro'))
        outro_id = save_outro(response.get('outro'))
        plans_ids = save_plans_to_db(response.get('plans'), intro_id, outro_id)
        save_tips_and_budget_tips(response, plans_ids)

        for plan_id in plans_ids:
            saved_plan = get_plan_from_db(plan_id)
            saved_plans.append(saved_plan)

    except Exception as e:
        logger.error(f'Error saving AI response: {e}')
        return

    return saved_plans


def save_plans_to_db(
        plans: list[dict[str, Any]],
        intro_id: int,
        outro_id: int
) -> list[int]:
    plans_ids = []

    for plan in plans:
        plan_id = save_plan_to_db(plan.get('title'), intro_id, outro_id)
        plans_ids.append(plan_id)

        for day in plan.get('days'):
            day_id = save_day_to_db(plan_id, day.get('title'))

            for activity in day.get('activities'):
                save_activity_to_db(day_id, activity.get('day_period'),
                                    activity.get('description'))

    return plans_ids


def save_tips_and_budget_tips(
        response: dict[str, Any],
        plans_ids: list[int]
) -> None:
    for plan_id in plans_ids:
        for tip in response.get('tips'):
            save_tip(plan_id, tip.get('category'), tip.get('advice'))

        for budget_tip in response.get('budget_tips'):
            save_budget_tip(plan_id, budget_tip.get('title'),
                            budget_tip.get('description'))


def save_intro(desc: str) -> int:
    db = next(get_db())
    intro = Intro(description=desc)

    db.add(intro)
    db.commit()
    db.refresh(intro)

    return intro.id


def save_tip(plan_id: int, category: str, advice: str) -> None:
    db = next(get_db())
    tip = Tip(plan_id=plan_id, category=category, advice=advice)

    db.add(tip)
    db.commit()


def save_plan_to_db(title: str, intro_id: int, outro_id: int) -> int:
    db = next(get_db())
    plan = Plan(title=title, intro_id=intro_id, outro_id=outro_id)

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan.id


def save_day_to_db(plan_id: int, title: str) -> int:
    db = next(get_db())
    day = Day(plan_id=plan_id, title=title)

    db.add(day)
    db.commit()
    db.refresh(day)

    return day.id


def save_activity_to_db(day_id: int, day_period: str, desc: str) -> None:
    db = next(get_db())
    activity = Activity(day_id=day_id, day_period=day_period, description=desc)

    db.add(activity)
    db.commit()


def save_budget_tip(plan_id: int, title: str, desc: str) -> None:
    db = next(get_db())
    budget_tip = BudgetTip(plan_id=plan_id, title=title, description=desc)

    db.add(budget_tip)
    db.commit()


def save_outro(desc: str) -> int:
    db = next(get_db())
    outro = Outro(description=desc)

    db.add(outro)
    db.commit()
    db.refresh(outro)

    return outro.id


def get_plan_from_db(plan_id: int) -> Plan:
    db = next(get_db())

    plan = db.query(Plan).filter_by(id=plan_id).options(
        joinedload(Plan.days).joinedload(Day.activities),
        joinedload(Plan.tips),
        joinedload(Plan.budget_tips),
        joinedload(Plan.intro),
        joinedload(Plan.outro)
    ).first()

    if plan:
        for day in plan.days:
            day.activities.sort(key=lambda activity: activity.id)

    return plan


def generate_pdf(plan: Plan) -> bytes:
    plan_md = generate_markdown(plan)
    plan_html = markdown.markdown(plan_md)

    return HTML(string=plan_html).write_pdf()


def generate_markdown(plan: Plan) -> str:
    template = Template("""
# {{ plan.title }}

## Intro
{{ plan.intro.description }}

## Travel Tips
{% for tip in plan.tips %}
- **{{ tip.category }}:** {{ tip.advice }}
{% endfor %}

## Plans
{% for day in plan.days %}
### Day {{ loop.index }}: {{ day.title }}
{% for activity in day.activities %}
- **{{ activity.day_period }}:** {{ activity.description }}
{% endfor %}
{% endfor %}

## Budget Tips
{% for budget_tip in plan.budget_tips %}
- **{{ budget_tip.title }}:** {{ budget_tip.description }}
{% endfor %}

## Outro
{{ plan.outro.description }}
""")

    return template.render(plan=plan)
