from crypt import methods
from flask import Blueprint, render_template, request, flash ,redirect, url_for,jsonify
from datetime import datetime,timedelta

from config import db, get_random
# from app import app
from api.models import UrlShort

url_short = Blueprint('url_short',__name__,template_folder='templates/url_shortener')

# add shortened url
@url_short.route('/',methods=['POST','GET'])
def home():
    url_shortened = ''
    if request.method == "POST":
        url_original = request.form['url_original']
        db_query = UrlShort.query.filter_by(url_original=url_original).first()
        if db_query:
            flash('Url already exists')
            url_shortened = UrlShort.query.order_by(UrlShort.id.desc()).first()
        else:
            url_shortened = get_random() # returns random 5 symbol value
            db_query = UrlShort.query.all()
            for url in db_query:
                while True:
                    # if url_shortened random 5 symbol is not in database, break
                    if url.url_shortened.split('/')[-1] != url_shortened:
                        break
                    else:
                        url_shortened = get_random() 
            url_short = str(request.url) +'picourl/' + url_shortened
            # add new urls in database model
            add_to_database = UrlShort(
                url_original = url_original,
                url_shortened = url_short
            )

            db.session.add(add_to_database)
            db.session.commit()
            url_shortened = UrlShort.query.order_by(UrlShort.id.desc()).first()

    return render_template('home.html',new_url=url_shortened)


# go to shortened url
@url_short.route('/picourl/<short>')
def go_website(short):
    short_url = UrlShort.query.filter_by(url_shortened=request.url).first()
    if short_url:
        return redirect(short_url.url_original)
    else:
        return 404, 'No such url'