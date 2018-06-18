from crudy.db import get_db
from flask import Blueprint, render_template


bp = Blueprint('report', __name__, url_prefix='/report')


@bp.route('/')
def read():
    db = get_db().cursor()
    query = db.execute(
        'SELECT m.order_id, p.name, p.price, o.created '
        'FROM middle AS m, products AS p, orders AS o '
        'WHERE m.prod_id = p.id'
    )
    cols = [key[0] for key in db.description]
    itens = [dict(zip(cols, row)) for row in query]
    for item in itens:
        print(item)
    return render_template('report/view.html')
