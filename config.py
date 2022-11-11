import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Hosts:
    def __init__(self):
        load_dotenv()
        self.env = os.getenv('environment')
        self.demoqa = {
            'local': 'localhost:5555',
            'test': 'http://your_test_env.com',
            'prod': 'https://demowebshop.tricentis.com',
        }[self.env]
        self.reqres = {
            'local': 'localhost:5555',
            'test': 'http://your_test_env.com',
            'prod': 'https://reqres.in',
        }[self.env]
