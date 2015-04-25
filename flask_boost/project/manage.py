# coding: utf-8
import glob2
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from application import create_app
from application.models import db
from application.utils.assets import build

# Used by app debug & livereload
PORT = 5000

app = create_app()
manager = Manager(app)

# db migrate commands
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    """Run app."""
    app.run(port=PORT)


@manager.command
def live():
    """Run livereload server"""
    from livereload import Server
    import formic

    server = Server(app)

    # html
    for filepath in glob2.glob("application/templates/**/*.html"):
        server.watch(filepath)
    # css
    for filepath in glob2.glob("application/static/css/**/*.css"):
        server.watch(filepath)
    # js
    for filepath in glob2.glob("application/static/js/**/*.js"):
        server.watch(filepath)
    # image
    for filepath in glob2.glob("application/static/image/**/*.*"):
        server.watch(filepath)

    server.serve(port=PORT)


@manager.command
def createdb():
    """Create database."""
    db.create_all()


@manager.command
def build_assets():
    build(app)


if __name__ == "__main__":
    manager.run()