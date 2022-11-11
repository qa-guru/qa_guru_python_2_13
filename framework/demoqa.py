import os

import allure
from dotenv import load_dotenv
from requests import Response
import logging
from config import Hosts
from utils.base_session import BaseSession

load_dotenv()


class DemoQA:
    def __init__(self):
        self.demoqa = BaseSession(base_url=os.getenv('api_url'))

    def login(self, user, password, **kwargs) -> Response:
        return self.demoqa.post(
            url='/login',
            params={'Email': user, 'Password': password},
            headers={'content-type': "application/x-www-form-urlencoded; charset=UTF-8"},
            allow_redirects=False
        )

    @allure.step('Добавить товар в карточку')
    def add_cart(self, **kwargs) -> Response:
        cookies = kwargs.pop('cookies', None)
        count = kwargs.pop('count', 1)
        response = None
        for i in range(0, count):
            response = self.demoqa.post('/addproducttocart/catalog/2/1/1', cookies=cookies)
        return response


class DemoQAWithServer:

    def __init__(self):
        self.demoqa = BaseSession(base_url=Hosts().demoqa)

    def login(self, user, password, **kwargs) -> Response:
        return self.demoqa.post(
            url='/login',
            params={'Email': user, 'Password': password},
            headers={'content-type': "application/x-www-form-urlencoded; charset=UTF-8"},
            allow_redirects=False
        )

    def add_cart(self, **kwargs) -> Response:
        cookies = kwargs.pop('cookies', None)
        count = kwargs.pop('count', 1)
        response = None
        for i in range(0, count):
            response = self.demoqa.post('/addproducttocart/catalog/2/1/1', cookies=cookies)
        return response