import click
from flask.cli import with_appcontext
from app.extensions import db


@click.command('init_db')
@with_appcontext
def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    click.echo("Created database")
