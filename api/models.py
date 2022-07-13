from config import db 
from sqlalchemy.sql import func

class UrlShort(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    url_original = db.Column(db.String(250))
    url_shortened = db.Column(db.String(25))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
