import os


def get_config():
    for key in ['API_KEY', 'DATABASE_URL', 'API_TYPE']:
        if key not in os.environ:
            raise EnvironmentError(f'{key} needs to be set')
    api_key = os.environ.get('API_KEY')
    db_url = os.environ.get('DATABASE_URL')
    api_type = os.environ.get('API_TYPE', 'sandbox')
    api_url = f'https://{api_type}-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    config = {
        'db_url': db_url,
        'api': {
            'url': api_url,
            'headers': {
                'Accept': 'application/json',
                'X-CMC_PRO_API_KEY': api_key,
            },
            'params': {'id': 1},
        },
    }
    return config


async def fetch_price(session, url, params, headers):
    async with session.get(url, params=params, headers=headers) as response:
        return await response.json()


def extract_price(data):
    return data['data']['1']['quote']['USD']['price']
