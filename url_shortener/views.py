from crypt import methods
from distutils.log import error
from flask import Blueprint, render_template, request, flash ,redirect, url_for,jsonify
from flask_login import login_required, current_user

from config import db, get_random,filter_database
# from app import app
from api.models import UrlShort
from auth.models import User

url_short = Blueprint('url_short',__name__,template_folder='templates/url_shortener')

# add shortened url
@url_short.route('/',methods=['POST','GET'])
def home():
    url_shortened = ''
    if request.method == "POST":
        url_original = request.form['url_original']
        db_query = UrlShort.query.filter_by(url_original=url_original).first()
        if db_query:
            flash('Url already exists',category='error')
            url_shortened = UrlShort.query.order_by(UrlShort.id.desc()).first()
        else:
            get_user_info = User.query.filter_by(id=current_user.id).first()
            if get_user_info.pro_user == 'True':
                url_shortened = request.form['custom_sufix']
                db_query = UrlShort.query.all()
                for url in db_query:
                    while True:
                        if url.url_shortened.split('/')[-1] != url_shortened:
                            break
                        else:
                            flash('Sufix already exists in database, try another',category='error')
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
                url_shortened = url_short,
                user_id = current_user.id
            )

            db.session.add(add_to_database)
            db.session.commit()
            url_shortened = UrlShort.query.order_by(UrlShort.id.desc()).first()

    return render_template('home.html',new_url=url_shortened,user=current_user)


# go to shortened url
@url_short.route('/picourl/<short>')
def go_website(short):
    # check and update database, remove old queries
    filter_database(UrlShort)
    short_url = UrlShort.query.filter_by(url_shortened=request.url).first()
    if short_url:
        short_url.used += 1
        db.session.commit() 
        return redirect(short_url.url_original)
    else:
        return render_template('404.html')

@url_short.route('/urls',methods=['GET'])
def get_all_urls():
    db_query = UrlShort.query.filter_by(user_id=current_user.id).all()
    urls_list = []
    for url in db_query:
        u = {
                "id":url.id,
                "url_original":url.url_original,
                "url_shortened":url.url_shortened,

                }
            
        urls_list.append(u)
    return jsonify(urls_list)