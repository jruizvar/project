from crudy.db import get_db
from flask import Blueprint, Markup, render_template

import pandas as pd


bp = Blueprint('report', __name__, url_prefix='/report')


@bp.route('/')
def read():
    db = get_db()
    query = """ SELECT m.order_id, p.name, p.price, o.created
                FROM middle AS m, products AS p, orders AS o
                WHERE m.prod_id = p.id AND m.order_id = o.id
                ORDER BY m.order_id
            """
    df = pd.read_sql(query, db)
    df = df.to_html(index=False, justify='center')
    return render_template('report/view.html', df=Markup(df))
