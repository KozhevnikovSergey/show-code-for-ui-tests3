# coding: utf8

import pytest

from conftest import check_and_open_main_page
from src.asrz import order_asrz
from src.common import wait_take_and_save_ls, wait_contract_status_in_sap_crm, choose_services
from src.sections import GeneralMenuSection
from src.pages import MainPage, LoginPage, ChooseRolePage, CustomerPage


@pytest.mark.usefixtures('login_in_sap_crm')
class TestCreateClientAndContract(object):
    # какая услуга добавляется
    service = '2 в 1 Легкий Переход 50 (IPTV)'

    #  количество тв приставок
    count_tv = 1  # max 3

    def test_create_client(self, new_client, request, ):
        main_page = MainPage()
        check_connectivity_page = main_page.click_creat()
        check_connectivity_page.input_street(new_client)
        check_connectivity_page.input_house(new_client)
        check_connectivity_page.input_housing(new_client)
        check_connectivity_page.inpute_entrance(new_client)
        check_connectivity_page.click_search()
        check_connectivity_page.choose_first_adress()
        create_customer_page = check_connectivity_page.click_to_connect()
        create_customer_page.input_info_about_client(new_client)
        customer_page = create_customer_page.click_save()
        customer_page.take_and_save_crmid_and_password(request)

    def test_contract_status_in_sap_crm(self, website, admin, request):
        main_page = check_and_open_main_page(website, admin)
        assert wait_contract_status_in_sap_crm(main_page, request.config.cache.get('LS', None))
