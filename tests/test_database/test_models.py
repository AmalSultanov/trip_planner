from database.models import (
    User,
    Plan,
    Intro,
    Outro,
    Tip,
    Day,
    Activity,
    BudgetTip
)


def test_user_creation(session):
    session.query(User).filter_by(username='test-user').delete()
    session.commit()

    user = User(username='test-user', email='test@example.com')
    user.set_password('secure-password')
    session.add(user)
    session.commit()

    user_in_db = session.query(User).filter_by(username='test-user').first()
    assert user_in_db is not None


def test_create_plan(session):
    intro = Intro(description='Trip Introduction')
    outro = Outro(description='Trip Outro')
    session.add_all([intro, outro])
    session.flush()

    plan = Plan(title='Paris Trip', intro_id=intro.id, outro_id=outro.id)
    session.add(plan)
    session.commit()

    retrieved_plan = session.query(Plan).filter_by(title='Paris Trip').first()

    assert retrieved_plan is not None
    assert retrieved_plan.intro is not None
    assert retrieved_plan.intro.description == 'Trip Introduction'


def test_add_days_and_activities(session):
    intro = Intro(description='Trip Introduction')
    outro = Outro(description='Trip Outro')
    session.add_all([intro, outro])
    session.flush()

    plan = Plan(title='Paris Trip', intro_id=intro.id, outro_id=outro.id)
    session.add(plan)
    session.flush()

    day = Day(plan_id=plan.id, title='Day 1')
    session.add(day)
    session.flush()

    activity = Activity(day_id=day.id, day_period='Morning',
                        description='Visit Eiffel Tower')
    session.add(activity)
    session.commit()

    retrieved_day = session.query(Day).filter_by(plan_id=plan.id).first()
    retrieved_activity = session.query(Activity).filter_by(
        day_id=day.id).first()

    assert retrieved_day is not None
    assert retrieved_activity is not None
    assert retrieved_activity.description == 'Visit Eiffel Tower'


def test_add_tips_to_plan(session):
    intro = Intro(description='Trip Introduction')
    outro = Outro(description='Trip Outro')
    session.add_all([intro, outro])
    session.flush()

    plan = Plan(title='Paris Trip', intro_id=intro.id, outro_id=outro.id)
    session.add(plan)
    session.flush()

    session.query(Tip).delete()
    session.commit()

    tip = Tip(plan_id=plan.id, category='Safety', advice='Always carry cash.')
    session.add(tip)
    session.commit()
    session.refresh(tip)

    retrieved_tip = session.query(Tip).filter_by(plan_id=plan.id).first()

    assert retrieved_tip is not None
    assert retrieved_tip.category == 'Safety'


def test_budget_tips(session):
    intro = Intro(description='Trip Introduction')
    outro = Outro(description='Trip Outro')
    session.add_all([intro, outro])
    session.flush()

    plan = Plan(title='Paris Trip', intro_id=intro.id, outro_id=outro.id)
    session.add(plan)
    session.flush()

    session.query(BudgetTip).delete()
    session.commit()

    budget_tip = BudgetTip(plan_id=plan.id, title='Save Money',
                           description='Use public transport.')
    session.add(budget_tip)
    session.commit()
    session.refresh(budget_tip)

    retrieved_tip = session.query(BudgetTip).filter_by(plan_id=plan.id).first()

    assert retrieved_tip is not None
    assert retrieved_tip.title == 'Save Money'
