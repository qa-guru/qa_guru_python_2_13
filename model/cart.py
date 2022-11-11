import logging

from requests import Response


class Cart:
    def __init__(self, response: Response):
        self.response = response
        self.json = response.json()

    def status_code(self):
        code = self.response.status_code
        logging.info(f'code: {code}')
        return code

    def message(self):
        return self.json['message']

    def product_count(self):
        return self.json['product_count']

    def success(self):
        return self.json['success']