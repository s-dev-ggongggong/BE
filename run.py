import os,sys
import click
from flask.cli import FlaskGroup
from flask_migrate import Migrate

# Add the current directory to sys.path
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, current_dir)

from __init__ import create_app, init_db
from extensions import db

def create_app_wrapper():
    return create_app()


@click.group(cls=FlaskGroup, create_app=create_app_wrapper)
def cli():
    pass

@cli.command('init_db')
def init_db_command():
    app= create_app()
    init_db(app)
    click.echo("Intialized the db")

@cli.command('dev')
@click.option('--port', default=8000, help='Port to run the server on')
def dev_cmd(port):
    click.echo(f"Running on port {port}")
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    click.echo(f"To run the server, use: flask run --port {port}")

if __name__ == '__main__':
    
    cli()