from app.extensions import db
from datetime import datetime as d, timedelta as t


class UrlShort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_original = db.Column(db.String(250))
    url_shortened = db.Column(db.String(35))
    date = db.Column(
        db.DateTime(timezone=True),
        default=d.now() + t(30)
    )
    used = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
