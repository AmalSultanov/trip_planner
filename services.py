from jinja2 import Template
from sqlalchemy.orm import joinedload

from ai.validators import validate_ai_response
from database import get_db
from database.models import Intro, Outro, Tip, Plan, Day, Activity, BudgetTip


def save_response_to_db(response):
    saved_plans = []

    try:
        if not validate_ai_response(response):
            print('AI response validation failed.')
            return

        intro_id = save_intro(response.get('intro'))
        outro_id = save_outro(response.get('outro'))

        plans_ids = []
        for plan in response.get('plans'):
            plan_id = save_plan_to_db(plan.get('title'), intro_id, outro_id)
            plans_ids.append(plan_id)

            for day in plan.get('days'):
                day_id = save_day_to_db(plan_id, day.get('title'))

                for activity in day.get('activities'):
                    save_activity_to_db(day_id, activity.get('day_period'),
                                        activity.get('description'))

        for plan_id in plans_ids:
            for tip in response.get('tips'):
                save_tip(plan_id, tip.get('category'), tip.get('advice'))

            for budget_tip in response.get('budget_tips'):
                save_budget_tip(plan_id, budget_tip.get('title'),
                                budget_tip.get('description'))

            saved_plan = get_plan_from_db(plan_id)
            saved_plans.append(saved_plan)

    except Exception as e:
        print(f'Error saving AI response: {e}')
        return

    return saved_plans


def save_intro(description):
    db = next(get_db())
    intro = Intro(description=description)

    db.add(intro)
    db.commit()
    db.refresh(intro)

    return intro.id


def save_tip(plan_id, category, advice):
    db = next(get_db())
    tip = Tip(plan_id=plan_id, category=category, advice=advice)

    db.add(tip)
    db.commit()


def save_plan_to_db(title, intro_id, outro_id):
    db = next(get_db())
    plan = Plan(title=title, intro_id=intro_id, outro_id=outro_id)

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan.id


def save_day_to_db(plan_id, title):
    db = next(get_db())
    day = Day(plan_id=plan_id, title=title)

    db.add(day)
    db.commit()
    db.refresh(day)

    return day.id


def save_activity_to_db(day_id, day_period, description):
    db = next(get_db())
    activity = Activity(day_id=day_id, day_period=day_period,
                        description=description)

    db.add(activity)
    db.commit()


def save_budget_tip(plan_id, title, description):
    db = next(get_db())
    budget_tip = BudgetTip(plan_id=plan_id, title=title,
                           description=description)

    db.add(budget_tip)
    db.commit()


def save_outro(description):
    db = next(get_db())
    outro = Outro(description=description)

    db.add(outro)
    db.commit()
    db.refresh(outro)

    return outro.id


def get_plan_from_db(plan_id):
    db = next(get_db())

    return db.query(Plan).filter_by(id=plan_id).options(
        joinedload(Plan.days).joinedload(Day.activities),
        joinedload(Plan.tips),
        joinedload(Plan.budget_tips),
        joinedload(Plan.intro),
        joinedload(Plan.outro)
    ).first()


def generate_markdown(plan):
    template = Template("""
# {{ plan.title }}

## Введение
{{ plan.intro.description }}

## Полезные советы
{% for tip in plan.tips %}
- **{{ tip.category }}:** {{ tip.advice }}
{% endfor %}

## План поездки
{% for day in plan.days %}
### День {{ loop.index }}: {{ day.title }}
{% for activity in day.activities %}
- **{{ activity.day_period }}:** {{ activity.description }}
{% endfor %}
{% endfor %}

## Бюджетные советы
{% for budget_tip in plan.budget_tips %}
- **{{ budget_tip.title }}:** {{ budget_tip.description }}
{% endfor %}

## Заключение
{{ plan.outro.description }}
""")

    return template.render(plan=plan)
