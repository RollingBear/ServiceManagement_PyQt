# -*- coding: utf-8 -*-

#   2019/3/19 0019 上午 10:31     

__author__ = 'RollingBear'

import interface

import sys
import ctypes
import logging
import traceback

from PyQt5.QtWidgets import QApplication


def start():
    app = QApplication(sys.argv)
    sm = interface.service_manamgement()
    sys.exit(app.exec_())


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        logging.info(traceback.format_exc())
        return False


def get_admin():
    if is_admin():
        start()
    else:
        try:
            if sys.version_info[0] == 3:
                ctypes.windll.shell32.shellExecuteW(None, 'runas', sys.executable, __file__, None, 1)
        except Exception:
            logging.info(traceback.format_exc())


if __name__ == '__main__':
    get_admin()
