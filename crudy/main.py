from crudy.db import get_db
from flask import (Blueprint, flash, Markup, redirect,
                   render_template, session, url_for)
from pymongo import MongoClient

import pandas as pd


bp = Blueprint('main', __name__)


def summary():
    db = get_db()
    query = """ SELECT m.oid, p.name, o.created, p.price
                FROM prod_order AS m, products AS p, orders AS o
                WHERE m.pid = p.id AND m.oid = o.id
                ORDER BY m.oid
            """
    df = pd.read_sql(query, db).groupby('oid')

    s1 = df['name'].apply(list)
    s2 = df['created'].first()
    s3 = df['price'].sum()

    df = pd.concat([s1, s2, s3], axis=1)
    df.columns = ['Products', 'Created', 'Total']
    df.index.rename('Order ID', inplace=True)

    norders = df.shape[0]
    tot = df['Total'].sum()
    return norders, tot, df


@bp.route('/')
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


@bp.route('/save', methods=('POST',))
def save():
    db = MongoClient().crudy_database
    db.invoices.insert_many(session.pop('df'))
    flash('Your data was successfully saved.')
    return redirect(url_for('main.index'))
