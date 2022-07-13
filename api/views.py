from flask import Blueprint, render_template, request, flash ,redirect, url_for,jsonify


from config import db, get_random
from .models import UrlShort


api = Blueprint('api',__name__,template_folder='api/templates/api')

@api.route('/')
def home():
    return """
        <ul>Hello to Api
        <li>/api/books GET # get all books </li>
        <li>/api/book/id GET # get single book by id </li>
        
        <li>/api/book POST # add book to database </li>
        <li>/api/book/id PUT # add new book or update by id </li>
        <li>/api/book/id DELETE # delete book by id </li>
        </ul>
        """


# add url to database
@api.route('/api/url',methods=['POST'])
def post():        
    request_data = request.get_json()
    url_original = request_data['url_original']
    # get data from database to check if there is already 
    short_url = UrlShort.query.filter_by(url_original=url_original).first()
    if short_url:
        return  jsonify(
            {
                'url_original' : short_url.url_original, 
                'url_shortened' : short_url.url_shortened
            }
        )

    else:
        url_shortened = get_random()
        url_shortened = str(request.url[:-7]) +'picourl/' +url_shortened
        add_to_database = UrlShort(
            url_original = url_original,
            url_shortened = url_shortened
            )

        db.session.add(add_to_database)
        db.session.commit()

        short_url = UrlShort.query.order_by(UrlShort.id.desc()).first()

        url = {
                "id" : short_url.id,
                'url_original' : short_url.url_original,
                'url_shortened' : short_url.url_shortened
                }
        return jsonify(url), 201

# 
@api.route('/picourl/<short>')
def go_website(short):
    short_url = UrlShort.query.filter_by(url_shortened=request.url).first()
    print('პრიიინტ',short_url.url_original)
    if short_url:
        return redirect(short_url.url_original)
    else:
        return 404, 'No such url'