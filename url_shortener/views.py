from crypt import methods
from distutils.log import error
from flask import Blueprint, render_template, request, flash ,redirect, url_for,jsonify
from flask_login import login_required, current_user

from config import db, filter_database, get_changed_url
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
            try:
                get_user_info = User.query.filter_by(id=current_user.id).first()
                # if user is PRO
                if get_user_info.pro_user == 'True':
                    # get custom sufix from user
                    url_sufix = request.form['custom_sufix']
                    # print('უსერ სუფიქს',url_sufix)
                    db_query = UrlShort.query.all()
                    # print(db_query,type(db_query),'დბქუერიიი')
                    if db_query:
                        for url in db_query:
                            while True:
                                # if user custom sufix is not same as url_sufix from database,take it
                                if url.url_shortened.split('/')[-1] != url_sufix:
                                    url_shortened = str(request.url) +'picourl/' + url_sufix
                                    print(url_shortened,'ურლ შორთენეეეეეედ')
                                    break
                                else:
                                    flash('Sufix already exists in database, try another',category='error')
                    add_to_database = UrlShort(
                        url_original = url_original,
                        url_shortened = url_shortened,
                        user_id = current_user.id
                    )
                # if user is not PRO
                else: 
                    # get random sufix
                    url_shortened= get_changed_url(UrlShort,request)
                    # add new urls in database model
                    add_to_database = UrlShort(
                        url_original = url_original,
                        url_shortened = url_shortened,
                        user_id = current_user.id
                    )
            except AttributeError:
                url_shortened = get_changed_url(UrlShort,request)
                print(url_shortened,'პრიიინტ')
                add_to_database = UrlShort(
                    url_original = url_original,
                    url_shortened = url_shortened
                )
            print(url_shortened,'ურლ შორთენეეეეეედ')
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
    try:
        db_query = UrlShort.query.filter_by(user_id=current_user.id).all()
    except AttributeError:
        db_query = UrlShort.query.filter_by(user_id=None).all()
    urls_list = []
    for url in db_query:
        u = {
                "id":url.id,
                "url_original":url.url_original,
                "url_shortened":url.url_shortened,

                }
            
        urls_list.append(u)
    return jsonify(urls_list)