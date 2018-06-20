from crudy.db import get_db
from pymongo import MongoClient

import pandas as pd
import pymongo


def summary():
    """ Calculate the number of orders (no),
        the total revenue (tot),
        and the denormalized dataframe (df).
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

    norders = df.shape[0]
    tot = df['Total'].sum()
    return norders, tot, df


def write_mongo(df):
    client = MongoClient()
    db = client.crudy_database
    collection = db.crudy_collection
    db.invoices.insert_many(df.to_dict(orient='records'))
