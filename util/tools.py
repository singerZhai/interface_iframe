# -*- coding: utf-8 -*-
import hashlib
import logging
import os
import re
import json
import time
import random
import string
import functools
import traceback
from json import JSONDecodeError

import requests
from config import web_headers, urls
from util.logger import Log

rsp_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rsp_file_path = os.path.join(rsp_file_path, 'static')
res_file_path = rsp_file_path.replace('\\', '/')

# res_file_path = rsp_file_path


def json_tools(string):
    return json.dumps(string, indent=4, ensure_ascii=False)


def check_json(json_str):
    try:
        json.loads(json_str)
        return True
    except Exception:
        return False


def get_phone_num():
    phone_num_start_list = ['13', '14', '15', '16', '17', '18', '19']
    phone_num_end_list = [random.choice(string.digits) for _ in range(9)]
    phone_num_end = ''.join(phone_num_end_list)
    return random.choice(phone_num_start_list) + phone_num_end


def get_random_username(length):
    random_list = [random.choice(string.digits) for _ in range(length)]
    random_username = ''.join(random_list)
    return 'vip' + random_username


def get_sql(key):
    with open(r"../sql/web_sql.json", "r", encoding="utf-8") as f:
        res_json = json.loads(f.read())
        return res_json.get(key)


def count_times(func):
    """
    统计函数、方法执行用时装饰器
    :param func:
    :return:
    """

    @functools.wraps(func)
    def init(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        print("运行 %s 函数用时：%.2f 秒" % (func.__name__, time.time() - start_time))

    return init


def _assert(file_path, rsp, skip_path_list):
    """
    断言json串，提供跳过指定key的验证
    :param file_path: 要验证的静态文件
    :param rsp: 本次返回的response.text
    :param skip_path_list: 跳过验证表达式的list
    :return: None
    注：
    skip_path_list 为一个list
    demo = {'person': {'username': 'ignore', 'age': 'ignore'}} 表达式为 ['["person"]["username"]', '["person"]["age"]']
    """
    if skip_path_list:
        if not isinstance(skip_path_list, list):
            Log.get_log().error("skip_path_list must be list")
            raise TypeError("skip_path_list must be list")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                old_rsp = json.loads(f.read())
            except JSONDecodeError:
                Log.get_log().error("解析原有json静态文件出错")
                f1 = open(file_path, 'wb')
                f1.truncate()
                f1.close()
        if not check_json(rsp):
            Log.get_log().error("response.text's type isn't json")
            return
        new_rsp = json.loads(rsp)
        if 'old_rsp' not in dir():
            Log.get_log().error('old_rsp is not defined')
            return
        if len(old_rsp) != len(new_rsp):
            return
        Log.get_log().info('old: ' + str(old_rsp))
        Log.get_log().info('new: ' + str(new_rsp))
        if skip_path_list is not None:
            for skip_path in skip_path_list:
                Log.get_log().info("已跳过 {} == {} 校验".format(eval('new_rsp{}'.format(skip_path)),
                                                            eval('old_rsp{}'.format(skip_path))))
                exec('old_rsp{}{}'.format(skip_path, ' = ""'))
                exec('new_rsp{}{}'.format(skip_path, ' = ""'))
            try:
                assert old_rsp == new_rsp
            except AssertionError:
                Log.get_log().error("校验失败：")
                Log.get_log().error("{} != {}".format(new_rsp, old_rsp))
                Log.get_log().error(traceback.format_exc())
                raise
        else:
            try:
                assert old_rsp == new_rsp
            except AssertionError:
                Log.get_log().error("校验失败：")
                Log.get_log().error("{} != {}".format(new_rsp, old_rsp))
                Log.get_log().error(traceback.format_exc())
                raise


def write_rsp(filename, rsp, skip_path_list=None):
    result = rename_test_func(filename)
    path = os.path.join(res_file_path, result)
    res_path = path.replace("\\", '/')
    if not os.path.exists(res_path):
        os.mkdir(res_path)
    file_path = res_path + '/{}.json'.format(filename)
    _assert(file_path, rsp, skip_path_list)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(rsp)


def read_rsp(filename, path):
    file_path = res_file_path + '/{}.json'.format(filename)
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            pass
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.loads(f.read())
    try:
        res = eval('json_data' + path)
    except Exception:
        Log.get_log().error("读取rsp参数出现错误")
        raise
    return res


def skip_case(func):
    @functools.wraps(func)
    def init(*args, **kwargs):
        logging.warning('skip testFunc --> {}'.format(func.__name__))
        return

    return init


def ignore_special_func(func_list):
    res_list = []
    if not isinstance(func_list, list):
        raise TypeError('typeError')
    for func in func_list:
        if not func.startswith('_'):
            res_list.append(func)
    return res_list


def dynamic_case(case_dict_str):
    case_dict = eval(case_dict_str)
    flag = 0
    res_dict = {}
    for i in case_dict.values():
        i_json = json.dumps(i)
        if "*" in i:
            res = i['*'].split(',')
            i.pop('*')
            for key in res:
                a = json.loads(i_json)
                a.pop(key)
                res_dict[str(flag)] = a
                res_dict[str(flag)]['remove'] = key
                flag += 1
        elif "?" in i:
            res = i['?'].split(',')
            i.pop('?')
            for key in res:
                a = json.loads(i_json)
                a[key] = ''
                res_dict[str(flag)] = a
                res_dict[str(flag)]['null'] = key
                flag += 1
        else:
            res_dict[str(flag)] = json.loads(i_json)
            flag += 1

    for i in res_dict.values():
        if "*" in i:
            i.pop("*")
        elif "?" in i:
            i.pop("?")
    return res_dict


def send_req(url_key, data=None, method=None, json=None, test=None):
    requests.packages.urllib3.disable_warnings()
    url = urls(url_key, test=test)
    if not data and not method:
        rsp = requests.get(url, headers=web_headers, verify=False)
    elif method == 'post':
        if not json:
            rsp = requests.post(url=url, data=data, headers=web_headers, verify=False)
        else:
            rsp = requests.post(url=url, json=data, headers=web_headers, verify=False)
    else:
        raise Exception('method not find')
    return rsp


def md5(need_md5):
    if not isinstance(need_md5, str):
        need_md5 = str(need_md5)
    m = hashlib.md5()
    m.update(need_md5.encode(encoding='utf-8'))
    return m.hexdigest()


def rename_test_func(func_name):
    pattern = re.compile(r'test_(.*?)_\d+.*?')
    res = pattern.findall(func_name)
    result = res[0].split('_')[0:-1]
    result = '_'.join([i for i in result])
    return result


if __name__ == '__main__':
    # print(get_phone_num())
    # with open("../data/register.json", 'r', encoding='utf-8') as f:
    #     res = f.read()
    # # print(res)
    # print(json_tools(dynamic_case(res)))
    # print(md5('123'))
    print(res_file_path)
