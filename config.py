from flask import Flask #, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime,timedelta
import string
import random
import os

db = SQLAlchemy()
DB_NAME = "shortener.sqlite"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key.'
    projectdir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(projectdir,DB_NAME)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    

    from api.views import api
    from url_shortener.views import url_short
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(url_short, url_prefix='/')

    from api.models import UrlShort
    create_database(app)
    migrate = Migrate(app,db)

    return app

def create_database(app):
    if not os.path.exists(DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

def get_random():
    alfabet = string.ascii_lowercase
    nums = "0123456789" * 2
    return ''.join(random.choices(alfabet + nums, k =5))

def filter_database(table):
    now = datetime.now()
    # t = timedelta(2)
    # time = t +now
    db_query = table.query.all()
    for url in db_query:
        if url.date < now:
            db.session.delete(url)
            db.session.commit()
            
    