from crudy.db import get_db
from flask import Markup

import pandas as pd


def summary():
    db = get_db()
    query = """ SELECT m.oid, p.name, p.price, o.created
                FROM middle AS m, products AS p, orders AS o
                WHERE m.pid = p.id AND m.oid = o.id
                ORDER BY m.oid
            """
    df = pd.read_sql(query, db)

    s1 = df.groupby('oid')['name'].apply(list)
    s2 = df.groupby('oid')['price'].sum()
    s3 = df.groupby('oid')['created'].first()

    df = pd.concat([s1, s2, s3], axis=1)
    df.columns = ['Products', 'Total', 'Created']
    df.index.rename('Order ID', inplace=True)
    df = df.to_html(justify='center')
    return Markup(df)
