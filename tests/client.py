import requests
from requests.cookies import RequestsCookieJar



class Client:

    def __init__(self):
        self._cookies: RequestsCookieJar = RequestsCookieJar()
        self._base_url = 'http://127.0.0.1'

    def update_cookies(self, cookies):
        self._cookies.update(cookies)

    def set_cookies(self, cookies):
        self._cookies = cookies

    @property
    def cookies(self):
        return dict(self._cookies)

    def set_base_url(self, url):
        if url[:-1] == '/':
            url = url[:-1]
        self._base_url = url

    @property
    def base_url(self):
        return self._base_url

    def _join_base_url_and_route_url(self, url):
        if url[0] != '/':
            return f'{self.base_url}/{url}'
        return f'{self.base_url}{url}'

    def get(self, url, params):
        url = self._join_base_url_and_route_url(url)
        response = requests.get(url, params=params,cookies=self.cookies)
        self.update_cookies(response.cookies)
        return response

    def post(self, url, params):
        url = self._join_base_url_and_route_url(url)
        print(url, 'HERE IS URL')
        response = requests.post(url, params=params, cookies=self.cookies)
        self.update_cookies(response.cookies)
        return response

    def delete(self, url , params):
        url = self._join_base_url_and_route_url(url)
        response = requests.delete(url, params=params, cookies=self.cookies)
        self.update_cookies(response.cookies)
        return response