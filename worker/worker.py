#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import asyncio
import atexit

import aiohttp

from btc_api.utils import get_config, fetch_price, extract_price
from btc_api.db import init_db, cleanup_db, add_price


async def update_prices(config, interval):
    try:
        db = await init_db(config['db_url'])
        session = aiohttp.ClientSession()
        while True:
            data = await fetch_price(
                session,
                config['api']['url'],
                config['api']['params'],
                config['api']['headers'],
            )
            price = extract_price(data)
            await add_price(db, price)

            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        pass
    finally:
        await session.close()
        await cleanup_db(db)


async def task_cleanup(task):
    task.cancel()
    await task


async def setup_task():
    config = get_config()
    interval = int(os.environ.get('API_INTERVAL', '5')) * 60
    task = asyncio.create_task(update_prices(config, interval))

    # Emulate cleanup behaviour of aiohttp server
    atexit.register(lambda: asyncio.run(task_cleanup(task)))

    await task


if __name__ == '__main__':
    asyncio.run(setup_task())
