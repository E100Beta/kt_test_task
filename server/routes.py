import aiohttp
from aiohttp import web

from btc_api.utils import fetch_price, extract_price
from btc_api.db import add_price, get_prices, get_last_price
from .utils import prepare_records

routes = web.RouteTableDef()


@routes.get('/test')
async def test(request):
    return web.Response(text="Hello World!")


@routes.get('/api/prices')
async def show_prices(request):
    prices = await get_prices(request.app['db'])
    response = prepare_records(prices)
    return web.json_response(response)


@routes.get('/api/prices/latest')
async def show_price(request):
    prices = await get_last_price(request.app['db'])
    response = prepare_records(prices)
    return web.json_response(response)


@routes.get('/api/prices/now')
async def update_prices(request):
    async with aiohttp.ClientSession() as session:
        api_conf = request.app['config']['api']
        data = await fetch_price(
                session,
                api_conf['url'],
                api_conf['params'],
                api_conf['headers']
        )
        price = extract_price(data)
        await add_price(request.app['db'], price)
    return await show_prices(request)


def init_routes(app):
    app.add_routes(routes)
