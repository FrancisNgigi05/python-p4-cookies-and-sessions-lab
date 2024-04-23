#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    # Where all the db data will be stored
    data  = []
    # Getting all the articles in the db
    for article in Article.query.all():
        # Transform the each db data to a dict
        article_dict = article.to_dict()
        # Appending the db data
        data.append(article_dict)
        # Converting the dict to json format
        response = make_response(jsonify(data),  200)
    # Getting all of the response needed
    return response

@app.route('/articles/<int:id>')
def show_article(id):
    """Start by acknowledging that there is a a key page_views which should have a value during get
    if there is no such key then create the key and set the value to zero"""
    session['page_views'] = session.get("page_views") or 0
    session["page_views"] += 1

    if session["page_views"] > 3:
        # setting the limit of amnt of get requests on the blog site
        response_body = {"message": "Maximum pageview limit reached"}
        # Making the response_body to json data
        response = make_response(jsonify(response_body), 401)

        return response
    
    # If the limit is not reached the user can still view the article
    article = Article.query.filter(Article.id == id).first()
    # Converting the db data to a dict
    article_dict = article.to_dict()
    # Converting the dict to json format
    response  = make_response(jsonify(article_dict), 200)

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)