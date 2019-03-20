# -*- coding: utf-8 -*-

#   2019/3/19 0019 上午 9:58     

__author__ = 'RollingBear'


import config

from PyQt5.QtGui import QPixmap


class image:

    img_config = config.config('\\config\\config.ini')

    red_img =QPixmap(img_config.get('image_address').red)
    green_img = QPixmap(img_config.get('image_address').green)
    yellow_img = QPixmap(img_config.get('image_address').yellow)
    logo_img = QPixmap(img_config.get('image_address').logo)
    message_img = QPixmap(img_config.get('image_address').message)