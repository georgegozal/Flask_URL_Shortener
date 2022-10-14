from app.extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, index=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    pro_user = db.Column(db.String(4), default=False)
    # pro_user = db.Column(db.Boolean)
    urls = db.relationship('UrlShort', backref='user')
