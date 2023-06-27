from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    link = db.Column(db.String(300))

class Students(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(256))
    klasse = db.Column(db.String(10))
    questions = db.relationship("Writer")


class Writer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000))
    answer = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    questioner_id = db.Column(db.Integer, db.ForeignKey('students.id'))