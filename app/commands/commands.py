import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.auth.models import User


def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

    test_user = User(
        email='test@gmail.com',
        password=generate_password_hash(
            'password123', 'sha256'),
        first_name='test_user'
    )
    db.session.add(test_user)
    db.session.commit()


@click.command('init_db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Created database")


@click.command('add-admin')
@with_appcontext
def add_admin_command():
    pass
