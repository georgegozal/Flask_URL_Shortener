from email.policy import default
from config import db 
# from sqlalchemy.sql import func
from datetime import datetime as d, timedelta as t

class UrlShort(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    url_original = db.Column(db.String(250))
    url_shortened = db.Column(db.String(25))
    date = db.Column(
        db.DateTime(timezone=True),
        default=d.now() + t(30)
    )
    used = db.Column(db.Integer,default=0)
    pro_user = db.Column(db.Boolean,default=False)
