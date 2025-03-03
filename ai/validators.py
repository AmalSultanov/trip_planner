import logging
from typing import Any

logger = logging.getLogger(__name__)


def validate_intro_field(response: dict[str, Any]) -> bool:
    intro = response.get('intro')
    valid = isinstance(intro, str) and bool(intro.strip())

    if not valid:
        logger.error(f'Invalid "intro" field: {intro}')

    return valid


def validate_outro_field(response: dict[str, Any]) -> bool:
    outro = response.get('outro')
    valid = isinstance(outro, str) and bool(outro.strip())

    if not valid:
        logger.error(f'Invalid "outro" field: {outro}')

    return valid


def validate_tip(tip: dict[str, int | str]) -> bool:
    valid = (
            isinstance(tip.get('id'), int) and
            isinstance(tip.get('category'), str) and
            isinstance(tip.get('advice'), str)
    )

    if not valid:
        logger.error(f'Invalid tip: {tip}')

    return valid


def validate_tips(response: dict[str, Any]) -> bool:
    tips = response.get('tips')
    valid = isinstance(tips, list) and all(validate_tip(tip) for tip in tips)

    if not valid:
        logger.error(f'Invalid "tips" field: {tips}')

    return valid


def validate_activity(activity: dict[str, int | str]) -> bool:
    valid = (
            isinstance(activity.get('id'), int) and
            isinstance(activity.get('day_period'), str) and
            isinstance(activity.get('description'), str)
    )

    if not valid:
        logger.error(f'Invalid activity: {activity}')

    return valid


def validate_day(day: dict[str, Any]) -> bool:
    valid = (
            isinstance(day.get('id'), int) and
            isinstance(day.get('title'), str) and
            isinstance(day.get('activities'), list) and
            all(validate_activity(activity) for activity in day['activities'])
    )

    if not valid:
        logger.error(f'Invalid day: {day}')

    return valid


def validate_plan(plan: dict[str, Any]) -> bool:
    valid = (
            isinstance(plan.get('id'), int) and
            isinstance(plan.get('title'), str) and
            isinstance(plan.get('days'), list) and
            all(validate_day(day) for day in plan['days'])
    )

    if not valid:
        logger.error(f'Invalid plan: {plan}')

    return valid


def validate_plans(response: dict[str, Any]) -> bool:
    plans = response.get('plans')
    valid = (isinstance(plans, list) and
             all(validate_plan(plan) for plan in plans))

    if not valid:
        logger.error(f'Invalid "plans" field: {plans}')

    return valid


def validate_budget_tip(budget_tip: dict[str, int | str]) -> bool:
    valid = (
            isinstance(budget_tip.get('id'), int) and
            isinstance(budget_tip.get('title'), str) and
            isinstance(budget_tip.get('description'), str)
    )

    if not valid:
        logger.error(f'Invalid budget tip: {budget_tip}')

    return valid


def validate_budget_tips(response: dict[str, Any]) -> bool:
    budget_tips = response.get('budget_tips')
    valid = (isinstance(budget_tips, list) and
             all(validate_budget_tip(budget_tip) for budget_tip in budget_tips))

    if not valid:
        logger.error(f'Invalid "budget_tips" field: {budget_tips}')

    return valid


def validate_ai_response(response: dict[str, Any]) -> bool:
    try:
        valid = (
                validate_intro_field(response) and
                validate_outro_field(response) and
                validate_tips(response) and
                validate_plans(response) and
                validate_budget_tips(response)
        )

        if not valid:
            logger.error(f'AI response validation failed: {response}')
        return valid
    except Exception as e:
        logger.error(f'Error occurred during validation: {e}')
        return False
