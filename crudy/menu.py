from crudy.db import get_db
from flask import Blueprint, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField
from wtforms.validators import DataRequired


bp = Blueprint('menu', __name__, url_prefix='/menu')


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('\u2611')


@bp.route('/')
def read():
    db = get_db()
    query = db.execute(
        'SELECT * FROM products'
    )
    return render_template('menu/view.html', query=query)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    form = ProductForm()
    if form.validate_on_submit():
        db = get_db()
        db.execute(
            'INSERT INTO products (name, price) VALUES (?, ?)',
            (form.name.data, form.price.data)
        )
        db.commit()
        return redirect(url_for('.read'))
    return render_template('menu/create.html', form=form)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    db = get_db()
    q = db.execute(
        'SELECT * FROM products WHERE id = ?', (id,)
    ).fetchone()
    form = ProductForm(data={'name': q['name'], 'price': q['price']})
    if form.validate_on_submit():
        db.execute(
            'UPDATE products SET name = ?, price = ? WHERE id = ?',
            (form.name.data, form.price.data, id)
        )
        db.commit()
        return redirect(url_for('.read'))
    return render_template('menu/update.html', form=form, id=id)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    db = get_db()
    db.execute(
        'DELETE FROM products WHERE id = ?', (id,)
    )
    db.commit()
    return redirect(url_for('.read'))
