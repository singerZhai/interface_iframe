# -*- coding: utf-8 -*-
# @Time    : 2019/11/23 16:58
# @Author  : zhaihuide@jiandan100.cn
# @Site    : 
# @File    : test_register.py
# @Software: PyCharm
from util.tools import *


class TestRegister(object):

    def test_register_user_exist(self, data, static_file_name):
        # print('data: {}'.format(data))
        rsp = send_req('register', data, 'post')
        # print('response: {}'.format(rsp.text))
        write_rsp(static_file_name, rsp.text)

    def test_register_success(self, data, static_file_name):
        data['mobile'] = get_phone_num()
        # print('data: {}'.format(data))
        rsp = send_req('register', data, 'post')
        # print('response: {}'.format(rsp.text))
        write_rsp(static_file_name, rsp.text, skip_path_list=['["data"]'])
