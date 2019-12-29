# -*- coding: utf-8 -*-
# @Time    : 2019/11/26 13:17
# @Author  : zhaihuide@jiandan100.cn
# @Site    : 
# @File    : demo.py
# @Software: PyCharm
import time

import requests
from config import web_headers
from util.tools import md5

# url = 'https://172.16.0.220/uc/v1/login'
# url = 'https://jdapi.jd100.com/uc/v1/login'

# header = {
#     'Host': 'jdapi.jd100.com',
#     # 'content-type': 'application/x-www-form-urlencoded',
#     # 'Origin': 'https://www.jd100.com',
#     # 'Referer': 'https://www.jd100.com/login?fromurl=https://www.jd100.com/',
#     'source': 'web',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
# }
#
# data = {
#     "account": "JD1574675566298157",
#     "login_type": "1",
#     "user_pwd": "555645"
# }
# requests.packages.urllib3.disable_warnings()
# # web_headers['Origin'] = 'https://www.jd100.com'
# rsp = requests.post(url, data=data, headers=header, verify=False)
# print(rsp.text)

# import hashlib
#
# m = hashlib.md5()
#
# m.update(str(time.time()).encode(encoding='utf-8'))
# print(m.hexdigest())


# print(int(time.time() * 1000))

# rsp = requests.post(url='http://127.0.0.1:5000/getCode', json={'timestamp': md5(int(time.time()))})
# print(rsp.text)

# # 判断变量是否定义
# demo = '123'
# print('demo' in dir())


data = {
    'timestamp': md5(int(time.time())),
    'phone_code': 'L2gs'
}

url = 'http://127.0.0.1:5000/assertCode'
rsp = requests.post(url, json=data)
print(rsp.text)