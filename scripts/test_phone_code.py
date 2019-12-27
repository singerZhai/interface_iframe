# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 18:33
# @Author  : zhaihuide@jiandan100.cn
# @Site    : 
# @File    : test_phone_code.py
# @Software: PyCharm
from util.tools import *
import requests


class TestPhoneCode(object):

    main_url = 'http://127.0.0.1:5000'
    get_code_url = main_url + '/getCode'
    assert_code_url = main_url + '/assertCode'

    def test_01_get_phone_code(self):
        rsp = requests.get(self.get_code_url)
        write_rsp('getCode', rsp.text, skip_path_list=['["phone_code"]'])

    def test_02_assert_code(self):
        assert_code_data = {
            'phone_code': read_rsp('getCode', '["phone_code"]'),
        }
        rsp = requests.post(self.assert_code_url, json=assert_code_data)
        write_rsp('assertCode', rsp.text)
