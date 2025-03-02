from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from app import bcrypt
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode(
            'utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'<User {self.id}: {self.username}>'

    def __str__(self) -> str:
        return f'User {self.id}: {self.username}, {self.email}'


class Intro(Base):
    __tablename__ = 'intros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Intro {self.id}: {self.description[:50]}...>'

    def __str__(self) -> str:
        return f'Intro {self.id}: {self.description[:50]}...'


class Tip(Base):
    __tablename__ = 'tips'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    category = Column(String, nullable=False)
    advice = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Tip {self.id}: {self.category}>'

    def __str__(self) -> str:
        return f'Tip {self.id}: {self.category}'


class Plan(Base):
    __tablename__ = 'plans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    intro_id = Column(Integer, ForeignKey('intros.id'), nullable=False)
    outro_id = Column(Integer, ForeignKey('outros.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    intro = relationship('Intro', lazy='subquery', foreign_keys=[intro_id])
    tips = relationship(Tip, lazy='subquery')
    days = relationship('Day', lazy='subquery')
    budget_tips = relationship('BudgetTip', lazy='subquery')
    outro = relationship('Outro', lazy='subquery', foreign_keys=[outro_id])

    def __repr__(self) -> str:
        return f'<Plan {self.id}: {self.title}>'

    def __str__(self) -> str:
        return f'Plan {self.id}: {self.title}'


class Day(Base):
    __tablename__ = 'days'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # allows Day to access all related Activity records
    activities = relationship('Activity', lazy='subquery')

    def __repr__(self) -> str:
        return f'<Day {self.id}: {self.title}>'

    def __str__(self) -> str:
        return f'Day {self.id}: {self.title}'


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    day_id = Column(Integer, ForeignKey('days.id'), nullable=False)
    day_period = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Activity {self.id}: {self.day_period}>'

    def __str__(self) -> str:
        return f'Activity {self.id}: {self.day_period}'


class BudgetTip(Base):
    __tablename__ = 'budget_tips'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<BudgetTip {self.id}: {self.title}>'

    def __str__(self) -> str:
        return f'BudgetTip {self.id}: {self.title}'


class Outro(Base):
    __tablename__ = 'outros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Outro {self.id}: {self.description[:50]}...>'

    def __str__(self) -> str:
        return f'Outro {self.id}: {self.description[:50]}...'
