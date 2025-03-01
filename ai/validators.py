from typing import Any


def validate_intro_field(response: dict[str, Any]) -> bool:
    intro = response.get('intro')

    return isinstance(intro, str) and bool(intro.strip())


def validate_outro_field(response: dict[str, Any]) -> bool:
    outro = response.get('outro')

    return isinstance(outro, str) and bool(outro.strip())


def validate_tip(tip: dict[str, int | str]) -> bool:
    return (
            isinstance(tip.get('id'), int) and
            isinstance(tip.get('category'), str) and
            isinstance(tip.get('advice'), str)
    )


def validate_tips(response: dict[str, Any]) -> bool:
    tips = response.get('tips')

    return isinstance(tips, list) and all(validate_tip(tip) for tip in tips)


def validate_activity(activity: dict[str, int | str]) -> bool:
    return (isinstance(activity.get('id'), int) and
            isinstance(activity.get('day_period'), str) and
            isinstance(activity.get('description'), str))


def validate_day(day: dict[str, Any]) -> bool:
    return (
            isinstance(day.get('id'), int) and
            isinstance(day.get('title'), str) and
            isinstance(day.get('activities'), list) and
            all(validate_activity(activity) for activity in day['activities'])
    )


def validate_plan(plan: dict[str, Any]) -> bool:
    return (
            isinstance(plan.get('id'), int) and
            isinstance(plan.get('title'), str) and
            isinstance(plan.get('days'), list) and
            all(validate_day(day) for day in plan['days'])
    )


def validate_plans(response: dict[str, Any]) -> bool:
    plans = response.get('plans')

    return (isinstance(plans, list) and
            all(validate_plan(plan) for plan in plans))


def validate_budget_tip(budget_tip: dict[str, int | str]) -> bool:
    return (
            isinstance(budget_tip.get('id'), int) and
            isinstance(budget_tip.get('title'), str) and
            isinstance(budget_tip.get('description'), str)
    )


def validate_budget_tips(response: dict[str, Any]) -> bool:
    budget_tips = response.get('budget_tips')

    return (isinstance(budget_tips, list) and
            all(validate_budget_tip(budget_tip) for budget_tip in budget_tips))


def validate_ai_response(response: dict[str, Any]) -> bool:
    try:
        return (
                validate_intro_field(response) and
                validate_outro_field(response) and
                validate_tips(response) and
                validate_plans(response) and
                validate_budget_tips(response)
        )
    except Exception as e:
        print(f'Error occurred during validation: {e}')
        return False
