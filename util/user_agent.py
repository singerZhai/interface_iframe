# -*- coding: utf-8 -*-
from fake_useragent import UserAgent

ua = UserAgent()
random_ua = ua.random


if __name__ == '__main__':
    print(random_ua)
