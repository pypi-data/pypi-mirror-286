import urllib.parse

import dacite
import requests

import digistore.model as dm


class DigistoreRoutes:
    def __init__(
        self,
        base_url: str='https://digistore24.com/api/call',
    ):
        self.base_url = base_url

    def _url(self, suffix, args: dict=None):
        url = f'{self.base_url}/{suffix}'

        if args:
            url += f'?{urllib.parse.urlencode(args)}'

        return url

    def list_products(self):
        return self._url('listProducts')

    def list_transactions(self, args: dict):
        return self._url(
            'listTransactions',
            args,
        )


class DigistoreClient:
    def __init__(
        self,
        api_key: str,
        routes: DigistoreRoutes=DigistoreRoutes()
    ):
        self.api_key = api_key
        self.routes = routes

        self.sess = requests.Session()
        sess = self.sess
        sess.headers = {
            'Accept': 'application/json',
            'X-DS-API-KEY': self.api_key,
        }

    def list_products(self):
        res = self.sess.get(self.routes.list_products())

        res.raise_for_status()

        data = res.json()['data']

        return [
            dacite.from_dict(
                data_class=dm.Product,
                data=product_dict,
                config=dacite.Config(
                    cast=[int, float, dm.DigiBool],
                ),
            ) for product_dict in data
        ]
