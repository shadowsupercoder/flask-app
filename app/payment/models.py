import datetime

from sqlalchemy_utils.types.choice import ChoiceType

from app.database import db


CURRENCY_CHOICE = [
    ('usd', 'USD'),
    ('eur', 'EUR'),
    ('rub', 'RUB')
]


class Log(db.Model):
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(precision='8', decimal_return_scale='2'))
    currency = db.Column(ChoiceType(CURRENCY_CHOICE))
    description = db.Column(db.String(4096))
    created = db.Column(db.DateTime, default=datetime.datetime.now)

    def __str__(self):
        return self.id


# TODO - create an event after delete
