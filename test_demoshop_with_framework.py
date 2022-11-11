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

from framework.demoqa import DemoQA, DemoQAWithServer
from model.cart import Cart

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


def test_login_through_api():
    """Successful authorization to some demowebshop (UI)"""
    response = DemoQA().login(LOGIN, PASSWORD)
    authorization_cookie = response.cookies.get('NOPCOMMERCE.AUTH')

    browser.open("/Themes/DefaultClean/Content/images/logo.png")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    browser.open("")

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_add_one_product_to_cart_authorized():
    cookie = DemoQA().login(LOGIN, PASSWORD).cookies.get('NOPCOMMERCE.AUTH')

    cart = Cart(DemoQA().add_cart(cookie=cookie))

    assert cart.status_code() == 200
    assert cart.success() is True
    assert cart.message() == 'The product has been added to your cart'


def test_add_two_products_to_cart_authorized():
    count = 2
    cookie = DemoQA().login(LOGIN, PASSWORD).cookies.get('NOPCOMMERCE.AUTH')

    response = DemoQA().add_cart(count=count, cookie=cookie)
    cart = Cart(response)

    assert cart.status_code() == 200
    # assert cart.success() is True
    # assert cart.message() == 'The product has been added to your cart'
    # assert cart.product_count() == count


def test_add_product_to_cart_unauthorized(demoqa_session):
    result = DemoQAWithServer().add_cart()
    cart = Cart(result)

    assert cart.status_code() == 200
    assert cart.success() is True
    assert cart.message() == 'The product has been added to your cart'
