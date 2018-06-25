from flask import Flask
from flask_bootstrap import Bootstrap

import os


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

    from crudy import main, menu, orders, pool
    app.register_blueprint(main.bp)
    app.register_blueprint(menu.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(pool.bp)

    return app
