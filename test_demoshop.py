import logging
import os
from time import sleep

import requests
from allure_commons._allure import step
from selene import have
from selene.support.shared import browser
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from framework.demoqa import DemoQA

load_dotenv()

LOGIN = os.getenv('user_login')
PASSWORD = os.getenv('user_password')
API_URL = os.getenv('api_url')
WEB_URL = os.getenv('web_url')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="105.0.5195").install()))
# browser.config.driver = driver
browser.config.base_url = WEB_URL


def test_login():
    """Successful authorization to some demowebshop (UI)"""
    with step("Open login page"):
        browser.open("/login")

    with step("Fill login form"):
        browser.element("#Email").send_keys(LOGIN)
        browser.element("#Password").send_keys(PASSWORD).press_enter()

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_through_api(demoqa_authorized_user):
    """Successful authorization to some demowebshop (UI)"""
    response = requests.post(
        url=API_URL + '/login',
        params={'Email': LOGIN, 'Password': PASSWORD},
        headers={'content-type': "application/x-www-form-urlencoded; charset=UTF-8"},
        allow_redirects=False
    )
    authorization_cookie = response.cookies.get('NOPCOMMERCE.AUTH')

    browser.open("/Themes/DefaultClean/Content/images/logo.png")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    browser.open("")

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_through_api_with_cookie_fixture(demoqa_authorized_user):
    """Successful authorization to some demowebshop (UI)"""
    authorization_cookie = demoqa_authorized_user

    browser.open("/Themes/DefaultClean/Content/images/logo.png")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    browser.open("")

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_through_api_with_framework(demoqa_session):
    """Successful authorization to some demowebshop (UI)"""
    auth_cookie_name = 'NOPCOMMERCE.AUTH'

    # response = demoqa_session.post(
    #     url='/login',
    #     params={'Email': LOGIN, 'Password': PASSWORD},
    #     headers={'content-type': "application/x-www-form-urlencoded; charset=UTF-8"},
    #     allow_redirects=False
    # )
    # cookie = response.cookies.get(auth_cookie_name)

    response = DemoQA().login(LOGIN, PASSWORD)
    cookie = response.cookies.get(auth_cookie_name)

    browser.open("/Themes/DefaultClean/Content/images/logo.png")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
    browser.open("")

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_add_one_product_to_cart_authorized(demoqa_authorized_session):
    result = demoqa_authorized_session.post('/addproducttocart/catalog/2/1/1')
    assert result.status_code == 200
    assert result.json()['success'] is True
    assert result.json()['message'] == 'The product has been added to your cart'


def test_add_two_products_to_cart_authorized(demoqa_authorized_session):
    demoqa_authorized_session.post('/addproducttocart/catalog/2/1/1')
    result = demoqa_authorized_session.post('/addproducttocart/catalog/2/1/1')

    assert result.status_code == 200
    assert result.json()['success'] is True
    assert result.json()['message'] == 'The product has been added to your cart'
    assert result.json()['product_count'] == 2


def test_add_product_to_cart_unauthorized(demoqa_session):
    result = demoqa_session.post('/addproducttocart/catalog/2/1/1')

    assert result.status_code == 200
    assert result.json()['success'] is True
    assert result.json()['message'] == 'The product has been added to your cart'