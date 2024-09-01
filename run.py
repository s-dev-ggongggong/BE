import os 
import sys 
import click

curr_dir=os.path.abspath(os.path.dirname(__file__))
sys.path.append(curr_dir)

from __init__ import create_app
from flask.cli import FlaskGroup
from extensions import db
from flask_migrate import Migrate


def create_app_wrapper():
    app= create_app()
    migrate = Migrate(app,db)
    return app


#cli =FlaskGroup(create_app=create_app_wrapper)
app = create_app_wrapper()

# migrate =Migrate(app,db)

@app.cli.command('dev')
@click.option('--port', default=8000, help='Port to run the server on')

def dev_cmd(port):
    click.echo(f"Running on port{port}")
    os.environ['FLASK_ENV']= 'development'
    os.environ['FLASK_DEBUG']= '1'
    click.echo("To run the server, use: flask run --port {port}")
    # app=create_app_wrapper()
    # app.run(debug=True,port=port)
# app.cli.add_command(dev_cmd)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
