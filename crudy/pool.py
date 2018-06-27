from crudy.db import get_db
from flask import Blueprint, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired
from pymongo import MongoClient

import datetime


bp = Blueprint('pool', __name__, url_prefix='/pool')


@bp.route('/')
def read():
    return render_template('pool/view.html')


@bp.route('/create', methods=('GET', 'POST'))
def create():
    query = get_db().execute(
        'SELECT id FROM orders'
    ).fetchall()
    choices = [(str(q['id']), q['id']) for q in query]

    class ProductForm(FlaskForm):
        order = SelectField('Order number:', choices=choices)
        service = RadioField('Como você se sente em relação ao atendimento?',
                             choices=[('VS', 'Very Satisfied'),
                                      ('S', 'Satisfied'),
                                      ('I', 'Indifferent'),
                                      ('D', 'Dissatisfied')])
        food = RadioField('Como você se sente em relação a comida?',
                          choices=[('VS', 'Very Satisfied'),
                                   ('S', 'Satisfied'),
                                   ('I', 'Indifferent'),
                                   ('D', 'Dissatisfied')])
        mood = RadioField('Como você se sente em relação ao ambiente?',
                          choices=[('VS', 'Very Satisfied'),
                                   ('S', 'Satisfied'),
                                   ('I', 'Indifferent'),
                                   ('D', 'Dissatisfied')])
        courtesy = RadioField('Escolha um aperitivo para sua próxima visita!',
                              choices=[('CW', 'Chicken Wings'),
                                       ('FS', 'Fries'),
                                       ('SL', 'Salad')])
        comment = StringField('Algum comentário adicional?')
        submit = SubmitField('\u2611')

    form = ProductForm()
    if form.validate_on_submit():
        pool_answer = {'order': form.order.data,
                       'service': form.service.data,
                       'food': form.food.data,
                       'mood': form.mood.data,
                       'courtesy': form.courtesy.data,
                       'comment': form.comment.data,
                       'date': datetime.datetime.utcnow()}
        db = MongoClient().crudy_database
        db.pools.insert_one(pool_answer)
        return redirect(url_for('pool.read'))
    return render_template('pool/create.html', form=form)
