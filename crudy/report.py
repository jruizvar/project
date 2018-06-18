from collections import defaultdict
from crudy.db import get_db
from flask import Blueprint, render_template

import pandas as pd

bp = Blueprint('report', __name__, url_prefix='/report')


@bp.route('/')
def read():
    db = get_db().cursor()
    query = db.execute(
        'SELECT m.order_id, p.name, p.price, o.created '
        'FROM middle AS m, products AS p, orders AS o '
        'WHERE m.prod_id = p.id AND m.order_id = o.id'
    )
    cols = [key[0] for key in db.description]
    results = [dict(zip(cols, row)) for row in query]
    dd = defaultdict(list)
    for d in results:
        for k, v in d.items():
            dd[k].append(v)
    df = pd.DataFrame.from_dict(dd)
    df = df.to_html(index=False, justify='center')
    print(df)
    return render_template('report/view.html', df=df)
