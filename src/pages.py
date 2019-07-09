# -*- coding: utf-8 -*-

import sys
import time

import pytest
from selene import browser
from selene.support import by
from selene.support.conditions import be
from selene.support.jquery_style_selectors import s, ss
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selene.browser import set_driver

from src.common import check_checkbox_leave_the_existence_of_sessions, switch_to_frame
from src.sections import GeneralMenuSection, ConfiguratorMenuSection, ConfiguratorPackageSection, \
    ConfiguratorTabsOfConnectedServicesSection


class MainPage(GeneralMenuSection):

    def __init__(self):
        self.ls_input = s(by.xpath('//*[contains(@id, "buag_lic_acc_num")]'))
        self.search_btn = s(by.xpath('//*[contains(@id, "thtmlb_grid_17")]//a[contains(@onclick, "Search:SEARCH")]'))
        self.confirm_btn = s(by.xpath('//*[contains(@onclick, "CONFIRM:CONFIRM")]'))
        self.create_btn = s(by.xpath('//a[contains(@id, "CREATE")]'))
        self.check_that_page_check_connecttivity_load = s(by.xpath('//*[contains(@id, "T_AddressTab")]'))
        self.crm_id_input = s(by.xpath('//*[contains(@id, "search_struct.partner")]'))
        super().__init__()

    def input_ls(self, client):
        switch_to_frame("WorkAreaFrame1")
        if isinstance(client, str):
            ls = client
        else:
            ls = client.ls
        self.ls_input.set(ls)

    def input_crm_id(self, crm_id):
        switch_to_frame("WorkAreaFrame1")
        self.crm_id_input.set(crm_id)

    def click_search(self):
        switch_to_frame("WorkAreaFrame1")
        self.search_btn.click()
        return CustomerPage()

    def click_creat(self):
        switch_to_frame('WorkAreaFrame1')
        self.create_btn.click()
        self.check_that_page_check_connecttivity_load.should(be.visible)
        return CheckConnecttivityPage()

    def open(self, website):
        browser.open_url(website)
        return ChooseRolePage()