from crudy.report import summary, write_mongo
from flask import Flask, Markup, render_template
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

    @app.route('/', methods=('GET', 'POST'))
    def index():
        norders, tot, df = summary()
        html = (
            df.style
            .set_properties(**{
                'background-color': 'lightgray',
                'border-color': 'white',
                })
            .render()
        )
        if norders:
            write_mongo(df)

        return render_template('index.html',
                               norders=norders,
                               tot=tot,
                               df=Markup(html))

    from crudy.db import init_app
    init_app(app)

    from crudy import menu, orders
    app.register_blueprint(menu.bp)
    app.register_blueprint(orders.bp)

    return app
