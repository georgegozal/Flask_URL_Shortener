from flask import Blueprint, render_template, request, flash ,redirect, url_for,jsonify
from datetime import datetime,timedelta

from config import db, get_random
from .models import UrlShort


api = Blueprint('api',__name__,template_folder='templates/api')

@api.route('/')
def home():
    return render_template('home.html')

"""
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
    # get data from database to check if it already exists in database
    new_url = UrlShort.query.filter_by(url_original=url_original).first()
    # if value is not none, return shortened url from database
    if new_url:
        return  jsonify(
            {
                'title':'already exists',
                'url_original' : new_url.url_original, 
                'url_shortened' : new_url.url_shortened
            }
        )
    # if url_original is not in database
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
        url_shortened = str(request.url[:-7]) +'picourl/' + url_shortened
        # add new urls in database model
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
    if short_url:
        return redirect(short_url.url_original)
    else:
        return 404, 'No such url'

@api.route('/api/urls',methods=['GET'])
def get_all_urls():
    urls = UrlShort.query.all()
    urls_list = []
    for url in urls:
        u = {
                "id":url.id,
                "url_original":url.url_original,
                "url_shortened":url.url_shortened,

                }
            
        urls_list.append(u)
    return jsonify(urls_list)