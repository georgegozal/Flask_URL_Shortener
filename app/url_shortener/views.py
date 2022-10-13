from flask import Blueprint, render_template, request, flash, redirect, jsonify
from flask_login import current_user
from app.extensions import db
from app.config import filter_database, get_changed_url
from app.api.models import UrlShort
from app.auth.models import User


url_short = Blueprint('url_short', __name__, template_folder='templates/url_shortener')


# add shortened url
@url_short.route('/', methods=['POST', 'GET'])
def home():
    url_shortened = ''

    if request.method == "POST":
        url_original = request.form['url_original']
        db_query = UrlShort.query.filter_by(url_original=url_original).first()
        if db_query:
            flash('Url already exists', category='error')
            url_shortened = UrlShort.query.order_by(UrlShort.id.desc()).first()
        else:
            try:
                get_user_info = User.query.filter_by(id=current_user.id).first()
                # if user is PRO
                if get_user_info.pro_user == 'True':
                    # get custom sufix from user
                    url_sufix = request.form['custom_sufix']
                    db_query = UrlShort.query.all()
                    if db_query:
                        for url in db_query:
                            while True:
                                # if user custom sufix is not same as url_sufix from database,take it
                                if url.url_shortened.split('/')[-1] != url_sufix:
                                    url_shortened = str(request.url) + 'picourl/' + url_sufix
                                    break
                                else:
                                    flash('Sufix already exists in database, try another', category='error')
                    add_to_database = UrlShort(
                        url_original=url_original,
                        url_shortened=url_shortened,
                        user_id=current_user.id
                    )
                # if user is not PRO
                else:
                    # get random sufix
                    url_shortened = get_changed_url(UrlShort, request)
                    # add new urls in database model
                    add_to_database = UrlShort(
                        url_original=url_original,
                        url_shortened=url_shortened,
                        user_id=current_user.id
                    )
            except AttributeError:
                url_shortened = get_changed_url(UrlShort, request)
                add_to_database = UrlShort(
                    url_original=url_original,
                    url_shortened=url_shortened
                )
            db.session.add(add_to_database)
            db.session.commit()
            url_shortened = UrlShort.query.order_by(UrlShort.id.desc()).first()

    return render_template('home.html', new_url=url_shortened, user=current_user)


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


@url_short.route('/urls', methods=['GET'])
def get_public_urls():

    urls = UrlShort.query.filter_by(user=None).all()
    urls_list = []
    for url in urls:
        u = {
            "id": url.id,
            "url_original": url.url_original,
            "url_shortened": url.url_shortened,
        }
        urls_list.append(u)
    return jsonify(urls_list)


@url_short.route('/<name>/urls', methods=['GET'])
def get_user_urls(name):

    try:
        user = User.query.filter_by(first_name=name).first()
    except Exception as e:
        print(e)
        user = None

    if user:
        if current_user.first_name == user.first_name:
            urls = UrlShort.query.filter_by(user_id=current_user.id).all()
            urls_list = []
            for url in urls:
                u = {
                    "id": url.id,
                    "url_original": url.url_original,
                    "url_shortened": url.url_shortened,
                }

                urls_list.append(u)
            return jsonify(urls_list)
        else:
            flash(f'You can`t see {user.first_name}`s urls', category='error')

    return render_template('404.html')
