import os

from flask import Flask
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'crudy.sqlite'),
    )
    bootstrap = Bootstrap(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from crudy.db import init_app
    init_app(app)

    from crudy.main import bp
    app.register_blueprint(bp)
    app.add_url_rule('/', endpoint='index')

    return app
