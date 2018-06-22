from crudy.report import summary
from flask import (Flask, flash, Markup, redirect,
                   render_template, session, url_for)
from flask_bootstrap import Bootstrap
from pymongo import MongoClient

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

    @app.route('/')
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
        session['df'] = df.to_dict(orient='records')

        return render_template('index.html',
                               norders=norders,
                               tot=tot,
                               df=Markup(html))

    @app.route('/save', methods=('POST',))
    def save():
        db = MongoClient().crudy_database
        collection = db.crudy_collection
        db.invoices.insert_many(session.pop('df'))
        flash('Your data was successfully saved.')
        return redirect(url_for('index'))

    from crudy.db import init_app
    init_app(app)

    from crudy import menu, orders
    app.register_blueprint(menu.bp)
    app.register_blueprint(orders.bp)

    return app
