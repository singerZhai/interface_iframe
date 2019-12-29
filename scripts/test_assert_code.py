# -*- coding: utf-8 -*-
# author: zhaihuide@jiandan100.cn
# time: 2019/12/29 17:04
# software: PyCharm
from util.tools import *


class TestAssertCode(object):

    def test_assert_code_first(self, data, static_file_name):
        if data['code'] == 'true':
            data['code'] = read_rsp('phone_code', '["phone_code"]')
        if data['timestamp'] == 'true':
            pass