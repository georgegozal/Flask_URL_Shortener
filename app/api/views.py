from flask import Blueprint, request, jsonify
from app.extensions import db
from app.config import get_random
from .models import UrlShort


api = Blueprint('api', __name__, template_folder='templates/api')


# add url to database
@api.route('/api/url', methods=['POST'])
def post():
    request_data = request.get_json()
    url_original = request_data['url_original']
    # get data from database to check if it already exists in database
    db_query = UrlShort.query.filter_by(url_original=url_original).first()
    # if value is not none, return shortened url from database
    if db_query:
        return jsonify(
            {
                'title': 'already exists',
                'url_original': db_query.url_original,
                'url_shortened': db_query.url_shortened
            }
        )
    # if url_original is not in database
    else:
        url_sufix = get_random()  # returns random 5 symbol value
        db_query = UrlShort.query.all()
        for url in db_query:
            while True:
                # if url_shortened random 5 symbol is not in database, break
                if url.url_shortened.split('/')[-1] != url_sufix:
                    break
                else:
                    url_sufix = get_random()
        url_short = str(request.url[:-7]) + 'picourl/' + url_sufix
        # add new urls in database model
        add_to_database = UrlShort(
            url_original=url_original,
            url_shortened=url_short
        )

        db.session.add(add_to_database)
        db.session.commit()

        url_shortened = UrlShort.query.order_by(UrlShort.id.desc()).first()

        url = {
            "id": url_shortened.id,
            'url_original': url_shortened.url_original,
            'url_shortened': url_shortened.url_shortened
        }
        return jsonify(url), 201


# get all urls
@api.route('/api/urls', methods=['GET'])
def get_all_urls():
    db_query = UrlShort.query.all()
    urls_list = []
    for url in db_query:
        u = {
            "id": url.id,
            "url_original": url.url_original,
            "url_shortened": url.url_shortened,
        }
        urls_list.append(u)
    return jsonify(urls_list)
