import os

import pytest
from dotenv import load_dotenv

from utils.base_session import BaseSession


@pytest.fixture(scope='session')
def reqres_session():
    with BaseSession(base_url='https://reqres.in') as session:
        yield session


@pytest.fixture(scope='session')
def cats_session():
    pass


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='session')
def demoqa_session():
    api_url = os.getenv('api_url')
    with BaseSession(base_url=api_url) as session:
        yield session


@pytest.fixture(scope='function')
def demoqa_authorized_session(demoqa_session):
    load_dotenv()
    LOGIN = os.getenv('user_login')
    PASSWORD = os.getenv('user_password')
    api_url = os.getenv('api_url')
    auth_cookie_name = 'NOPCOMMERCE.AUTH'
    with BaseSession(base_url=api_url) as session:
        response = session.post(
            url='/login',
            params={'Email': LOGIN, 'Password': PASSWORD},
            headers={'content-type': "application/x-www-form-urlencoded; charset=UTF-8"},
            allow_redirects=False
        )
        cookie = response.cookies.get(auth_cookie_name)
        session.cookies.set(auth_cookie_name, cookie)
    return session


@pytest.fixture(scope='function')
def demoqa_authorized_user(demoqa_session):
    load_dotenv()
    LOGIN = os.getenv('user_login')
    PASSWORD = os.getenv('user_password')
    api_url = os.getenv('api_url')
    auth_cookie_name = 'NOPCOMMERCE.AUTH'
    response = demoqa_session.post(
            url='/login',
            params={'Email': LOGIN, 'Password': PASSWORD},
            headers={'content-type': "application/x-www-form-urlencoded; charset=UTF-8"},
            allow_redirects=False
        )
    cookie = response.cookies.get(auth_cookie_name)
    return cookie