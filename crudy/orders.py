from flask import Blueprint, redirect, render_template, url_for
from flask_wtf import FlaskForm
from crudy.db import get_db
from wtforms import SelectField, SubmitField
from wtforms.validators import NumberRange


bp = Blueprint('orders', __name__, url_prefix='/orders')


@bp.route('/')
@bp.route('/<int:id>')
def read(id=None):
    db = get_db()
    if id:
        itens = db.execute(
            'SELECT m.order_id, p.name, p.price '
            'FROM middle AS m, products AS p '
            'WHERE m.order_id = ? AND m.prod_id = p.id', (id,)
        )
        return render_template('orders/view.html', itens=itens, id=id)

    itens = db.execute(
        'SELECT m.order_id, p.name, p.price '
        'FROM middle AS m, products AS p '
        'WHERE m.prod_id = p.id '
        'ORDER BY m.order_id'
    )
    return render_template('orders/view.html', itens=itens)


@bp.route('/create', methods=('GET', 'POST'))
@bp.route('/create/<int:id>', methods=('GET', 'POST'))
def create(id=None):
    db = get_db()
    itens = db.execute(
        'SELECT id, name FROM products'
    ).fetchall()
    choices = [(str(it['id']), it['name']) for it in itens]

    message = 'Amount must be between 1 and 10.'
    validators = [NumberRange(min=1, max=10, message=message)]

    class OrderForm(FlaskForm):
        item = SelectField('Item', choices=choices)
        amount = IntegerField('Amount', validators=validators)
        submit = SubmitField('Submit')

    form = OrderForm()
    if form.validate_on_submit():
        if id:
            for _ in range(form.amount.data):
                db.execute(
                    'INSERT INTO middle VALUES (?, ?)',
                    (id, int(form.item.data))
                )
            db.commit()
            return redirect(url_for('.read'))

        db.execute('INSERT INTO orders DEFAULT VALUES')
        ids = db.execute('SELECT id FROM orders').fetchall()
        order_id = ids[-1]['id']
        for _ in range(form.amount.data):
            db.execute(
                'INSERT INTO middle VALUES (?, ?)',
                (order_id, int(form.item.data))
            )
        db.commit()
        return redirect(url_for('.read'))
    return render_template('orders/create.html', form=form)
