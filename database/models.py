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


class Intro(Base):
    __tablename__ = 'intros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Tip(Base):
    __tablename__ = 'tips'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    category = Column(String, nullable=False)
    advice = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


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


class Day(Base):
    __tablename__ = 'days'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # allows Day to access all related Activity records
    activities = relationship('Activity', lazy='subquery')


class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    day_id = Column(Integer, ForeignKey('days.id'), nullable=False)
    day_period = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class BudgetTip(Base):
    __tablename__ = 'budget_tips'

    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Outro(Base):
    __tablename__ = 'outros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
