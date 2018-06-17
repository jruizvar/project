from flask import Blueprint, redirect, render_template, url_for
from flask_wtf import FlaskForm
from crudy.db import get_db
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


bp = Blueprint('orders', __name__, url_prefix='/orders')


class OrderForm(FlaskForm):
    item = IntegerField('Item', validators=[DataRequired()])
    amount = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')


@bp.route('/')
@bp.route('/<int:id>')
def read(id=None):
    db = get_db()
    if id:
        itens = db.execute(
            'SELECT m.order_id, p.name, p.price FROM middle m, products p '
            'WHERE m.order_id = ? AND m.prod_id = p.id', (id,)
        )
        return render_template('orders/view.html', itens=itens, id=id)

    itens = db.execute(
        'SELECT m.order_id, p.name, p.price FROM middle m, products p '
        'WHERE m.prod_id = p.id '
        'ORDER BY m.order_id'
    )
    return render_template('orders/view.html', itens=itens)


@bp.route('/create', methods=('GET', 'POST'))
@bp.route('/create/<int:id>', methods=('GET', 'POST'))
def create(id=None):
    form = OrderForm()
    if form.validate_on_submit():
        db = get_db()
        if id:
            for _ in range(form.amount.data):
                db.execute(
                    'INSERT INTO middle VALUES (?, ?)',
                    (id, form.item.data)
                )
            db.commit()
            return redirect(url_for('.read'))
        db.execute('INSERT INTO orders DEFAULT VALUES')
        ids = db.execute('SELECT id FROM orders').fetchall()
        order_id = ids[-1]['id']
        for _ in range(form.amount.data):
            db.execute(
                'INSERT INTO middle VALUES (?, ?)',
                (order_id, form.item.data)
            )
        db.commit()
        return redirect(url_for('.read'))
    return render_template('create.html', form=form)
