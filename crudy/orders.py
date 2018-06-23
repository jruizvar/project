from crudy.db import get_db
from flask import Blueprint, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import NumberRange


bp = Blueprint('orders', __name__, url_prefix='/orders')


@bp.route('/')
def read():
    db = get_db()
    query = db.execute(
        'SELECT m.oid, o.created, '
        'printf("%.2f", SUM(p.price)) AS sum_prices '
        'FROM middle AS m, products AS p, orders AS o '
        'WHERE m.pid = p.id AND m.oid = o.id '
        'GROUP BY m.oid '
        'ORDER BY m.oid'
    )
    return render_template('orders/view.html', query=query)


@bp.route('/<int:oid>')
@bp.route('/<int:oid>/<int:pid>')
def update(oid, pid=None):
    db = get_db()
    if pid:
        query = db.execute(
            'SELECT m.pid, p.name, p.price '
            'FROM middle AS m, products AS p '
            'WHERE m.oid = ? AND m.pid = p.id AND p.id = ?', (oid, pid)
        )
        return render_template('orders/update.html',
                               query=query, oid=oid, pid=pid)

    query = db.execute(
        'SELECT m.pid, p.name, p.price '
        'FROM middle AS m, products AS p '
        'WHERE m.oid = ? AND m.pid = p.id', (oid,)
    )
    return render_template('orders/update.html', query=query, oid=oid)


@bp.route('/create', methods=('GET', 'POST'))
@bp.route('<int:oid>/create', methods=('GET', 'POST'))
def create(oid=None):
    db = get_db()
    query = db.execute(
        'SELECT id, name FROM products'
    ).fetchall()
    choices = [(str(q['id']), q['name']) for q in query]

    message = 'Amount must be between 1 and 100.'
    validators = [NumberRange(min=1, max=100, message=message)]

    class OrderForm(FlaskForm):
        amount = IntegerField('Amount', validators=validators)
        item = SelectField('Item', choices=choices)
        submit = SubmitField('\u2611')

    form = OrderForm(data={'amount': 1})
    if form.validate_on_submit():
        if oid:
            for _ in range(form.amount.data):
                db.execute(
                    'INSERT INTO middle VALUES (?, ?)',
                    (oid, int(form.item.data))
                )
            db.commit()
            return redirect(url_for('orders.update', oid=oid))

        db.execute('INSERT INTO orders DEFAULT VALUES')
        ids = db.execute('SELECT id FROM orders').fetchall()
        oid = ids[-1]['id']
        for _ in range(form.amount.data):
            db.execute(
                'INSERT INTO middle VALUES (?, ?)',
                (oid, int(form.item.data))
            )
        db.commit()
        return redirect(url_for('orders.update', oid=oid))
    return render_template('orders/create.html', form=form)


@bp.route('/<int:oid>/<int:pid>/delete', methods=('POST',))
def delete(oid, pid):
    db = get_db()
    db.execute(
        'DELETE FROM middle '
        'WHERE oid = ? AND pid = ?', (oid, pid)
    )
    db.commit()
    return redirect(url_for('orders.update', oid=oid))
