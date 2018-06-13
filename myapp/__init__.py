"""
    Usage:

      - Set environment variables

        export FLASK_APP=myapp
        export FLASK_ENV=development

      - Outside `myapp` directory execute

        flask init-db
        flask run
"""
import os

from flask import Flask
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'myapp.sqlite'),
    )
    bootstrap = Bootstrap(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import menu
    app.register_blueprint(menu.bp)
    app.add_url_rule('/', endpoint='index')

    return app
