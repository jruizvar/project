from crudy.db import get_db
from flask import Blueprint, Markup, render_template

import pandas as pd


bp = Blueprint('report', __name__, url_prefix='/report')


@bp.route('/')
def read():
    db = get_db()
    query = """ SELECT m.oid, p.name, p.price, o.created
                FROM middle AS m, products AS p, orders AS o
                WHERE m.pid = p.id AND m.oid = o.id
                ORDER BY m.oid
            """
    df = pd.read_sql(query, db)
    df = df.to_html(index=False, justify='center')
    return render_template('report/view.html', df=Markup(df))
