# coding: utf8

import time

import allure
import pytest

from src.common import re_enter_in_sap, check_id_workplace_page_and_click_if_need, db_query
from src.domain import UserForSapCrm, Client, NewClient
from src.pages import LoginPage, MainPage
from src.sections import GeneralMenuSection
from selenium import webdriver
from selene.browser import set_driver
from selene import browser as browser_selene, config
import MySQLdb
from webdriver_manager.chrome import ChromeDriverManager
import random

config.timeout = 15  # время ожидания поиска элементов через selene


@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    set_driver(driver)
    return driver


@pytest.yield_fixture(scope='session')
def login_in_sap_crm(browser, website, admin):
    login_page = LoginPage.open(website)
    choose_a_role_page = login_page.login_as(admin)
    choose_a_role_page.click_on_head_of_commercial_departament()
    check_id_workplace_page_and_click_if_need()
    yield
    browser_selene.close()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    res = outcome.get_result()
    if res.when == 'call':
        # Для Allure
        allure.attach(
            browser_selene.driver().get_screenshot_as_png(),
            name="Screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            browser_selene.driver().current_url,
            name="Link",
            attachment_type=allure.attachment_type.URI_LIST
        )


def pytest_addoption(parser):
    """Берет информацию с консоли"""
    parser.addoption("--envir", action="store", default="test",
                     help="my option: test or prod")
    parser.addoption("--street", action="store", default="Новинки",
                     help="Улица для подключения услуг")
    parser.addoption("--house", action="store", default="9",
                     help="Дом для подключения услуг")
    parser.addoption("--housing", action="store", default="",
                     help="Корпус дома")
    parser.addoption("--type_service", action="store", default='IPTV_package',
                     help="Тип подключаемой услуги. IPTV, IPTV_package, Internet, CTV_package, CTV, MVNO, "
                          "IPTV_package_MVNO, CTV_package_MVNO")


@pytest.fixture(scope="session")
def envir(request):
    return request.config.getoption("--envir")


@pytest.fixture(scope="session")
def street(request):
    return request.config.getoption("--street")


@pytest.fixture(scope="session")
def house(request):
    return request.config.getoption("--house")


@pytest.fixture(scope="session")
def housing(request):
    return request.config.getoption("--housing")


@pytest.fixture(scope="session")
def type_service(request):
    return request.config.getoption("--type_service")


@pytest.fixture(scope='session')
def new_client(street, house, housing):
    try:
        # Это делается т.к. из Jenkins приходит текст в CP866 формате.
        street = street.encode('CP866').decode("utf-8")
    except UnicodeDecodeError:
        pass
    return NewClient(
        street,
        house,
        housing,
        entrance='1',
        surname='Тест',
        name='Тест',
        floor='563',
        apartament=(random.randint(7000, 9999)),
        phone='+79999999999'
    )
