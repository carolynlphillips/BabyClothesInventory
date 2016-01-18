from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from mayaclothesapp import app

db = SQLAlchemy(app)


class MayaClothes(db.Model):
    __tablename__ = "mayaclothes"
    id = db.Column('id', db.Integer, primary_key=True)
    category_id = db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
    age_id = db.Column('age_id', db.Integer, db.ForeignKey('age.id'))
    description = db.Column('description', db.Unicode)
    creation_date = db.Column('creation_date', db.Date, default=datetime.utcnow)

    age = db.relationship('Age', foreign_keys=age_id, backref="mayaclothes")
    category = db.relationship('Category', foreign_keys=category_id, backref="mayaclothes")


class Age(db.Model):
    __tablename__ = "age"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)
    value = db.Column('value', db.Integer)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Unicode)

