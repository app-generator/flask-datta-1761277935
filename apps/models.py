# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Model(db.Model):

    __tablename__ = 'Model'

    id = db.Column(db.Integer, primary_key=True)

    #__Model_FIELDS__
    name = db.Column(db.String(255),  nullable=True)
    status = db.Column(db.Boolean, nullable=True)
    version = db.Column(db.String(255),  nullable=True)
    time = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Model_FIELDS__END

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)


class Modelstrategy(db.Model):

    __tablename__ = 'Modelstrategy'

    id = db.Column(db.Integer, primary_key=True)

    #__Modelstrategy_FIELDS__
    time = db.Column(db.DateTime, default=db.func.current_timestamp())
    key = db.Column(db.String(255),  nullable=True)
    value = db.Column(db.Integer, nullable=True)
    unit = db.Column(db.String(255),  nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Modelstrategy_FIELDS__END

    def __init__(self, **kwargs):
        super(Modelstrategy, self).__init__(**kwargs)


class Modelalert(db.Model):

    __tablename__ = 'Modelalert'

    id = db.Column(db.Integer, primary_key=True)

    #__Modelalert_FIELDS__
    time = db.Column(db.DateTime, default=db.func.current_timestamp())
    type = db.Column(db.Integer, nullable=True)
    level = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Modelalert_FIELDS__END

    def __init__(self, **kwargs):
        super(Modelalert, self).__init__(**kwargs)



#__MODELS__END
