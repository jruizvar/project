from flask import Blueprint, redirect, render_template, url_for
from flask_wtf import FlaskForm
from myapp.db import get_db
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired


bp = Blueprint('menu', __name__)


class MyForm(FlaskForm):
    item = StringField('Item', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')


@bp.route('/')
def index():
    db = get_db()
    itens = db.execute(
        'SELECT * FROM prices'
    )
    return render_template('index.html', itens=itens)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    form = MyForm()
    if form.validate_on_submit():
        item = form.item.data
        price = float(form.price.raw_data[0])
        db = get_db()
        db.execute(
            'INSERT INTO prices (item, price)'
            ' VALUES (?, ?)', (item, price)
        )
        db.commit()
        return redirect(url_for('index'))
    return render_template('create.html', form=form)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    it = get_db().execute(
      'SELECT item, price FROM prices'
      ' WHERE id = ?', (id,)
    ).fetchone()
    data = {'item': it['item'],
            'price': it['price']}
    form = MyForm(data=data)
    if form.validate_on_submit():
        item = form.item.data
        price = float(form.price.raw_data[0])
        db = get_db()
        db.execute(
            'UPDATE prices SET item = ?, price = ?'
            ' WHERE id = ?', (item, price, id)
        )
        db.commit()
        return redirect(url_for('index'))
    return render_template('update.html', form=form, id=id)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    db = get_db()
    db.execute(
        'DELETE FROM prices WHERE id = ?', (id,)
    )
    db.commit()
    return redirect(url_for('index'))
