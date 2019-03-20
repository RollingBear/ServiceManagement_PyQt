# -*- coding: utf-8 -*-

#   2019/3/19 0019 上午 11:23     

__author__ = 'RollingBear'

import configparser

# class toDict(configparser.ConfigParser):
#
#     def as_dict(self):
#
#         d = dict(self._sections)
#
#         for k in d:
#             d[k] = dict(d[k])
#         return d
#
# cfg = toDict()
# cfg.read('\\config\\service_name.ini', encoding='utf8')
# print(cfg.as_dict())
#
# dict = config.config('\\config\\service_name.ini')
#
# print(1)
# print(dict)

import config

conf = config.config('\\config\\service_name.ini')
print(conf.outer_element_count())
