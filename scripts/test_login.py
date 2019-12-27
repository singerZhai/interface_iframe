# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 20:30
# @Author  : zhaihuide@jiandan100.cn
# @Site    : 
# @File    : test_login.py
# @Software: PyCharm
from util.tools import *


class TestLogin(object):

    def test_login(self, data, static_file_name):
        # print('data: {}'.format(data))
        rsp = send_req('login', data, 'post')
        # print('rsp: {}'.format(rsp.text))
        write_rsp(static_file_name, rsp.text)
        # time.sleep(60)
