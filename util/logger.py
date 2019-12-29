# -*- coding: utf-8 -*-
import logging
import time
import os


class Log(object):
    """
    封装后的logging
    """

    logger = None

    @classmethod
    def get_log(cls):
        if not cls.logger:
            # 创建一个logger
            cls.logger = logging.getLogger()
            cls.logger.setLevel(logging.DEBUG)
            # 创建一个handler，用于写入日志文件
            cls.log_time = time.strftime("%Y_%m_%d_")
            log_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_file = os.path.join(log_file_path, 'log/{}.log'.format(time.strftime('%Y-%m-%d')))
            if not os.path.exists(os.path.join(log_file_path, 'log')):
                os.mkdir(os.path.join(log_file_path, 'log'))
            fh = logging.FileHandler(log_file, 'a', encoding='utf-8')
            fh.setLevel(logging.INFO)

            # 再创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.WARNING)

            # 定义handler的输出格式
            formatter = logging.Formatter(
                '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s] %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # 给logger添加handler
            cls.logger.addHandler(fh)
            cls.logger.addHandler(ch)

            # 关闭打开的文件
            fh.close()
            ch.close()
        return cls.logger


if __name__ == '__main__':
    Log.get_log().error("hello world")
