import os

from flask import Flask, render_template
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

    @app.route('/')
    def index():
        return render_template('index.html')

    from crudy.db import init_app
    init_app(app)

    from crudy import menu, orders, report
    app.register_blueprint(menu.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(report.bp)

    return app
