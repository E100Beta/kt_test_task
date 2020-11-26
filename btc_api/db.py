import datetime

from databases import Database
import sqlalchemy
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, DateTime, Float,
    select,
)

meta = MetaData()

btc_prices = Table(
    'btc', meta,
    Column('id', Integer, primary_key=True),
    Column('price', Float),
    Column('timestamp', DateTime),
)


def create_tables(db_url):
    engine = sqlalchemy.create_engine(db_url)
    meta.create_all(engine, checkfirst=True)


def drop_tables(db_url):
    engine = sqlalchemy.create_engine(db_url)
    meta.drop_all(engine)


async def init_db(db_url):
    db = Database(db_url)
    await db.connect()
    return db


async def cleanup_db(db):
    await db.disconnect()


async def add_price(db, price):
    async with db.transaction():
        query = btc_prices.insert()
        values = {
            'price': price,
            'timestamp': datetime.datetime.utcnow(),
        }
        await db.execute(query=query, values=values)


async def get_last_price(db):
    query = select([btc_prices]).order_by(btc_prices.c.timestamp.desc())
    return await db.fetch_one(query=query)


async def get_prices(db):
    query = select([btc_prices]).order_by(btc_prices.c.timestamp.desc())
    return await db.fetch_all(query=query)
