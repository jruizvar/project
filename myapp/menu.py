from flask import Blueprint, redirect, render_template, url_for
from flask_wtf import FlaskForm
from myapp.db import get_db
from wtforms import FloatField, StringField, SubmitField
from wtforms.validators import DataRequired


bp = Blueprint('menu', __name__)


class MyForm(FlaskForm):
    item = StringField('Item', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
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
        db = get_db()
        db.execute(
            'INSERT INTO prices (item, price) VALUES (?, ?)',
            (form.item.data, form.price.data)
        )
        db.commit()
        return redirect(url_for('index'))
    return render_template('create.html', form=form)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    db = get_db()
    it = db.execute(
      'SELECT * FROM prices WHERE id = ?', (id,)
    ).fetchone()
    form = MyForm(data={'item': it['item'], 'price': it['price']})
    if form.validate_on_submit():
        db.execute(
            'UPDATE prices SET item = ?, price = ? WHERE id = ?',
            (form.item.data, form.price.data, id)
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
