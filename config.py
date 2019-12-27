# -*- coding: utf-8 -*-
from util.user_agent import random_ua

SCRIPT_PATH = 'scripts'

TEST_MODULES_START = 'test'

TEST_OBJ_START = 'Test'

TEST_FUNC_START = 'test'

REPORT_PATH = 'reports'

web_headers = {
    'source': 'web',
    'Host': 'jdapi.jd100.com',
    'User-Agent': random_ua
}

# 生产环境url
# main_url = 'https://jdapi.jd100.com'

# 测试环境url
main_url = 'https://172.16.0.220'

# 测试
test_main_url = 'http://127.0.0.1:5000'


def urls(key, test=None):
    urls_dict = {
        'register': '/uc/v1/reg',
        'login': '/uc/v1/login',
        'getCode': '/getCode'
    }
    if test:
        return test_main_url + urls_dict.get(key)
    return main_url + urls_dict.get(key)


if __name__ == '__main__':
    print(urls('login'))
