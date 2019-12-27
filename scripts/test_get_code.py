# -*- coding: utf-8 -*-
# author: zhaihuide@jiandan100.cn
# time: 2019/12/21 21:08
# software: PyCharm
from util.tools import *


class TestGetCode(object):

    def test_get_code_first(self, data, static_file_name):
        timestamp = int(time.time())
        data['timestamp'] = md5(timestamp)
        rsp = send_req('getCode', data, method='post', json=1, test=1)
        write_rsp(static_file_name, rsp.text, skip_path_list=['["phone_code"]'])

    def test_get_code_second(self, data, static_file_name):
        rsp = send_req('getCode', data, method='post', json=1, test=1)
        write_rsp(static_file_name, rsp.text)
