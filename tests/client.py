import requests


class Client:

    def __init__(self):
        self._cookies = None
        self._base_url = 'http://127.0.0.0'

    def set_cookies(self, cookies):
        self._cookies = cookies

    @property
    def cookies(self):
        return self._cookies

    def set_base_url(self, url):
        if url[:-1] == '/':
            url = url[:-1]
        self._base_url = url

    @property
    def base_url(self):
        return self._base_url

    def _join_base_url_and_route_url(self, url):
        if url[0] != '/':
            url =  f'{self.base_url}/{url}'
        return url

    def get(self, url, params):
        url = self._join_base_url_and_route_url(url)
        response = requests.get(url, params=params,cookies=self.cookies)
        return response

    def post(self, url, params):
        url = self._join_base_url_and_route_url(url)
        response = requests.post(url, params=params, cookies=self.cookies)
        return response

    def delete(self, url , params):
        url = self._join_base_url_and_route_url(url)
        response = requests.delete(url, params=params, cookies=self.cookies)
        return response