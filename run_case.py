# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 9:48
# @Author  : zhaihuide@jiandan100.cn
# @Site    :
# @File    : run_case.py
# @Software: PyCharm
import os
import time
import config
from util.logger import Log
import importlib
import traceback
from util.tools import dynamic_case
from util.xlsUnit import Xls


def run_case():
    xls = Xls()
    success_list = []
    failed_list = []
    data_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    data_file_list = os.listdir(data_file_path)
    for data_file in data_file_list:
        with open(data_file_path + "/{}".format(data_file), 'r', encoding='utf-8') as f:
            data_dict = dynamic_case(f.read())

        for index, data in data_dict.items():
            if 'skip' in data:
                continue

            api = data['api'].split('.')
            test_module = importlib.import_module(config.SCRIPT_PATH + "." + api[0])
            test_obj = getattr(test_module, api[1])
            test_func = getattr(test_obj(), api[2])
            api[2] = api[2] + "_" + str(index)
            # 删除动态case中的多余参数
            if 'remove' in data:
                api[2] = api[2] + "_remove_{}".format(data['remove'])
                data.pop('remove')
            if 'null' in data:
                api[2] = api[2] + '_null_{}'.format(data['null'])
                data.pop('null')
            data.pop('api')
            if 'notes' in data:
                data.pop('notes')
            try:
                test_func(data=data, static_file_name=api[2])
                print(api[2].ljust(50) + 'OK'.rjust(50))
                success_list.append((api[2], 'OK'))
            except Exception:
                failed_list.append((api[2], 'failed', traceback.format_exc()))
                # traceback.print_exc()
                print(api[2].ljust(50) + 'failed'.rjust(50))
                Log.get_log().error(traceback.format_exc())

    Log.get_log().warning('success_counts: ----------> {} 条'.format(len(success_list)))
    Log.get_log().warning('failed_counts:  ----------> {} 条'.format(len(failed_list)))
    success_list.extend(failed_list)

    for line, i in enumerate(success_list):
        if len(i) == 2:
            xls.xls_write(line + 1, 1, i[0])
            xls.xls_write(line + 1, 2, i[1])
        elif len(i) == 3:
            xls.xls_write(line + 1, 1, i[0])
            xls.xls_write(line + 1, 2, i[1])
            xls.xls_write(line + 1, 3, i[2])

    xls.set_width_height(['A', 'B', 'C', 'D'], len(success_list))
    xls.save('./report/{} report.xlsx'.format(time.strftime('%Y-%m-%d %H-%M-%S')))


if __name__ == '__main__':
    run_case()
