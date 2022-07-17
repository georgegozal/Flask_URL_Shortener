from flask import Flask #, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import LoginManager
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
    from auth.views import auth
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(url_short, url_prefix='/')
    app.register_blueprint(auth,url_prefix='/auth')

    from api.models import UrlShort
    create_database(app)
    migrate = Migrate(app,db)

    from auth.models import User
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not os.path.exists(DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

def get_random():
    alfabet = string.ascii_lowercase
    nums = "0123456789" * 2
    return ''.join(random.choices(alfabet + nums, k =5))

def get_changed_url(table,request):
    url_sufix = get_random() # returns random 5 symbol value
    db_query = table.query.all()
    if db_query:
        for url in db_query:
            while True:
                # if url_shortened random 5 symbol is not in database, break
                if url.url_shortened.split('/')[-1] != url_sufix:
                    break
                else:
                        url_sufix = get_random() 
            changed_url = str(request.url) +'picourl/' + url_sufix
        return changed_url

def filter_database(table):
    now = datetime.now()
    db_query = table.query.all()
    for url in db_query:
        if url.date < now:
            db.session.delete(url)
            db.session.commit()

