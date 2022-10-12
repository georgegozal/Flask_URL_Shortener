from flask import Flask, render_template
from app.config import Config
from api.views import api
from url_shortener.views import url_short
from api.models import UrlShort
from auth.models import User
from auth.views import auth
from app.extensions import db, migrate, login_manager



BLUEPRINTS = [api, auth, url_short]
COMMANDS = []


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # register_commands(app)
    register_extensions(app)
    register_blueprints(app)
    # register_admin_panel(app)

    # Invalid URL
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Internal Server Error
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app


def register_extensions(app):

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Flask-Login
    @login_manager.user_loader
    def load_user(id_):
        return User.query.get(id_)

    login_manager.init_app(app)


def register_blueprints(app):

    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)
