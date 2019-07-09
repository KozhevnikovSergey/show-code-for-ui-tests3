# -*- coding: utf-8 -*-
import re
import time

import MySQLdb
import pytest
from selene import browser
from selene.support import by
from selene.support.jquery_style_selectors import s
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoAlertPresentException

@with_connection
def take_ls_from_db(conn, table_db, adding_or_shutdown):
    """
    Получение лс из базы данных. Изменение info на врменное значение - делается для того, чтобы при падение теста было
    понятна, что УЗ нерабочая.
    """
    # взятие ЛС с базы данных
    if adding_or_shutdown == 'adding_service':
        take_user = f'SELECT `Personal_account` FROM {table_db} WHERE Info = "Without_iptv"'
    elif adding_or_shutdown == 'shutdown_service':
        take_user = f'SELECT `Personal_account` FROM {table_db} WHERE Info = "With_iptv"'
    data = db_query(conn, take_user)
    if len(data) == 0:
        pytest.fail('В базе данных отсутсвует подходящая учетная запись для теста')
    ls = str(data[0]['Personal_account'])
    print(f'LS: {ls}')
    # запись статуса УЗ в базу данных
    change_info = f'UPDATE {table_db} SET Info = "In work" WHERE `Personal_account` = {ls}'
    db_query(conn, change_info)

    return ls

