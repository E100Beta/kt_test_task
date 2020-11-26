#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging

from aiohttp import web

from btc_api.db import init_db, cleanup_db
from btc_api.utils import get_config
from .routes import init_routes


async def db_engine(app):
    app['db'] = await init_db(app['config']['db_url'])
    yield  # wait for server to finish
    await cleanup_db(app['db'])


def init_app():
    app = web.Application()

    app['config'] = get_config()

    app.cleanup_ctx.append(db_engine)

    init_routes(app)

    return app


logging.basicConfig(level=logging.INFO)
app = init_app()


if __name__ == '__main__':
    host = os.environ.get('HOST', 'localhost')
    port = os.environ.get('PORT', '8080')
    web.run_app(app, host, port)
