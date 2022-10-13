import os
import string
import random
from datetime import datetime
from .extensions import db


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    PROJECT_NAME = "flask_microblog"
    PROJECT_ROOT = PROJECT_ROOT
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
        or 'sqlite:///' + os.path.join(PROJECT_ROOT, 'db.sqlite')
    SECRET_KEY = 'asd;lkajs-90 as;doaks/A'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def get_random():
    alfabet = string.ascii_lowercase
    nums = "0123456789" * 2
    return ''.join(random.choices(alfabet + nums, k=5))


def get_changed_url(table, request):
    url_sufix = get_random()  # returns random 5 symbol value
    db_query = table.query.all()
    if db_query:
        for url in db_query:
            while True:
                # if url_shortened random 5 symbol is not in database, break
                if url.url_shortened.split('/')[-1] != url_sufix:
                    break
                else:
                    url_sufix = get_random()
            changed_url = str(request.url) + 'picourl/' + url_sufix
        return changed_url


def filter_database(table):
    now = datetime.now()
    db_query = table.query.all()
    for url in db_query:
        if url.date < now:
            db.session.delete(url)
            db.session.commit()
