from crudy.db import get_db
from flask import Markup

import pandas as pd


def summary():
    """ Calculate the number of orders (no),
        the total revenue (tot),
        and the denormalized database (df)
    """
    db = get_db()
    query = """ SELECT m.oid, p.name, o.created, p.price
                FROM middle AS m, products AS p, orders AS o
                WHERE m.pid = p.id AND m.oid = o.id
                ORDER BY m.oid
            """
    df = pd.read_sql(query, db).groupby('oid')

    s1 = df['name'].apply(list)
    s2 = df['created'].first()
    s3 = df['price'].sum()

    df = pd.concat([s1, s2, s3], axis=1)
    df.columns = ['Products', 'Created', 'Total']
    df.index.rename('Order ID', inplace=True)

    no = df.shape[0]
    tot = df['Total'].sum()

    html = (
        df.style
        .set_properties(**{
            'background-color': 'lightgray',
            'border-color': 'white',
            })
        .render()
    )

    return no, tot, Markup(html)
