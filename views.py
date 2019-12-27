# -*- coding: utf-8 -*-
# @Time    : 2019/10/15 13:14
# @Author  : zhaihuide@jiandan100.cn
# @Site    : 
# @File    : views.py
# @Software: PyCharm
from util.tools import *
from flask import Flask, request
import random
import string
import json
from util.tools import md5

app = Flask(__name__)


def phone_code(counts):
    random_str_list = [random.choice(string.digits + string.ascii_letters) for _ in range(int(counts))]
    random_str = ''.join(random_str_list)
    return random_str


@app.route("/getCode", methods=['post'])
def index():
    rsp = {
        'code': '',
        'phone_code': '',
        'msg': ''
    }
    if request.method == 'POST':
        data = request.get_json()
        if len(data) == 0:
            rsp['code'] = 204
            rsp['msg'] = '缺少必要参数'
            return json.dumps(rsp)
        timestamp = int(time.time())

        if data['timestamp'] == md5(timestamp):
            rsp['code'] = 200
            rsp['phone_code'] = phone_code(4)
            rsp['msg'] = 'success'
            # todo 自定义写data函数

            return json.dumps(rsp)
        else:
            rsp['code'] = 202
            rsp['msg'] = 'timestamp is false'
            return json.dumps(rsp)


@app.route("/assertCode", methods=['post'])
def assert_code():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        code = read_rsp('phone_code', '["phone_code"]')
        success_rsp = {
            'code': 200,
            'msg': 'success'
        }
        failed_rsp = {
            'code': 401,
            'msg': 'failed'
        }
        if data['phone_code'] == code:
            return json.dumps(success_rsp)
        return json.dumps(failed_rsp)


if __name__ == '__main__':
    app.run(debug=True)