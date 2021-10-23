from sqlalchemy import func

from . import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(110), unique=True, nullable=False)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
